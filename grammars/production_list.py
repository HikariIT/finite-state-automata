import re
from typing import List


class ProductionRule:

    SPLIT_REGEX: str = r"->|🠖"
    start: str
    target: str

    def __init__(self, start, target):
        self.start = start
        self.target = target

    def __repr__(self):
        return f"{self.start}🠖{self.target}"

    @staticmethod
    def from_str(production_text: str) -> List["ProductionRule"]:
        split = re.split(ProductionRule.SPLIT_REGEX, production_text)
        stripped = [el.strip() for el in split]
        if len(stripped) < 2:
            raise Exception()

        split_right = stripped[1].split('|')
        stripped_right = [el.strip() for el in split_right]

        return [ProductionRule(stripped[0], right_side) for right_side in stripped_right]


class ProductionList:

    productions: List[ProductionRule]

    def __init__(self):
        self.productions = []

    def add_productions(self, productions: List[ProductionRule]):
        self.productions.extend(productions)

    def get_productions_for_symbol(self, symbol: str) -> List[ProductionRule]:
        return list(filter(lambda prod: prod.start == symbol, self.productions))

    @staticmethod
    def productions_from_str(production_text: str) -> "ProductionList":
        production_list = ProductionList()
        for line in production_text.splitlines():
            try:
                production_list.add_productions(ProductionRule.from_str(line))
            except Exception:
                pass
        return production_list

    def __repr__(self):
        return ", ".join([repr(prod) for prod in self.productions])