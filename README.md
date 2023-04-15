# Guess Number Bot
This is a simple Telegram bot that plays a game where the bot will guess a number and the user has a limited number of attempts to guess it. The bot writes the results of the games to a SQLite database and provides a command to show statistics.

## Installation
To use this bot, you first need to create a Telegram bot and obtain a token. Follow the instructions provided by [Telegram documentation](https://core.telegram.org/bots#6-botfather) to create your bot and obtain the token.

Then, clone this repository
``` shell 
# using github
git clone https://github.com/<username>/<repository>.git
# using gitlab 1)
git clone https://gitlab.com/<username>/<repository>.git
# using gitlab 2)
git clone https://<username>@github.com/<username>/<repository>.git
```

and install the required dependencies using pip:
```shell
pip install -r requirements.txt
```

or setup <b>conda environment</b>
<details>
    <summary> <b>Expand</b> </summary>

``` shell
# create env
conda env create --name "my_environment" python=3.9

or 
# depending on your anaconda version
conda create --name "my_environment" python=3.10

# then install requirements:
pip install -r requirements.txt
```
</details>

## Usage
To start the bot, run the following command:

Copy code
python bot.py
You can interact with the bot in Telegram by searching for your bot's username and sending a message.

The following commands are supported:

* /start - Start the game.
* /stop - Stop the game.
* /stats - Show statistics of the games.



## Database
The bot uses a SQLite database to store the results of the games. The database file is created automatically when the bot starts and is located in the database/ directory.

## License
For now no license :)