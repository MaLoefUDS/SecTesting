import os
import inspect

PRINT_FORMAT = '{:<40}{}'
CORRECT_STATE = 'PASS'
WRONG_STATE = 'FAIL'

files_to_verify = [
    os.path.join('Task1', 'RandomConcolicTracer.py'),
    os.path.join('Task1', 'RandomGeneration.py'),
    os.path.join('Task1', 'Benchmark.py'),
    os.path.join('Task1', 'benchmark_results.txt'),

    os.path.join('Task2', 'Summaries.py'),
    os.path.join('Task2', 'TestSummaries.py'),
    os.path.join('Task2', 'EMail.py'),
    os.path.join('Task2', 'RunInputs.py'),
    os.path.join('Task2', 'ConcolicEMailExploration.py')
]

def verify_files():
    missing_files = list()
    for path in files_to_verify:
        if os.path.exists(path):
            state = CORRECT_STATE
        else:
            missing_files.append(path)
            state = WRONG_STATE
        print(PRINT_FORMAT.format(path, state))
    print()
    return missing_files

class VerificationError(ValueError):
    pass

if __name__ == '__main__':
    missing_files = verify_files()
    for l, m in [(missing_files, 'Missing file')]:
        for v in l:
            print(f'{m}: {v}')
        if l:
            print()
    if missing_files:
        raise VerificationError()
