from os import environ
import sys

try:
  from modules.logger.logger import Logger
except Exception as e:
  print(f"No logger module can't load it", file=sys.stderr)
  Logger = None

def load_an_environ(value : str) -> str | None:
  """
    This function load an element from the environment with checks

    :param value: The key of the environment
    :type value: str
    :param type: The type as a class type; Optional; Default : str
    :type type: A class type
  """
  try:
    data = environ[value]
    if data is not None and data != "":
      if Logger is not None:
        Logger.debug(f"The imported value of {value} is {data}")
      return data
    return None
  except Exception as e:
    if Logger is not None:
      Logger.warning(f"There was an error while loading the env variable : {value}")
    return None