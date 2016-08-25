"""
Join any number of flat record JSON tables together via composition.
"""
import copy
import json


class Table(object):

    def __init__(self, table, primary_key=None):
        """
         Create a new Table

        :param table: A JSON string with a list of records (keyed on "rec") or a dict of records keyed on the primary key
        :param primary_key: If table is a JSON string, use this attribute as the primary key
        """
        if primary_key is None:
            self.table_ = table
        else:
            self.table_ = {}
            tbl = json.loads(table) if isinstance(table, basestring) else table
            for row in tbl['recs']:
                pkey = row[primary_key]
                if pkey in self.table_:
                    raise KeyError('Primary key: "' + pkey + '" is not unique')
                else:
                    self.table_[pkey] = row

    def join(self, table):
        """
        Creates a new joined table.

        :param table: The table to join to
        :return: A new joined table
        """
        result = copy.deepcopy(self.table_)
        for key, row in result.iteritems():
            try:
                # Merge the dict if there is a match
                row.update(table.table_[key])
            except:
                # If there isn't a match, do nothing
                pass
        # Return a new copy of the joined result
        return Table(result)

    def rows(self):
        """
        Generate rows in this table

        :return: an iterator to the rows in this table (like a cursor)
        """
        for row in self.table_.itervalues():
            yield row


def test():
    stream1 = '''
    {"recs": [{
        "Decimal": "1469119904.875811",
        "Example_Dictionary": "Example_1",
        "Literal_1": "Example",
        "Number": "26809",
        "NumberExample": "0     0     1    0",
        "SN": "18",
        "Sequence_1": "Example    1469119904.875811   Example_1        18      26809        0    0     1     0",
        "input_record_label": "hdfs://foo.foobar.us.ibm.com:8020/mydata/JOEL_101_DAVIN_102/2016_08_02/JOEL101-DAVIN102-somethinghere-2016-07-21_Data.log"
      },
      {
        "Decimal": "1469119904.875812",
        "Example_Dictionary": "Example_2",
        "Literal_1": "Example2",
        "Number": "26810",
        "NumberExample": "0     0     1    0",
        "SN": "19",
        "Sequence_1": "Example    1469119904.875812   Example_2        19      26810        0    0     1     0",
        "input_record_label": "hdfs://foo.foobar.us.ibm.com:8020/mydata/JOEL_101_DAVIN_102/2016_08_02/JOEL101-DAVIN102-somethinghere2-2016-07-21_Data.log"
      }
    ]}
    '''

    stream2 = '''
    {"recs":[{
        "additional_attribute_1": "one",
        "additional_attribute_2": 2,
        "additional_attribute_3": 3.1000000000000001,
        "input_record_label": "hdfs://foo.foobar.us.ibm.com:8020/mydata/JOEL_101_DAVIN_102/2016_08_02/JOEL101-DAVIN102-somethinghere-2016-07-21_Data.log"
      }
    ]}
    '''

    joinedTable = Table(stream1, 'input_record_label').join(Table(stream2, 'input_record_label'))
    print json.dumps({'recs': list(joinedTable.rows())}, indent=2, sort_keys=True)

if __name__ == '__main__':
    test()
