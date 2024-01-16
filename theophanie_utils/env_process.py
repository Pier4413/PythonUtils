from os import environ

from logger import Logger

def load_an_environ(value : str, default_value : str) -> str:
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
      Logger.debug(value=f"The imported value of {value} is {data}")
      return data
    return default_value
  except Exception as e:
    Logger.warning(value=f"There was an error while loading the env variable : {value}")
    return default_value