Created for the 2023 Taiko Suiji Cup, in which players are divided by their rank into equal-sized seeds, and each team consists of a randomly chosen set number of players from each seed. This randomizer attempts to create teams in a stochastic way while attempting to balance teams' skill levels in relation to each other at the same time.

# Installation
Requirements: Python 3.9, pipenv
### Configuration Parameters
Parameters such as the number of teams in the tournament and the number of players per team can be set by editing `config.py`. Make sure that `CLIENT_ID` and `CLIENT_SECRET` are configured with an OAuth client, for which instructions to create one can be found at https://circleguard.github.io/ossapi/creating-a-client.html.
### Running the Script
In a command terminal, make sure you're in the root directory of the project and enter:
```
> pipenv install
> pipenv run python main.py
```
