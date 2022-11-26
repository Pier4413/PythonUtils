import sys
import getopt
from typing import Any
from dotenv import (
    load_dotenv
)

try:
  from ..logger.logger import Logger
except Exception as e:
  print(f"Error while importing Logger : {e}", file=sys.stderr)
  Logger = None

try:
  from ..settings.settings import Settings
except Exception as e:
  print(f"Error while importing Settings : {e}", file=sys.stderr)
  Settings = None

def options() -> list:
  return ["help", "settings", "env", "log_console", "log_level", "log_info_file", "log_crit_file"]

def print_help():
  text = [
    "Print this help",
    "Path for the ini settings file\n\tOptional\n\tA relative or absolute path\n\tDefault : None", 
    "Path for the env file if needed\n\tOptional\n\tA relative or absolute path\n\tDefault : None"
  ]

  if Logger is not None:
    text = text + Logger.helper()

  if len(text) == len(options()):
    for value in range(0, len(options())):
      print(f"{options()[value]}=\t{text[value]}\n\n")
  else:
    print("Error in the helper. Please contact the developer of the application")
  sys.exit(0)

def start_app(parameters : dict) -> None:
  """
    Cette fonction initialise le logger et charge le fichier de conf

    A noter cette fonction n'est pas teste car toutes les fonctions utilises au sein de cette fonction viennent de sous-module et sont sensé etre teste dans leur propre module

    :param parameters: Un dictionnaire des parametres necessaire pour initialiser les informations
    :type parameters: dict
  """

  if Logger is not None:
    # Logger loading
    Logger.get_instance().load_logger(info_file=parameters["log_info"], critical_file=parameters["log_critical"], console=parameters["log_console"], level=parameters["log_level"], app_name="Accounts")
    
    # Printing options for debug purposes in the logger (i.e in files and console if wanted)
    Logger.info(value="Given options : ")
    Logger.info(value=f"--settings={parameters['conf_file_name']}")
    Logger.info(value=f"--env={parameters['env_file']}")
    Logger.info(value=f"--log_level={parameters['log_level']}")
    Logger.info(value=f"--log_info_file={parameters['log_info']}")
    Logger.info(value=f"--log_crit_file={parameters['log_critical']}")
    Logger.info(value=f"--log_console={parameters['log_console']}")
  else:
    print(f"No logger module is present can't prepare the module", file=sys.stderr)

  if Settings is not None:
    # Load settings
    Settings.get_instance().load_settings(parameters["conf_file_name"])
  else:
    print(f"No Settings module is present can't prepare the module", file=sys.stderr)
    
  # Env
  load_dotenv(parameters["env_file"])

def parse_command_line(args : Any) -> dict:
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
  conf_file_name = None
  env_file = None
  log_info = None
  log_critical = None
  log_level = 20
  log_console = False
  
  # Process command line options
  long = options()

  for value in range(1,len(long)):
    long[value] = long[value] + "="
  
  opts, args = getopt.getopt(args, "", long)

  for opt, arg in opts:
    if opt in ["--help"]:
      print_help()
    elif opt in ["--settings"]:
      conf_file_name = str(arg)
    elif opt in ["--log_level"]:
      log_level = int(arg)
    elif opt in ["--log_info_file"]:
      log_info = str(arg)
    elif opt in ["--log_crit_file"]:
      log_critical = str(arg)
    elif opt in ["--env"]:
      env_file = str(arg)
    elif opt in ["--log_console"]:
      log_console = bool(arg)
    else:
      print(f"Option not handled {opt}")

  return {
    "conf_file_name": conf_file_name,
    "log_level": log_level,
    "log_info": log_info,
    "log_critical": log_critical,
    "env_file": env_file,
    "log_console": log_console
  }
