Created for the _Taiko Suiji Cup 2023_, in which players are divided by their rank into equal-sized seeds, and each team consists of a randomly chosen set number of players from each seed. This randomizer attempts to create teams in a stochastic way while attempting to balance teams' skill levels in relation to each other at the same time.

# Installation
Requirements: Python 3, pipenv
### Configuration Parameters
Parameters such as the gamemode, number of teams in the tournament, and number of players per team can be set by editing `config.py`. Make sure that `CLIENT_ID` and `CLIENT_SECRET` are configured with an OAuth client, for which instructions to create one can be found at https://circleguard.github.io/ossapi/creating-a-client.html.

Players will be loaded from the csv named `player_ids.csv`. This file comes premade with a list of ids of players from the first iteration of the _Taiko Suiji Cup_, but you can change it to contain whatever ids you wish.

### Running the Script
In a command terminal, make sure you're in the root directory of the project and enter:
```
> pipenv install
```

Then, every time you want to run the script, enter:
```
> pipenv run python main.py
```

 A csv will be saved to the project folder containing a list of all the generated teams. The csv will be titled with the timestamp it was made at, and formatted with the following column headers: `team,seed,player,pp`.

# Algorithm Implementation
### Motivation
The core idea of the randomizer's algorithm is to randomly swap players between teams, keep the changes if the balance has gotten better, and revert the changes if it's gotten worse. After repeating this process many times, the tournament should be more balanced than it would be if it were fully random. 

This idea is a good start, but we need to decide what metric should be used to represent "balance". In the first iteration of the _Suiji Cup_, a similar idea was used to **make every team's total pp as close as possible**. This is an intuitive metric, however, it led to some teams having one high-ranked player and one low-ranked player in their seeds, which was a problem because those teams would simply have the high-ranked player in each seed play, outperforming every team who had two average-ranked players in the same seeds.

### Choosing Another Metric
Consider two teams whose A seeds have two players. Both A seeds have the same average pp, but one seed has a high-ranked player and a low-ranked player, and the other seed has two average-ranked players. How can we quantify the difference between these A seeds in a way that is optimizable? The metric I have chosen to represent this difference is the **pp variation** within the seed, because a seed with higher variation in pp will have both the strongest player and the weakest player, and therefore an advantage.

### Implementation
In order to clear up any ambiguity, we'll define a few terms:
- Seed: The set of all players in the tournament that are grouped into the same skill level.
- Team: The set of players forming a team. A team is comprised of a set number of players from each seed.
- Subteam: The set of players on a team that are grouped under a particular seed. A team is comprised of a number of subteams equal to the number of seeds.

The algorithm itself is made up of two phases. In each phase, players are repeatedly swapped until the chosen metric for that phase is lowered. If the metric is not lowered within a given number of swaps, the changes are reverted. This process is repeated for a given number of times. Below, each phase is described in more detail.

## Phase 1: Balance Seed pp
This phase runs once for each seed. For each seed, we swap players between subteams in an attempt to make every subteam's **pp** as close as possible. This means minimizing the **pp variation** across the entire seed.

## Phase 2: Balance Team pp Variation
In this phase, we swap subteams between teams in an attempt to make every team's **pp variation** as close as possible. This means minimizing the **pp variation variation** across the entire tournament. That is to say, if each team has a **pp variation** value, then we're trying to minimize the variation of that value across every team.

### Couldn't you have done this in a better way?
Yes.

If I were to do this again for a future _Suiji Cup_, I suspect that a gradient descent algorithm would work much, _much_ better. However, I did not have the knowledge or the available free time to research how to implement such an algorithm in this context.