# -*- coding: utf-8 -*-

"""Installer for the MOPAC plug-in.

This handles any further installation needed after installing the Python
package `mopac-step`.
"""

import logging
from pathlib import Path
import pkg_resources
import subprocess

import seamm_installer

logger = logging.getLogger(__name__)


class Installer(seamm_installer.InstallerBase):
    """Handle further installation needed after installing mopac-step.

    The Python package `MOPAC-step` should already be installed, using `pip`,
    `conda`, or similar. This plug-in-specific installer then checks for the
    MOPAC executable, installing it if needed, and registers its
    location in seamm.ini.

    There are a number of ways to determine which are the correct MOPAC
    executables to use. The aim of this installer is to help the user locate
    the executables. There are a number of possibilities:

    #. The correct executables are already available.

        #. If they are already registered in `seamm.ini` there is nothing else
           to do.

        #. They may be in the current path, in which case they need to be added
           to `seamm.ini`.

        #. If a module system is in use, a module may need to be loaded to give
           access to MOPAC.

        #. They cannot be found automatically, so the user needs to locate the
           executables for the installer.

    #. MOPAC is not installed on the machine. In this case they can be
       installed in a Conda environment. There is one choice:

        #. They can be installed in a separate environment, `seamm-mopac` by
           default.
    """

    def __init__(self, logger=logger):
        # Call the base class initialization, which sets up the commandline
        # parser, amongst other things.
        super().__init__(logger=logger)

        logger.debug("Initializing the MOPAC installer object.")

        self.section = "mopac-step"
        self.executables = ["mopac"]
        self.resource_path = Path(pkg_resources.resource_filename(__name__, "data/"))

        # The environment.yaml file for Conda installations.
        logger.debug(f"data directory: {self.resource_path}")
        self.environment_file = self.resource_path / "seamm-mopac.yml"

    def check(self):
        """Check the status of the MOPAC installation."""
        print("Checking the MOPAC installation.")

        # What Conda environment is the default?
        path = self.configuration.path.parent / "mopac.ini"
        if not path.exists():
            text = (self.resource_path / "mopac.ini").read_text()
            path.write_text(text)
            print(f"    The mopac.ini file did not exist. Created {path}")

        self.exe_config.path = path

        # Get the current values
        data = self.exe_config.get_values("local")

        if "conda-environment" in data and data["conda-environment"] != "":
            self.environment = data["conda-environment"]
        else:
            self.environment = "seamm-mopac"

        super().check()

    def install(self):
        """Install MOPAC in a conda environment."""
        print("Installing MOPAC.")

        # What Conda environment is the default?
        path = self.configuration.path.parent / "mopac.ini"
        if not path.exists():
            text = (self.resource_path / "mopac.ini").read_text()
            path.write_text(text)
            print(f"    The mopac.ini file did not exist. Created {path}")

        self.exe_config.path = path

        # Get the current values
        data = self.exe_config.get_values("local")

        if "conda-environment" in data and data["conda-environment"] != "":
            self.environment = data["conda-environment"]
        else:
            self.environment = "seamm-mopac"

        super().install()

    def show(self):
        """Show the status of the MOPAC installation."""
        print("Showing the MOPAC installation.")

        # What Conda environment is the default?
        path = self.configuration.path.parent / "mopac.ini"
        if not path.exists():
            text = (self.resource_path / "mopac.ini").read_text()
            path.write_text(text)
            print(f"    The mopac.ini file does not exist at {path}")
            print("    The 'check' command will create it if MOPAC is installed.")
            print("    Otherwise 'install' will install MOPAC.")
            return

        self.exe_config.path = path

        if not self.exe_config.section_exists("local"):
            print(
                "    MOPAC is not configured: there is no 'local' section in "
                f"     {path}."
            )
            return

        # Get the current values
        data = self.exe_config.get_values("local")

        if "conda-environment" in data and data["conda-environment"] != "":
            self.environment = data["conda-environment"]
        else:
            self.environment = "seamm-mopac"

        super().show()

    def uninstall(self):
        """Uninstall the MOPAC installation."""
        print("Uninstall the MOPAC installation.")

        # What Conda environment is the default?
        path = self.configuration.path.parent / "mopac.ini"
        if not path.exists():
            text = (self.resource_path / "mopac.ini").read_text()
            path.write_text(text)
            print(
                f""""    The mopac.ini file does not exist at {path}
    Perhaps MOPAC is not installed, but if it is the 'check' command may locate it
    and create the ini file, after which 'uninstall' will remove it."""
            )
            return

        self.exe_config.path = path

        if not self.exe_config.section_exists("local"):
            print(
                f""""    The mopac.ini file at {path} does not have local section.
    Perhaps MOPAC is not installed, but if it is the 'check' command may locate it
    and update the ini file, after which 'uninstall' will remove it."""
            )
            return

        # Get the current values
        data = self.exe_config.get_values("local")

        if "conda-environment" in data and data["conda-environment"] != "":
            self.environment = data["conda-environment"]
        else:
            self.environment = "seamm-mopac"

        super().uninstall()

    def update(self):
        """Updates the MOPAC installation."""
        print("Updating the MOPAC installation.")

        # What Conda environment is the default?
        path = self.configuration.path.parent / "mopac.ini"
        if not path.exists():
            text = (self.resource_path / "mopac.ini").read_text()
            path.write_text(text)
            print(f"    The mopac.ini file did not exist. Created {path}")

        self.exe_config.path = path

        # Get the current values
        data = self.exe_config.get_values("local")

        if "conda-environment" in data and data["conda-environment"] != "":
            self.environment = data["conda-environment"]
        else:
            self.environment = "seamm-mopac"

        super().update()

    def exe_version(self, config):
        """Get the version of the MOPAC executable.

        Parameters
        ----------
        path : pathlib.Path
            Path to the executable.

        Returns
        -------
        str
            The version reported by the executable, or 'unknown'.
        """
        environment = config["conda-environment"]
        conda = config["conda"]
        if environment[0] == "~":
            environment = str(Path(environment).expanduser())
            command = f"'{conda}' run --live-stream -p '{environment}' mopac --version"
        elif Path(environment).is_absolute():
            command = f"'{conda}' run --live-stream -p '{environment}' mopac --version"
        else:
            command = f"'{conda}' run --live-stream -n '{environment}' mopac --version"

        logger.debug(f"    Running {command}")
        try:
            result = subprocess.run(
                command,
                stdin=subprocess.DEVNULL,
                capture_output=True,
                text=True,
                shell=True,
            )
        except Exception as e:
            logger.debug(f"    Failed to run {command}: {e}")
            version = "unknown"
        else:
            logger.debug(f"    {result.stdout}")
            version = "unknown"
            lines = result.stdout.splitlines()
            for line in lines:
                line = line.strip()
                tmp = line.split()
                if len(tmp) >= 2:
                    version = tmp[2]
                    break

        return "MOPAC", version
