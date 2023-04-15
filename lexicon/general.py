from pathlib import Path
import yaml

from constants.game import GameConstants
from utils.common.general import (
    load_yaml, attributes,
    colorstr, infoColorstr, warningColorstr, exceptionColorstr
)

from typing import Dict, Optional, Union, Any, Set, List


ROOT: Path = Path(__file__).parents[0]


class Commands:
    START: str = "start"
    HELP: str = "help"
    # CANCEL = "/cancel"
    # STAT = "stat"
    NO_GAME_YET: str = 'no_game_yet'
    ALREADY_IN_GAME: str = 'already_in_game'
    GAME_CANCELLED: str = 'game_cancelled'


class MissedLexiconLanguages(Exception):
    pass


class MissedCommands(Exception):
    pass


class LexiconModel:
    en_lang: str = 'en'
    supported_languages: Set[str] = {en_lang, 'ru', 'es'}
    no_command_found_response: str = "Command not found."

    __slots__ = ('_lexicon', )

    def __init__(self, lexicon_filepath: Optional[Union[str, Path]] = None):
        lexicon_filepath = lexicon_filepath or ROOT / 'lexicon.yaml'

        self.lexicon: Dict[str, Dict[str, str]] = load_yaml(lexicon_filepath, encoding='utf-8')

    @property
    def lexicon(self) -> Dict[str, Any]:
        return self._lexicon

    @lexicon.setter
    def lexicon(self, value: Dict[str, Dict[str, str]]):
        assert isinstance(value, dict), f"lexicon must be of type dict, got {type(value)}"
        # 1. check if you have all required commands:
        commands_set: Set[str] = set(value.keys())
        attribute_names: List[str] = attributes(Commands)
        attribute_values: Set[str] = set([getattr(Commands, an) for an in attribute_names])
        missed_commands = attribute_values - commands_set
        if missed_commands:
            raise MissedCommands(f"Not enough commands: {missed_commands}")
        # 2. check languages
        for command, lang_to_answer in value.items():
            langs_set: Set[str] = set(lang_to_answer.keys())
            missing_languages = self.supported_languages - langs_set
            if missing_languages:
                raise MissedLexiconLanguages(
                    f"Not enough languages: for command {command}, missing {', '.join(missing_languages)}")

        self._lexicon = value

    def get_response(self, command: str, language: Optional[str] = None):
        language = language or 'en'
        command = command.lstrip('/')
        command_responses: Union[str, Dict[str, str]] = self.lexicon.get(command, self.no_command_found_response)
        if command_responses == self.no_command_found_response:
            return command_responses
        if language not in command_responses:
            raise ValueError(f"Invalid language: {language}")
        # return command_responses.get(language, "Language not found.")
        return command_responses[language]


Lexicon = LexiconModel()

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


def _main():
    lexicon = LexiconModel()

    # Get the English response for the "/start" command
    english_response = lexicon.get_response('/start', 'en')
    print(english_response)

    # Get the Russian response for the "/cancel" command
    russian_response = lexicon.get_response('/cancel', 'ru')
    print(russian_response)


if __name__ == '__main__':
    _main()
