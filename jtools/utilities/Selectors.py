"""
Common selector functors
"""


class ToUpperSelector(object):
    def __init__(self, select_function):
        self.select_function_ = select_function

    def __call__(self, obj):
        return self.select_function_(obj).upper()


class ToLowerSelector(object):
    def __init__(self, select_function):
        self.select_function_ = select_function

    def __call__(self, obj):
        return self.select_function_(obj).lower()
