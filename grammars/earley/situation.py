class EarleySituation:

    start: str
    target: str

    h: int
    i: int
    p: int  # Dot position

    def __init__(self, start: str, target: str, h: int, i: int, p: int):
        self.start = start
        self.target = target

        self.h = h
        self.i = i
        self.p = p

    def __repr__(self):
        return f"{self.start}🠖{self.target[:self.p]}⚫{self.target[self.p:]} [{self.h}, {self.i}]"

    def __key(self):
        return self.start, self.target, self.h, self.i, self.p

    def __hash__(self):
        return hash(self.__key())

    def __eq__(self, other):
        if isinstance(other, EarleySituation):
            return self.__key() == other.__key()
        return NotImplemented
