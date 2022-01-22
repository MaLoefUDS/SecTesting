import z3
from fuzzingbook.ConcolicFuzzer import ConcolicTracer
from RandomGeneration import random_int, random_string

def Not(x: bool):
    return not x

class RandomConcolicTracer(ConcolicTracer):
    def reval(self, attempts: int):
        assert attempts > 0
        return 'unsat', {}
        # TODO: Implement me
