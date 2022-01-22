import fuzzingbook.ConcolicFuzzer
from RandomConcolicTracer import RandomConcolicTracer # use this in project
#from RandomConcolicTracer_solution import RandomConcolicTracer # during developiment
import time
import random
import z3

from samples.triangle import triangle
from samples.string_cmp import string_cmp_test
from samples.arithmetic import arithmetic_test

def benchmark(f, args):
    print('[*] Running benchmark for function', f.__name__)

    with RandomConcolicTracer() as _:
        _[f](*args)
    
    # Negate last path constraint
    new_path = _.path[0:-1] + [z3.Not(_.path[-1])]
    new_ = RandomConcolicTracer((_.decls, new_path))
    new_.fn = _.fn
    new_.fn_args = _.fn_args
    
    # Measure zeval
    start = time.time()
    zeval_result = new_.zeval()
    end = time.time()
    print('[zeval] result: ', zeval_result)
    print('[zeval] time: ', end-start)

    # Measure reval
    start = time.time()
    reval_result = new_.reval(attempts=10000)
    end = time.time()
    print('[reval] result: ', reval_result)
    print('[reval] time: ', end-start)

    return zeval_result[0] == 'sat' and reval_result[0] == 'sat'

def main():
    random.seed(0)

    fuzzingbook.ConcolicFuzzer.initialize() # Don't change me!

    assert benchmark(triangle, (1,2,3)), 'Benchmark 1 failed'
    print('Benchmark 1 passed')
    print()

    assert benchmark(string_cmp_test, ('hey')), 'Benchmark 2 failed'
    print('Benchmark 2 passed')
    print()

    assert benchmark(arithmetic_test, (1,2)), 'Benchmark 3 failed'
    print('Benchmark 3 passed')
    print()


if __name__ == "__main__":
    main()
