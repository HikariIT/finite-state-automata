from copy import deepcopy
from typing import Set, Dict

from grammars.earley.situation import EarleySituation
from grammars.grammar import Grammar


class Earley:
    grammar: Grammar
    word: str

    situations: Set[EarleySituation]
    processed: Dict[int, Set[EarleySituation]]

    def __init__(self, grammar: Grammar):
        self.grammar = deepcopy(grammar)
        self.grammar.fix_starting_state()
        self.situations = set()
        self.processed = {}

    def word_in_grammar(self, word: str):
        self.word = word

        self.situations = {EarleySituation(self.grammar.start_symbol, self.grammar.start_symbol[0], 0, 0, 0)}
        self.processed = {}

        while len(self.situations) > 0:
            situation = self.situations.pop()
            if self.situation_processed(situation):
                continue

            if len(situation.target) == situation.p:
                self.completion(situation)
            elif self.grammar.is_non_terminal(situation.target[situation.p]):
                self.prediction(situation)
            elif situation.i < len(word) and situation.target[situation.p] == self.word[situation.i]:
                self.scanning(situation)

            self.add_situation_to_processed(situation)
            self.print_processed()

        return len(word) in self.processed and EarleySituation(self.grammar.start_symbol, self.grammar.start_symbol[0],
                                                               0, len(word), 1) in self.processed[len(word)]

    def prediction(self, situation: EarleySituation):
        non_terminal = situation.target[situation.p]
        for rule in self.grammar.productions.get_productions_for_symbol(non_terminal):
            self.situations.add(EarleySituation(rule.start, rule.target, situation.i, situation.i, 0))

    def completion(self, situation: EarleySituation):
        for pr_situation in self.processed[situation.h]:
            if pr_situation.target[pr_situation.p] == situation.start:
                self.situations.add(EarleySituation(pr_situation.start, pr_situation.target,
                                                    pr_situation.h, situation.i, pr_situation.p + 1))
        pass

    def scanning(self, situation):
        symbol = situation.target[situation.p]
        self.situations.add(
            EarleySituation(situation.start, situation.target, situation.h, situation.i + 1, situation.p + 1))
        pass

    def add_situation_to_processed(self, situation: EarleySituation):
        if situation.i not in self.processed:
            self.processed[situation.i] = {situation}
        else:
            self.processed[situation.i].add(situation)

    def situation_processed(self, situation: EarleySituation) -> bool:
        if situation.i not in self.processed:
            return False
        return situation in self.processed[situation.i]

    def print_processed(self):
        print("----------------------------------------------------------------")
        for key, value in self.processed.items():
            print(f"{key}: {value}")
        print("----------------------------------------------------------------")
