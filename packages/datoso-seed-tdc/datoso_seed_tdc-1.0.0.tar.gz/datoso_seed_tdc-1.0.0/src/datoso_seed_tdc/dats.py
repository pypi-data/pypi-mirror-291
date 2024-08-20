"""TDC Dat class."""
from datoso.repositories.dat_file import DOSCenterDatFile


class TdcDat(DOSCenterDatFile):
    """TDC Dat class."""

    seed: str = 'tdc'

    def initial_parse(self) -> list:
        """Parse the dat file."""
        # pylint: disable=R0801
        self.company = 'IBM'
        self.system = 'PC and Compatibles'
        self.suffix = 'Total DOS Collection'
        self.date = self.get_date()
        self.full_name = self.name + ' - ' + self.full_name
        self.prefix = 'Computer'
        self.system_type = 'Computer'

        return [self.prefix, self.company, self.system, self.suffix, self.get_date()]


    def get_date(self) -> str:
        """Get the date from the dat file."""
        return self.header['date']
