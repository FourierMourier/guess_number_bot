import yaml
import pydantic
from pathlib import Path


ROOT: Path = Path(__file__).parents[0]


class BotConfigModel(pydantic.BaseModel):
    token: pydantic.StrictStr


with open(ROOT / 'bot.yaml', 'r') as f:
    bot_config_dict: dict = yaml.safe_load(f)

BotConfig = BotConfigModel(**bot_config_dict)
