import sys
import getopt
from typing import Optional
from dataclasses import dataclass
from typing import Any
from dotenv import load_dotenv

from logger import Logger
from settings import Settings

@dataclass
class SettingsBase:
  long: str
  short: Optional[str] = None
  default_value: Optional[str] = None
  help_text: str = ""
  
def proposed_options() -> list[SettingsBase]:
  help = SettingsBase("help", help_text="Print this help")
  settings = SettingsBase("settings", default_value="conf/settings.ini", help_text="Path for the ini settings file\n\tOptional\n\tA relative or absolute path")
  env = SettingsBase("env", default_value="conf/.env", help_text="Path for the env file if needed\n\tOptional\n\tA relative or absolute path")
  log_console = SettingsBase("log_console", default_value="True", help_text="Choose to print the logs in the console\n\tOptional\n\tBoolean")
  log_info_file = SettingsBase("log_info_file", help_text="The path to save the logs (info level minimum)\n\tOptional\n\tA relative or absolute path")
  log_crit_file = SettingsBase("log_crit_file", help_text="The path to save the logs (error level minimum)\n\tOptional\n\tA relative or absolute path")
  log_level = SettingsBase("log_level", default_value="20", help_text="The minimal log level as defined in the python logging module. A lower level includes all above\n\t\tOptional\n\t\t\t- 10 : DEBUG\n\t\t\t- 20 : INFO\n\t\t\t- 30 : ERROR\n\t\t\t- 40 : CRITICAL")

  return [help, settings, env, log_console, log_info_file, log_crit_file, log_level]

def print_help(options: list[SettingsBase]):

  for option in options:
    text = f"Long option : --{option.long}"
    if option.short:
      text = f"{text};\n\tShort option : -{option.short}"
    text = f"{text};\n\tDefault: {str(option.default_value)}"
    text = f"{text};\n\tDescription: {option.help_text}"

    print(f"{text}")
  sys.exit(0)

def validate_mandatory_options(params: dict[str, str]) -> None:
  """
    This function validates the minimal mandatory options

    :param params: The dict of parameters we want to validate
    :type params: dict[str, str]
    :raise: A ValueError Exception if a key is missing
  """
  proposed = proposed_options()
  mandatory_options = [option.long for option in proposed]
  missing = [opt for opt in mandatory_options if opt not in params]
  if missing:
      raise ValueError(f"Missing mandatory options: {', '.join(missing)}. If you have any doubts you shall extend the proposed_options function")

def start_app(parameters : dict[str, str], app_name : str = "NO_NAME") -> None:
  """
    This function initialize the logger and load the settings and the env file

    :param parameters: A dict containing the necessary data to load the app
    :type parameters: dict[str, str]
    :param app_name: The name of the application
    :type app_name: str
  """
  validate_mandatory_options(parameters)

  Logger.get_instance().load_logger(info_file=parameters["log_info_file"],
                                    critical_file=parameters["log_crit_file"],
                                    console=bool(parameters["log_console"]),
                                    level=int(parameters["log_level"]),
                                    app_name=app_name)
  
  # Printing options for debug purposes in the logger (i.e in files and console if wanted)
  Logger.info(value="Given options : ")
  for key, parameter in parameters.items():
    Logger.info(f"--{key}={parameter}")

  Settings.get_instance().load_settings(parameters["settings"])
  load_dotenv(parameters["env"])
  
def parse_command_line(args : Any, options: list[SettingsBase] = proposed_options()) -> dict:
  """
    Cette fonction parse la ligne de commande des options fournis et le renvoi sous forme de dictionnaire d'options

    Par exemple si on fournit le tableau suivant :
    ["--settings=./conf/settings.ini", "--log_info_file=./logs/info.log"]

    A noter qu'il existe des valeurs par defaut pour toutes les options propose afin que si l'information n'est pas passe une valeur par defaut puisse
    etre utilise

    :param args: Le tableau des options que l'on fournit en parametre
    :type args: []
    :return: Un dictionnaire avec les informations de la ligne de commande
    :rtype: dict
  """
  long_options = []
  short_options = ""
  for option in options:
    long_options.append(f"{option.long}=")
    short_options = f"{option.short}"

  opts, args = getopt.getopt(args, short_options, long_options)
  result = {}

  for opt, arg in opts:
      clean_opt = opt.lstrip('-')  # retire les "--"
      result[clean_opt] = arg if arg else True  # True pour les flags (genre --help)
  
  for option in options:
    if option.long not in result.keys():
      result[option.long] = option.default_value

  return result
