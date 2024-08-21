import configparser
import platform
from pathlib import Path

class Config:
    def __init__(self):
        if platform.system() == "Windows":
            config_path = Path(__file__).resolve().parent / "config.ini"
        else:
            config_path = "/etc/log/config.ini"
        self.__config = configparser.ConfigParser()
        self.__config.read(config_path, "utf-8")

    @property
    def log_name(self):
        try:
            return self.__config["log"]["log_name"]
        except:
            return "log"

    @property
    def console_log_level(self):
        try:
            return self.__config["log"]["console_log_level"]
        except:
            return "INFO"

    @property
    def file_log_level(self):
        try:
            return self.__config["log"]["file_log_level"]
        except:
            return "INFO"

    @property
    def log_dir(self):
        try:
            return self.__config["log"]["log_dir"]
        except:
            return "/var/log/log"

    @property
    def open_console(self):
        try:
            return self.__config.getint("log", "open_console")
        except:
            return 1



config=Config()


