import ossapi

# Whether the application should grab user profiles from player_ids.csv
# via the osu! API or grab user data from google spreadsheets
# By setting this to True you will also need to provide CLIENT_ID and CLIENT_SECRET below
USE_OSU_API = False

# To learn about getting a client id + secret, see:
# https://circleguard.github.io/ossapi/creating-a-client.html
CLIENT_ID = 0
CLIENT_SECRET = ""

# Randomizer seed
SEED = 727

# How many iterations the randomizer will take
# Setting this to a higher value will lead to better results
# at the expense of more time taken.
NUM_ITERATIONS = 100000

# How many random player swaps the randomizer will make at each iteration
# Setting this to a higher value will lead to better results
# at the expense of more time taken.
SEARCH_DEPTH = 4

# Tournament size
NUM_PLAYERS_PER_SUBTEAM = 2
NUM_SUBTEAMS_PER_TEAM = 4
NUM_TEAMS_PER_TOURNAMENT = 24

# Which gamemode's pp value to use for balancing
MODE = ossapi.GameMode.TAIKO
