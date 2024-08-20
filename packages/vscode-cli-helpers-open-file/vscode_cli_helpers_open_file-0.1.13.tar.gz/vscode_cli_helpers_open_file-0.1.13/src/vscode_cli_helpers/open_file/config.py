import configparser
import importlib.resources
import logging
import shutil
import typing
from configparser import ConfigParser
from pathlib import Path
from typing import Optional

import platformdirs

from vscode_cli_helpers.open_file.exceptions import ConfigException


class Config:
    # NOTE: These are made class variables since they must be accessible from
    #   pytest before creating an object of this class
    dirlock_fn = ".dirlock"
    config_fn = "config.ini"
    appname = "vscode-cli-helpers-open-file"

    def __init__(self) -> None:
        self.lockfile_string = "author=HH"
        self.config_dir = self.get_config_dir()
        self.config_path = Path(self.config_dir) / self.config_fn
        self.read_config()

    def check_correct_config_dir(self, lock_file: Path) -> None:
        """The config dir might be owned by another app with the same name"""
        if lock_file.exists():
            if lock_file.is_file():
                with open(str(lock_file), encoding="utf_8") as fp:
                    line = fp.readline()
                    if line.startswith(self.lockfile_string):
                        return
                msg = "bad content"
            else:
                msg = "is a directory"
        else:
            msg = "missing"
        raise ConfigException(
            f"Unexpected: Config dir lock file: {msg}. "
            f"The data directory {str(lock_file.parent)} might be owned by another app."
        )

    def copy_default_config(self, path: Path) -> None:
        """Copy the default config file to the given path."""
        logging.info(f"Copying default config file to: {str(path)}")
        default_config = importlib.resources.files(
            "vscode_cli_helpers.open_file.data"
        ).joinpath("default_config.ini")
        shutil.copyfile(str(default_config), str(path))

    def get_config_dir(self) -> Path:
        config_dir = platformdirs.user_config_dir(appname=self.appname)
        path = Path(config_dir)
        lock_file = path / self.dirlock_fn
        if path.exists():
            if path.is_file():
                raise ConfigException(
                    f"Config directory {str(path)} is file. Expected directory"
                )
            self.check_correct_config_dir(lock_file)
        else:
            path.mkdir(parents=True)
            with open(str(lock_file), "a", encoding="utf_8") as fp:
                fp.write(self.lockfile_string)
        return path

    def get_config_file(self) -> Path:
        return self.config_path

    def get_default_filename(self, template_name: str) -> str:
        if template_name in self.config["DefaultFilenames"]:
            return self.config["DefaultFilenames"][template_name]
        else:
            return self.config["Defaults"]["Filename"]

    def get_default_template_name(self) -> str:
        return self.config["Defaults"]["Template"]

    def get_template(self, language: str, version: int) -> str:
        path = self.get_template_path(language, version)
        logging.info(f"Reading {language} template from: {path}")
        with open(str(path), "r", encoding="utf_8") as fp:
            return fp.read()

    def get_template_path(self, language: Optional[str], version: int) -> Path:
        if language is None:
            language = self.get_default_template_name()
        dir_ = self.get_config_dir()
        template_dir = dir_ / "templates"
        if not template_dir.exists():
            template_dir.mkdir(parents=True)
        filename = f"{language}"
        if version > 1:
            filename += f"__{version}"
        path = template_dir / f"{filename}.txt"
        if not path.exists():
            template = ""
            if version > 1:
                logging.info(
                    f"No template file {filename}.txt found. Creating empty file."
                )
            else:
                logging.info(
                    f"No template found for {language}. Looking for a default template..."
                )
                def_path = importlib.resources.files(
                    "vscode_cli_helpers.open_file.data.templates"
                ).joinpath(f"{language}.txt")
                def_path = typing.cast(Path, def_path)
                if def_path.exists():
                    logging.info("Default template found. Using it.")
                    with open(str(def_path), "r", encoding="utf_8") as fp:
                        template = fp.read()
                else:
                    logging.info(
                        f"No default template found for {language}.."
                        f"Creating empty template."
                    )
            with open(path, "w", encoding="utf_8") as fp:
                fp.write(template)
        return path

    def get_template_extension(self, language: str) -> str:
        if language in self.config["FileExtensions"]:
            return self.config["FileExtensions"][language]
        else:
            if language in self.config["FileExtensionsAliases"]:
                language2 = self.config["FileExtensionsAliases"][language]
                return self.config["FileExtensions"][language2]
            else:
                raise ConfigException(
                    f"Could not find file extension for language: {language}"
                )

    def read_config(self) -> None:
        path = self.get_config_file()
        if path.exists():
            if not path.is_file():
                raise ConfigException(
                    f"Config filename {str(path)} exists, but filetype is not file"
                )
        else:
            self.copy_default_config(path)
        config = configparser.ConfigParser(
            # See https://stackoverflow.com/a/53274707/2173773
            converters={"list": lambda x: [i.strip() for i in x.split(",")]}
        )
        self.read_defaults(config)
        config.read(str(path))
        logging.info(f"Read config file: {str(path)}")
        self.config = config

    def read_defaults(self, config: ConfigParser) -> None:
        path = importlib.resources.files("vscode_cli_helpers.open_file.data").joinpath(
            "default_config.ini"
        )
        config.read(str(path))
