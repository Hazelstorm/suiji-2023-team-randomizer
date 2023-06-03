from ossapi import Ossapi

# To learn about getting a client id + secret, see:
# https://circleguard.github.io/ossapi/creating-a-client.html
CLIENT_ID = 0
CLIENT_SECRET = ""

# Randomizer seed
SEED = 727

# How many iterations the randomizer will take
NUM_ITERATIONS = 1000

# Tournament size
NUM_PLAYERS_PER_SUBTEAM = 2
NUM_SUBTEAMS_PER_TEAM = 3
NUM_TEAMS_PER_TOURNAMENT = 16

api = Ossapi(CLIENT_ID, CLIENT_SECRET)
