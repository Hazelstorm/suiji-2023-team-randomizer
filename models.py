import csv
import time
from ossapi import UserCompact
from more_itertools import batched
from statistics import variance, mean
from tqdm import tqdm
from typing import Callable, TypeVar
from functools import cached_property

import random

from config import (
    NUM_PLAYERS_PER_SUBTEAM,
    NUM_SUBTEAMS_PER_TEAM,
    NUM_TEAMS_PER_TOURNAMENT,
    NUM_ITERATIONS,
    SEARCH_DEPTH,
    MODE,
)

T = TypeVar("T")

NUM_PLAYERS_PER_TOURNAMENT = (
    NUM_PLAYERS_PER_SUBTEAM * NUM_SUBTEAMS_PER_TEAM * NUM_TEAMS_PER_TOURNAMENT
)
NUM_PLAYERS_PER_SEED = NUM_PLAYERS_PER_SUBTEAM * NUM_TEAMS_PER_TOURNAMENT


class Player:
    # user: UserCompact

    @cached_property
    def pp(self) -> float:
        # user_stats = self.user.statistics_rulesets
        try:
            # pp = getattr(user_stats, MODE.value).pp

            pp = self.user["pp"]
        except AttributeError:
            raise AttributeError(
                f"Player {self.user.username} has no pp for the mode {MODE.value}.")
        return pp

    def __init__(self, user: UserCompact) -> None:
        self.user = user


# Represents a subset of a team consisting of all players on that team within a single seed
class Subteam:
    players: list[Player]

    # Average pp value in this subteam
    @property
    def pp(self) -> float:
        return mean([player.pp for player in self.players])

    # Variance of pp within this subteam
    @property
    def variance(self) -> float:
        return variance([player.pp for player in self.players])

    def __init__(self, players: list[Player]) -> None:
        assert len(players) == NUM_PLAYERS_PER_SUBTEAM
        self.players = players

    def replace_player(self, player_to_remove: Player, player_to_add: Player) -> None:
        self.players.remove(player_to_remove)
        self.players.append(player_to_add)


class Team:
    subteams: dict[int, Subteam]

    @property
    def variance(self) -> float:
        return mean([subteam.variance for subteam in self.subteams.values()])

    def __init__(self, subteams: dict[int, Subteam]) -> None:
        assert len(subteams) == NUM_SUBTEAMS_PER_TEAM
        self.subteams = subteams

    def replace_subteam(self, seed_tier: int, subteam_to_add: Subteam) -> None:
        self.subteams[seed_tier] = subteam_to_add


class Seed:
    subteams: list[Subteam]

    # Used to optimize subteams having similar pp
    @property
    def pp_variance(self):
        return variance([subteam.pp for subteam in self.subteams])

    def __init__(self, players: list[Player] = []) -> None:
        assert len(players) == NUM_PLAYERS_PER_SEED
        self.subteams = [
            Subteam(subteam_players)
            for subteam_players in batched(players, NUM_PLAYERS_PER_SUBTEAM)
        ]


class Tournament:
    teams: list[Team]
    seeds: dict[int, Seed]
    players: list[Player]

    # Used to optimize teams having similar pp variance
    @property
    def pp_variance_variance(self):
        return variance([team.variance for team in self.teams])

    def __init__(self, players: list[Player]) -> None:
        assert len(players) >= NUM_PLAYERS_PER_TOURNAMENT, (
            "Not enough players given for the current tournament parameters:\n"
            + f"{NUM_PLAYERS_PER_SUBTEAM=}\n"
            + f"{NUM_SUBTEAMS_PER_TEAM=}\n"
            + f"{NUM_TEAMS_PER_TOURNAMENT=}\n"
            + f"Total Player Count {NUM_PLAYERS_PER_TOURNAMENT}\n"
            + "More players can be added in player_ids.csv\n"
            + "These parameters can be changed in config.py"
        )
        eligible_players = sorted(
            players,
            key=lambda player: player.pp,
            reverse=True,
        )[:NUM_PLAYERS_PER_TOURNAMENT]

        # Initialize seeds
        self.seeds = dict()
        players_per_seed = batched(eligible_players, NUM_PLAYERS_PER_SEED)
        for seed_tier, seed_players in enumerate(players_per_seed):
            random.shuffle(seed_players)
            self.seeds[seed_tier] = Seed(seed_players)

        # Initialize empty teams
        self.teams = []

    def init_teams(self) -> None:
        for seed in self.seeds.values():
            random.shuffle(seed.subteams)

        self.teams = [
            Team(
                {seed_tier: seed.subteams[i]
                    for seed_tier, seed in self.seeds.items()}
            )
            for i in range(NUM_TEAMS_PER_TOURNAMENT)
        ]

    def balance_seed_pp(self) -> None:
        for seed_tier, seed in self.seeds.items():
            print("Randomizing subteams...")
            minimize_metric(
                seed.subteams, swap_random_players, lambda: seed.pp_variance
            )

    def balance_team_variance(self) -> None:
        print("Randomizing teams...")
        minimize_metric(
            self.teams, swap_random_subteams, lambda: self.pp_variance_variance
        )

    def balance_tournament(self) -> None:
        self.balance_seed_pp()
        self.init_teams()
        self.balance_team_variance()

    def export_teams(self) -> None:
        filename = f"teams-{time.strftime('%Y%m%d-%H%M%S')}-{MODE.value}.csv"
        with open(filename, "a", newline="") as f:
            writer = csv.DictWriter(f, ["team", "seed", "player", "pp"])
            writer.writeheader()
            for i, team in enumerate(self.teams):
                for seed_tier, subteam in team.subteams.items():
                    for player in subteam.players:
                        writer.writerow(
                            {
                                "team": i,
                                "seed": seed_tier,
                                "player": player.user["username"],
                                "pp": player.user["pp"],
                            }
                        )
        print(f"Teams successfully exported to: {filename}")


def minimize_metric(
    lst: list[T],
    swap_func: Callable[[T, T], Callable[[None], None]],
    metric_func: Callable[[], float],
) -> list[float]:

    for _ in tqdm(range(NUM_ITERATIONS)):
        old_metric = metric_func()

        # Swap between 2 random objects in the list, 5 times
        # See examples of swap functions below
        reverts = []
        for _ in range(SEARCH_DEPTH):
            obj1, obj2 = random.sample(lst, 2)
            revert = swap_func(obj1, obj2)
            reverts.append(revert)
            # If the metric is ever lower, immediately bail out and
            # keep the changes
            if metric_func() < old_metric:
                break

        # If the metric increased, revert the changes
        # Reverts need to be applied in reverse order
        if metric_func() > old_metric:
            for revert in reverts[::-1]:
                revert()


# Swaps a random player between 2 subteams,
# returns a function that can be called to revert this operation
def swap_random_players(subteam1: Subteam, subteam2: Subteam) -> Callable[[None], None]:
    player1 = random.choice(subteam1.players)
    player2 = random.choice(subteam2.players)

    subteam1.replace_player(player1, player2)
    subteam2.replace_player(player2, player1)

    def revert() -> None:
        subteam1.replace_player(player2, player1)
        subteam2.replace_player(player1, player2)

    return revert


# Swaps a random subteam between 2 teams,
# returns a function that can be called to revert this operation
def swap_random_subteams(team1: Team, team2: Team) -> Callable[[None], None]:
    seed_tier = random.randint(0, NUM_SUBTEAMS_PER_TEAM - 1)
    subteam1 = team1.subteams[seed_tier]
    subteam2 = team2.subteams[seed_tier]

    team1.replace_subteam(seed_tier, subteam2)
    team2.replace_subteam(seed_tier, subteam1)

    def revert() -> None:
        team1.replace_subteam(seed_tier, subteam1)
        team2.replace_subteam(seed_tier, subteam2)

    return revert
