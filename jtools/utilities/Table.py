"""
A table object
"""


class Table(object):
    def __init__(self, table, key_function=None, is_primary_key=True):
        """
         Create a new Table

        :param table: A list of dicts representing table rows
        :param key_function: Use the result of this function in a row as the key
        :param is_primary_key: True when keys are to be unique and False otherwise
        """
        self.is_primary_key_ = is_primary_key
        if key_function is None:
            self.table_ = table
        else:
            self.table_ = {}
            self.key_function = key_function
            for row in table:
                matching_key = self.key_function(row)
                # Ensure that the matching key is unique for this table (can be used as a primary key)
                if matching_key in self.table_:
                    if is_primary_key:
                        raise KeyError('Primary key "' + matching_key + '" is not unique')
                    else:
                        self.table_[matching_key].append(row)
                else:
                    self.table_[matching_key] = [row]

    def row_join(self, row, matching_key, pass_through=True, exclude_columns=None, updateable=False):
        """
        Join in matching columns into the given row.

        :param row: A row to add matching columns to
        :param matching_key: The key to match on
        :param pass_through: If there is no match, should the row pass through (if True) or should None be returned (if False)
        :param exclude_columns: Matching columns to exclude
        :param updateable: If there are columns in the table that match the columns in the row, should they be updated
        :return: A new joined row or None if no match was found and pass_through is False
        """
        if not self.is_primary_key_:
            raise KeyError('Cannot do a row join on a table whose keys are not primary keys')
        result = row.copy()
        try:
            row_to_merge = self.table_[matching_key][0]
            if exclude_columns:
                row_to_merge = dict((k, v) for k, v in row_to_merge.items() if k not in exclude_columns)
            if not updateable:
                for k in row_to_merge.iterkeys():
                    if k in row:
                        raise KeyError('Column "' + k + '" is already in this row')

            result.update(row_to_merge)
        except:
            # no match found
            if not pass_through:
                return None
        return result

    def left_join(self, right_side_table, exclude_columns=None, updateable=False):
        """
        Creates a new left joined table.

        :param right_side_table: The right-side table to join to (its keys must be unique)
        :param exclude_columns: Do not join in these columns from the given right-side table
        :param updateable: If there are columns in the right-side table that match the left-side table , should they \
        be updated.  If there are columns in the right-side table that match the left-side table and updating is not \
        desired, a KeyError will be raised.
        :return: A new joined table
        """
        if not right_side_table.is_primary_key_:
            raise KeyError('Cannot do a left_join on a right-side table whose keys are not unique')
        result = self.table_.copy()
        for key, rows in result.iteritems():
            for row in rows:
                try:
                    row_to_merge = right_side_table.table_[key][0]
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
        for rows in self.table_.itervalues():
            for row in rows:
                yield row

