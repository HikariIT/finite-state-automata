class State:

    name: str
    is_starting: bool
    is_accepting: bool

    def __init__(self, name: str, is_starting: bool, is_accepting: bool):
        self.name = name
        self.is_starting = is_starting
        self.is_accepting = is_accepting

    def __str__(self):
        ret = self.name
        if self.is_starting:
            ret = ">" + ret
        if self.is_accepting:
            ret = ret + "*"
        return ret

    def __repr__(self):
        return str(self)
