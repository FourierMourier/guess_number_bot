from typing import Dict
from constants.game import GameConstants

LEXICON_EN: Dict[str, str] = {
    '/start': (f"Hi, i will generate number and you will try to guess it\n"
               f"you can also use commands /help or /stat"),
    '/help': (f"Rules: I'll guess the number in range [1, 100] "
              f"and you will try to guess;\n"
              f"you have {GameConstants.attempts} attempts.\n"
              f"Available commands:\n"
              f"/help - rules & available commands,\n"
              f"/cancel - to quit the game,\n"
              f"/stat - get statistics"),
    'no_game_yet': f"We haven't played yet. Shall we /start?",
    'already_in_game': (f"We're already in the game. "
                        f"I will respond only to numbers and command '/cancel' and '/stat'"),
}
