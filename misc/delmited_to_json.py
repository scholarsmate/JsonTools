import json


def generate_records(column_defs, rows):
    """
    Given a column specification and an rows iterable, generate records (set of key/value pairs)

    :param column_defs: Set of column names
    :param rows: rows iterable
    :return: a generated record
    """
    num_cols = len(column_defs)
    for row in rows:
        record = {}
        for i in range(0, num_cols):
            record[column_defs[i]] = row[i]
        yield record


# For generating some dummy row data
def generate_rows(num_cols, num_rows):
    for i in range(0, num_rows):
        row = []
        for j in range(0, num_cols):
            row.append("val%d.%d" % (i, j))
        yield row


def test_delimited_to_json(num_cols, num_rows):
    # Generate a dummy column spec
    column_defs = ["col%d" % i for i in range(0, num_cols)]
    for record in generate_records(column_defs, generate_rows(num_cols, num_rows)):
        print json.dumps(record)


if __name__ == "__main__":
    test_delimited_to_json(10, 20)
