"""The left_join command."""

from json import dumps

from .base import Base
from operator import itemgetter
from jtools.utilities.json_utils import left_join


class LeftJoin(Base):
    """Left join files of JSON objects"""

    def run(self):
        pkey = self.options['--pkey']
        for row in left_join(itemgetter(pkey), file_paths=self.options['<file>'], exclude_columns=[pkey]).rows():
            print dumps(row, sort_keys=True)
