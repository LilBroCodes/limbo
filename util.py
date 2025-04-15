import json
import logging
import re
from enum import Enum
from typing import Optional, List

from colorlog import ColoredFormatter

class Logging:
   @staticmethod
   def change_log_format(name: str):
      logger = logging.getLogger(name)
      logger.setLevel(logging.DEBUG)

      formatter = ColoredFormatter(
         fmt='%(light_black)s%(asctime)s %(log_color)s%(levelname)-8s %(purple)s%(name)s: %(message_log_color)s%(message)s',
         datefmt='%Y-%m-%d %H:%M:%S',
         reset=True,
         log_colors={  # Controls only %(log_color)s (used around levelname)
            'DEBUG': 'cyan',
            'INFO': 'white',
            'WARNING': 'yellow',
            'ERROR': 'red',
            'CRITICAL': 'bold_red',
         },
         secondary_log_colors={  # Controls %(message_log_color)s (used around message)
            'message': {
               'DEBUG': 'bold_light_black',
               'INFO': 'white',
               'WARNING': 'yellow',
               'ERROR': 'red',
               'CRITICAL': 'bold_red',
            }
         },
         style='%'
      )

      logger.handlers.clear()

      handler = logging.StreamHandler()
      handler.setFormatter(formatter)
      logger.addHandler(handler)

      return logger


class Function:
    def __init__(self, name: str, commands: List[str], limbo = False):
        self.name = name
        self.commands = commands
        self.limbo = limbo

    def __repr__(self):
        return f"McFunction(name={self.name!r}, commands={self.commands!r})" if not self.limbo else f"LmFunction(name={self.name!r}, commands={self.commands!r})"

class MapType(Enum):
    ENTITY = "Entity"
    BLOCK = "Block"
    GLOBAL = "Global"

    def __str__(self):
        return self.value

class Mapping:
    def __init__(self, owner: MapType, subcommand: str, translatable: str):
        self.owner = owner
        self.subcommand = subcommand
        self.translatable = translatable

    def to_dict(self):
        return {
            "owner": self.owner.value,
            "subcommand": self.subcommand,
            "translatable": self.translatable
        }

class Mappings:
    def __init__(self, mappings=None):
        if mappings is None:
            mappings = []
        self.mappings = mappings

    def get_translatable(self, owner: MapType, subcommand: str):
        bucket = [i for i in self.mappings if i.owner == owner and i.subcommand == subcommand]
        return bucket[0] if len(bucket) > 0 else None

    def to_dict(self):
        return {
            "mappings": [m.to_dict() for m in self.mappings]
        }

def string_format(format_string, args):
    return re.sub(r'%(\d+)', lambda m: str(args[int(m.group(1)) - 1]), format_string)

def get_all(data: List[dict], key: str, value: str):
   return [i for i in data if i.get(key) == value]
