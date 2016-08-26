class Table(object):
    def __init__(self, table, primary_key_function=None):
        """
         Create a new Table

        :param table: A list of dicts representing table rows
        :param primary_key_function: Use this column as the primary key
        """
        if primary_key_function is None:
            self.table_ = table
        else:
            self.table_ = {}
            self.primary_key_function = primary_key_function
            for row in table:
                matching_key = self.primary_key_function(row)
                # Ensure that the matching key is unique for this table (can be used as a primary key)
                if matching_key in self.table_:
                    raise KeyError('Primary key "' + matching_key + '" is not unique')
                else:
                    self.table_[matching_key] = row

    def left_join(self, right_side_table, exclude_columns=None, updateable=False):
        """
        Creates a new left joined table.

        :param right_side_table: The right-side table to join to
        :param exclude_columns: Do not join in these columns from the given right-side table
        :param updateable: If there are columns in the right-side table that match the left-side table , should they \
        be updated.  If there are columns in the right-side table that match the left-side table and updating is not \
        desired, a KeyError will be raised.
        :return: A new joined table
        """
        result = self.table_.copy()
        for key, row in result.iteritems():
            try:
                row_to_merge = right_side_table.table_[key]
            except:
                # no match found
                continue
            # Merge the dict if there is a match
            if exclude_columns:
                row_to_merge = dict((k, v) for k, v in row_to_merge.items() if k not in exclude_columns)
            if not updateable:
                for k in row_to_merge.iterkeys():
                    if k in row:
                        raise KeyError('Column "' + k + '" is already in this table')

            row.update(row_to_merge)

        # Return a new copy of the joined result
        return Table(result)

    def rows(self):
        """
        Generate rows in this table

        :return: an iterator to the rows in this table (like a cursor)
        """
        for row in self.table_.itervalues():
            yield row

