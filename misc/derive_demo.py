"""
Demo functors
"""

class Sequence(object):
    def __init__(self, field, start=1, step=1):
        self.name_ = field
        self.start_ = start
        self.step_ = step

    def __call__(self, record):
        record[self.name_] = self.start_
        self.start_ += self.step_
        return record


class MD5(object):
    def __init__(self, field='md5'):
        self._col = field
        pass

    def __call__(self, record):
        import hashlib
        m = hashlib.md5()
        for k, v in record.items():
            m.update(k)
            m.update('\0')
            m.update(v)
            m.update('\0')
        record[self._col] = m.hexdigest()
        return record


class EmitJson(object):
    def __init__(self, sink):
        self.sink_ = sink

    def __call__(self, record):
        import json
        print >>self.sink_, json.dumps(record)
        return record


def visit(records, function):
    for record in records:
        yield function(record)


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


if __name__ == "__main__":
    import sys
    cols = 5
    rows = 10
    column_defs = ["col%d" % i for i in range(0, cols)]
    for i in visit(visit(visit(generate_records(column_defs,generate_rows(len(column_defs), rows)), MD5()),
                         Sequence('id')), EmitJson(sys.stdout)):
        pass
