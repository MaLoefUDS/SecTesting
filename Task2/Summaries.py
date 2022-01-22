import z3
import fuzzingbook.ConcolicFuzzer
from fuzzingbook.ConcolicFuzzer import zstr, zint, zbool, fresh_name

class zint(zint):
    def __abs__(self) -> zint:
        pass # TODO: Implement me

class zstr(zstr):
    def __contains__(self, m: str) -> zbool:
        pass # TODO: Implement me

    def capitalize(self) -> zstr:
        pass # TODO: Implement me

    def endswith(self, other: zstr, start: int, stop: int) -> zbool:
        assert start is None, 'No need to handle this parameter'
        assert stop is None, 'No need to handle this parameter'
        pass # TODO: Implement me

    def isalnum(self) -> zbool:
        pass # TODO: Implement me

    def isdecimal(self) -> zbool:
        pass # TODO: Implement me

    def isdigit(self) -> zbool:
        pass # TODO: Implement me

    def islower(self) -> zbool:
        pass # TODO: Implement me

    def isnumeric(self) -> zbool:
        pass # TODO: Implement me

    def isprintable(self) -> zbool:
        pass # TODO: Implement me

    def isspace(self) -> zbool:
        pass # TODO: Implement me

    def isupper(self) -> zbool:
        pass # TODO: Implement me

    def rfind(self, sub: str, start: int, stop:int) -> zint:
        assert start is None, 'No need to handle this parameter'
        assert stop is None, 'No need to handle this parameter'
        pass # TODO: Implement me

    def swapcase(self) -> zstr:
        pass # TODO: Implement me

    def title(self) -> zstr:
        pass # TODO: Implement me



def setup_summary():
    fuzzingbook.ConcolicFuzzer.__dict__['zstr'] = zstr
    fuzzingbook.ConcolicFuzzer.__dict__['zint'] = zint
    fuzzingbook.ConcolicFuzzer.Z3_OPTIONS = '-T:5' # Set solver timeout to 5 seconds. Might be possible to reduce this given a strong CPU, or must be increased with a weak CPU.
