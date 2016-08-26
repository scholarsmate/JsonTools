import operator


def test(d, ks):
    return ks(d)

d = {'key': "foo", 'val':'val1'}
ks = operator.itemgetter('key')
print test(d, ks)
