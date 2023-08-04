import get_players
import json

if __name__ == "__main__":
    print("Fetching users...")
    players = get_players.from_osu()

    with open("players.json", "w+") as file:
        json.dump([{"username": player.username, "pp": player.pp}
                   for player in players], file)

    print("players.json has been generated! You may set PLAYER_DATA_SOURCE to \"locked\"")
