"""The left_join command."""

from json import dumps

from .base import Base
from operator import itemgetter
from jtools.utilities.json_utils import left_join as left_join_


class LeftJoin(Base):
    """Left join files of JSON objects"""

    def run(self):
        is_primary_key = True
        key = self.options['--pkey']
        if key is None:
            key = self.options['--key']
            if key is None:
                raise ValueError('Must provide either --pkey or --key for a left join')
            is_primary_key = False
        for row in left_join_(itemgetter(key), file_paths=self.options['<file>'], exclude_columns=[key],
                              is_primary_key=is_primary_key).rows():
            print dumps(row, sort_keys=True)
