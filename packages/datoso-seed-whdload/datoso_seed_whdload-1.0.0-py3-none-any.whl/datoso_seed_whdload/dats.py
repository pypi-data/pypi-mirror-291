"""WhdloadDat class to parse different types of dat files."""

import re

from datoso.repositories.dat_file import ClrMameProDatFile


class WhdloadDat(ClrMameProDatFile):
    """Whdload Dat class."""

    seed: str = 'Whdload'

    def initial_parse(self) -> list:
        """Parse the dat file."""
        # pylint: disable=R0801
        system, suffix1, suffix2 = self.name.split(' - ')
        self.prefix = 'Computer'
        self.company, self.system = system.split(' ')
        self.suffix = [suffix1, suffix2]
        self.date = ''
        return [self.prefix, self.company, self.system, self.suffix, self.get_date()]

    def get_date(self) -> str:
        """Get the date from the dat file."""
        if self.date:
            return self.date
        if self.version:
            result = re.findall(r'\(.*?\)', str(self.version))
            self.date = result[len(result)-1][1:-1].replace('_CM','')
        if self.file:
            result = re.findall(r'\(.*?\)', str(self.file))
            self.date = result[len(result)-1][1:-1].replace('_CM','')
        return self.date
