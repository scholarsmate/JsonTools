"""
Join any number of flat record JSON tables together via composition.
"""
import json
from operator import itemgetter

from jtools.utilities.Selectors import ToUpperSelector
from jtools.utilities.json_utils import left_join


def test():
    for row in left_join(ToUpperSelector(itemgetter('pkey')),
                         ['test/Samples/Sample_1.txt',
                          'test/Samples/Sample_2.txt',
                          'test/Samples/Sample_3.txt',
                          'test/Samples/Sample_4.txt'],
                         exclude_columns=['pkey']).rows():
        print json.dumps(row, sort_keys=True)


if __name__ == '__main__':
    test()
