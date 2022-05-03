class Round:
    def __init__(self, name, start, end):
        self._name = name
        self._start = start
        self._end = end

    @property
    def name(self):
        return self._name

    @property
    def start(self):
        return self._start

    @property
    def end(self):
        return self._end

    def during_round(self, a_date):
        return a_date >= self._start and a_date <= self._end
