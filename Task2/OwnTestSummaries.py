import random

import fuzzingbook.ConcolicFuzzer
import z3
from fuzzingbook.ConcolicFuzzer import ConcolicTracer

import Summaries  # In final project
from summary_samples.string_endswith import *


# import Summaries_Solution as Summaries # For testing during development


def test_summary_endswith():
    print('[*] Testing the function summary for endswith')

    with ConcolicTracer() as _:
        #_[string_startswith_test]('Hello')
        _[string_endswith_test]('Hello Detlef du Banana')

    print(f"{_.path=}")
    new_path = _.path[0:-1] + [z3.Not(_.path[-1])]
    print("-" * 50)

    print(f"{new_path=}")
    new_ = ConcolicTracer((_.decls, new_path))
    new_.fn = _.fn
    new_.fn_args = _.fn_args

    result = new_.zeval()
    print(result)
    if result[0] == 'sat' and result[1]['x'][0].endswith('World'):
        return True
    return False


summary_dict = {
    'endswith': test_summary_endswith
}


def main():
    random.seed(0)
    fuzzingbook.ConcolicFuzzer.initialize()
    Summaries.setup_summary()

    passed = 0
    for name, f in summary_dict.items():
        try:
            success = f()
            if success:
                print('Summary for {} passed'.format(name))
                passed += 1
            else:
                print('Summary for {} did not pass'.format(name))
        except Exception as e:
            print('Summary for {} failed: {}'.format(name, str(e)))

        print()

    print()
    print('Done.')
    print('Passed {:d}/{:d}.'.format(passed, len(summary_dict)))


if __name__ == "__main__":
    main()
