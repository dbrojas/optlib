from optlib.gbs import american


class Option:

    def __init__(self, option_type, fs, x, t, v):
        self.option_type = option_type
        self.fs = fs
        self.x = x
        self.t = t
        self.v = v

    def __repr__(self):
        raise NotImplementedError


class AmericanOption(Option):

    def __init__(self, *args, **kwargs):
        super().__init__(self, *args, **kwargs)

    @property
    def price(self):
        raise NotImplementedError

    @property
    def greeks(self)
        raise NotImplementedError
