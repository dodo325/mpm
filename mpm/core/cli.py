from mpm.core.configs import get_scripts, get_known_packages, update_user_known_package
from mpm.core.logging import getLogger, logging
from mpm.pm import (
    Package,
    UniversalePackage,
    NAMES_TO_PACKAGE_MANAGERS,
    PACKAGE_MANAGERS_NAMES,
    get_installed_pms,
)
from mpm.shell import AutoShell
import json
from plumbum import cli
from rich.console import Console
from rich.table import Table
from rich import box
from rich.prompt import Prompt
from rich.syntax import Syntax
from rich.traceback import install
from rich import print, pretty
console = Console()

logger = getLogger(__name__)

from mpm.__init__ import __version__ as version_str

def print_info(info: dict()):
    for pm_name, data in info.items():
        table = Table(title=pm_name, box=box.ROUNDED)

        table.add_column("Field name", justify="right", style="cyan")
        table.add_column("Data", justify="left", style="deep_sky_blue3")
        for field_name, field_data in data.items():
            table.add_row(str(field_name), str(field_data))
        console.print(table)

class MainMixin():
    offline = cli.Flag(
        ["off", "offline"], help="Search for information not only in local the known_packages")
    all_flag = cli.Flag(
        ["a", "all"], help="Search for information not only the known_packages")
    quiet = cli.Flag(
        ["q", "quiet"], help="Disable Logging")

    pm_names = []

    @cli.switch("--pm", str, list=True, help="Search in Package Manager: " + str(PACKAGE_MANAGERS_NAMES))
    def pms(self, PM_names):
        for pm in PM_names:
            if pm not in PACKAGE_MANAGERS_NAMES:
                try:
                    raise ValueError(f"\"{pm}\" not found in known Package Managers")
                except:
                    console.print_exception()
                    exit()
        self.pm_names = PM_names

    known_packages = cli.SwitchAttr(
        ["k", "package-manager"], cli.ExistingFile, help="known_packages.json file")

class Main(cli.Application):
    PROGNAME = "mpm"
    VERSION = version_str
    

@Main.subcommand("info")
class Info(cli.Application, MainMixin):
    """
    Показать дополнительные данные о пакете
    """

    def main(self, package_name):
        pretty.install()
        install()
        if self.quiet:
            logging.disable(logging.CRITICAL)

        logger.debug(
            f"Args:\n\tpackage_name = {package_name},\n\tpm_names = {self.pm_names}\n\tall = {self.all_flag}\n\toffline = {self.offline}"
        )
        known_packages = get_known_packages(offline=self.offline)
        if self.known_packages:
            known_packages.update(json.load(self.known_packages))

        shell = AutoShell()
        PMs = get_installed_pms(shell=shell)
        if len(self.pm_names) > 0:
            def pm_fliter(PM): return PM.name in self.pm_names
            PMs = list(filter(pm_fliter, PMs))
            logger.debug(f"PMs after filtering: {PMs}")

        package = UniversalePackage(
            package_name, shell=shell, pms_classes=PMs, known_packages=known_packages
        )

        info = package.get_info(all_pm=self.all_flag)
        if info == {}:
            logger.error("Package Does Not Found")
            return

        print_info(info)
        if package_name not in known_packages:
            update_user_known_package(package_name, package.config)


def main():
    Main.run()

if __name__ == '__main__':
    main()
