import z3
from fuzzingbook.ConcolicFuzzer import ConcolicTracer
from RandomGeneration import random_int, random_string

def Not(x: bool):
    return not x

class RandomConcolicTracer(ConcolicTracer):
    def reval(self, attempts: int):
        assert attempts > 0
        for _ in range(attempts):
            env = dict()
            for key in self.decls.keys():
                value = random_int() if self.decls[key] == "Int" else random_string()
                locals()[key] = value
                env[key] = value, self.decls[key]
            sat = True
            for statement in self.path:
                sat = sat and eval(f"{statement}")
            if sat:
                return "sat", env
        return 'unsat', {}
