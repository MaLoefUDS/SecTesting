import random
import fuzzingbook.ConcolicFuzzer
#import Summaries_Solution as Summaries # During development
import Summaries
from fuzzingbook.ConcolicFuzzer import SimpleConcolicFuzzer, ConcolicTracer, ExpectError
from EMail import check_mail
import json

def main():
    random.seed(0)
    fuzzingbook.ConcolicFuzzer.initialize()
    Summaries.setup_summary()
    inputs = []

    scf = SimpleConcolicFuzzer()
    for i in range(200):
        v = scf.fuzz()
        hex = ":".join("{:02x}".format(ord(c)) for c in v)
        inputs.append(hex)
        print('Generated input: >>{}<<'.format(hex))
        print(repr(v))
        if v is None:
            continue
        with ConcolicTracer() as _:
            with ExpectError(print_traceback=True):
                _[check_mail](v)
        scf.add_trace(_, v)
        print()
        print()

    print('Serializing inputs to inputs.json')
    with open('inputs.json', 'w') as f:
        json.dump(inputs, f)


if __name__ == "__main__":
    main()
