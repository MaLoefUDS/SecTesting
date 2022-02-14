import random
import z3

import fuzzingbook.ConcolicFuzzer
from fuzzingbook.ConcolicFuzzer import ConcolicTracer

import Summaries # In final project
#import Summaries_Solution as Summaries # For testing during development

from summary_samples.int_abs import int_abs_test

from summary_samples.string_isalnum import string_isalnum_test
from summary_samples.string_isdecimal import string_isdecimal_test
from summary_samples.string_isdigit import string_isdigit_test
from summary_samples.string_islower import string_islower_test
from summary_samples.string_isnumeric import string_isnumeric_test
from summary_samples.string_isprintable import string_isprintable_test
from summary_samples.string_isspace import string_isspace_test

from summary_samples.string_swapcase import string_swapcase_test
from summary_samples.string_title import string_title_test
from summary_samples.string_capitalize import string_capitalize_test
from summary_samples.string_rfind import string_rfind_test



def test_summary_abs():
    print('[*] Testing the function summary for __abs__ (int)')

    with ConcolicTracer() as _:
        _[int_abs_test](-123, 456)
    
    new_path = _.path[0:-1] + [z3.Not(_.path[-1])]
    new_ = ConcolicTracer((_.decls, new_path))
    new_.fn = _.fn
    new_.fn_args = _.fn_args
    result = new_.zeval()

    #Solutions as int:
    x = int(''.join(result[1]['x'][0]))
    y = int(''.join(result[1]['y'][0]))

    if result[0] == 'sat' and x != 0 and y != 0 and x+y==0: # due to previous path constraints, x and y cannot be 0.
        return True
    return False

def test_summary_isalnum():
    print('[*] Testing the function summary for isalnum')

    with ConcolicTracer() as _:
        _[string_isalnum_test]('??')
    
    new_path = _.path[0:-1] + [z3.Not(_.path[-1])]
    new_ = ConcolicTracer((_.decls, new_path))
    new_.fn = _.fn
    new_.fn_args = _.fn_args

    result = new_.zeval()
    if result[0] == 'sat' and result[1]['x'][0].isalnum():
        return True
    return False

def test_summary_isdecimal():
    print('[*] Testing the function summary for isdecimal')

    with ConcolicTracer() as _:
        _[string_isdecimal_test]('qqq')
    
    new_path = _.path[0:-1] + [z3.Not(_.path[-1])]
    new_ = ConcolicTracer((_.decls, new_path))
    new_.fn = _.fn
    new_.fn_args = _.fn_args

    result = new_.zeval()
    if result[0] == 'sat' and result[1]['x'][0].isdecimal():
        return True
    return False

def test_summary_isdigit():
    print('[*] Testing the function summary for isdigit')

    with ConcolicTracer() as _:
        _[string_isdigit_test]('qqq')
    
    new_path = _.path[0:-1] + [z3.Not(_.path[-1])]
    new_ = ConcolicTracer((_.decls, new_path))
    new_.fn = _.fn
    new_.fn_args = _.fn_args

    result = new_.zeval()
    if result[0] == 'sat' and result[1]['x'][0].isdigit():
        return True
    return False

def test_summary_islower():
    print('[*] Testing the function summary for islower')

    with ConcolicTracer() as _:
        _[string_islower_test]('ABC')
    
    new_path = _.path[0:-1] + [z3.Not(_.path[-1])]
    new_ = ConcolicTracer((_.decls, new_path))
    new_.fn = _.fn
    new_.fn_args = _.fn_args

    result = new_.zeval()
    if result[0] == 'sat' and result[1]['x'][0].islower():
        return True
    return False

def test_summary_isnumeric():
    print('[*] Testing the function summary for isnumeric')

    with ConcolicTracer() as _:
        _[string_isnumeric_test]('ABC')
    
    new_path = _.path[0:-1] + [z3.Not(_.path[-1])]
    new_ = ConcolicTracer((_.decls, new_path))
    new_.fn = _.fn
    new_.fn_args = _.fn_args

    result = new_.zeval()
    if result[0] == 'sat' and result[1]['x'][0].isnumeric():
        return True
    return False

def test_summary_isprintable():
    print('[*] Testing the function summary for isprintable')

    with ConcolicTracer() as _:
        _[string_isprintable_test]('\x01')
    
    new_path = _.path[0:-1] + [z3.Not(_.path[-1])]
    new_ = ConcolicTracer((_.decls, new_path))
    new_.fn = _.fn
    new_.fn_args = _.fn_args

    result = new_.zeval()
    if result[0] == 'sat' and result[1]['x'][0].isprintable():
        return True
    return False

def reformat_utf(s):
    import re
    return re.sub(r'\\u\{([0-9a-fA-F]{1,4})\}', lambda x: chr(int(x.group(1), 16)), s)

def test_summary_isspace():
    print('[*] Testing the function summary for isspace')

    with ConcolicTracer() as _:
        _[string_isspace_test]('Aa')
    
    new_path = _.path[0:-1] + [z3.Not(_.path[-1])]
    new_ = ConcolicTracer((_.decls, new_path))
    new_.fn = _.fn
    new_.fn_args = _.fn_args

    result = new_.zeval()
    print(result)
    if result[0] == 'sat' and reformat_utf(result[1]['x'][0]).isspace():
        return True
    return False


def test_summary_swapcase():
    print('[*] Testing the function summary for swapcase')

    with ConcolicTracer() as _:
        _[string_swapcase_test]('AaBb')
    
    new_path = _.path[0:-1] + [z3.Not(_.path[-1])]
    new_ = ConcolicTracer((_.decls, new_path))
    new_.fn = _.fn
    new_.fn_args = _.fn_args

    result = new_.zeval()
    if result[0] == 'sat' and result[1]['x'][0] == 'aAbB':
        return True
    return False

def test_summary_title():
    print('[*] Testing the function summary for title')

    with ConcolicTracer() as _:
        _[string_title_test]('Hello world')
    
    new_path = _.path[0:-1] + [z3.Not(_.path[-1])]
    new_ = ConcolicTracer((_.decls, new_path))
    new_.fn = _.fn
    new_.fn_args = _.fn_args

    result = new_.zeval()
    if result[0] == 'sat' and result[1]['x'][0] == 'Hello World':
        return True
    return False


def test_summary_capitalize():
    print('[*] Testing the function summary for capitalize')

    with ConcolicTracer() as _:
        _[string_capitalize_test]('solution')
    
    new_path = _.path[0:-1] + [z3.Not(_.path[-1])]
    new_ = ConcolicTracer((_.decls, new_path))
    new_.fn = _.fn
    new_.fn_args = _.fn_args

    result = new_.zeval()
    if result[0] == 'sat' and result[1]['x'][0] == 'Solution':
        return True
    return False

def test_summary_rfind():
    print('[*] Testing the function summary for rfind')

    with ConcolicTracer() as _:
        _[string_rfind_test]('haybeedlehay', 'needle')
    
    new_path = _.path[0:-1] + [z3.Not(_.path[-1])]
    new_ = ConcolicTracer((_.decls, new_path))
    new_.fn = _.fn
    new_.fn_args = _.fn_args

    result = new_.zeval()
    if result[0] == 'sat' and result[1]['x'][0].contains('needle'):
        return True
    return False


summary_dict = {
        'abs': test_summary_abs,
        'isalnum': test_summary_isalnum,
        'isdecimal': test_summary_isdecimal,
        'isdigit': test_summary_isdigit,
        'islower': test_summary_islower,
        'isnumeric': test_summary_isnumeric,
        'isprintable': test_summary_isprintable,
        'isspace': test_summary_isspace,
        'swapcase': test_summary_swapcase,
        'title': test_summary_title,
        'capitalize': test_summary_capitalize,
        'rfind': test_summary_rfind
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
