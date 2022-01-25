import string

import z3
import fuzzingbook.ConcolicFuzzer
from fuzzingbook.ConcolicFuzzer import zstr, zint, zbool, fresh_name, ConcolicTracer

class zint(zint):
    def __abs__(self) -> zint:
        if self < 0:
            return zint(self.context, self.z * -1, self.v * -1)
        else:
            return self

class zstr(zstr):
    def __len__(self): # Do not change me
        return self._len

    def __contains__(self, m: str) -> zbool:
        no_match = zint(self.context, z3.IntVal(-1), -1)
        find = self.find(m)
        return zbool(self.context, find.z != no_match.z, self.v.find(m) != -1)

    def on_all(self, cond) -> zbool:
        z3s = list()
        pys = list()
        for i in range(len(self)):
            z3_cond, py_cond = cond(self[i])
            z3s.append(z3_cond)
            pys.append(py_cond)
        return zbool(self.context, z3.And(z3s), all(pys))

    def in_range(self, start, end):
        _set = "".join([chr(i) for i in range(start, end)])
        return self.in_set(_set)

    def in_set(self, _set):
        def check_include(char):
            z3s = list()
            pys = list()
            for elem in _set:
                cond = (char == elem)
                z3s.append(cond.z)
                pys.append(cond.v)
            return z3.Or(z3s), any(pys)
        return self.on_all(check_include)

    def capitalize(self) -> zstr:
        pass # TODO: Implement me

    def endswith(self, other: zstr, start: int = None, stop: int = None) -> zbool:
        assert start is None, 'No need to handle this parameter'
        assert stop is None, 'No need to handle this parameter'
        len_self = z3.Length(self.z)
        len_suffix = z3.Length(other.z)
        diff = zint(self.context, len_self - len_suffix, len(self.v) - len(other.v))
        if diff < 0:
            return zbool(self.context, diff < 0, diff.v < 0)
        return zbool(self.context, self.startswith(other, beg=diff.v).z, self.v.startswith(other.v, diff.v))

    def isalnum(self) -> zbool:
        is_dec = self.isdecimal()
        is_dig = self.isdigit()
        is_num = self.isnumeric()
        return zbool(self.context,
                     z3.Or([is_dec.z, is_dig.z, is_num.z]),
                     any([is_dec.v, is_dig.v, is_num.v]))

    def isdecimal(self) -> zbool:
        return self.in_set(string.digits)

    def isdigit(self) -> zbool:
        pass  # TODO: Implement me

    def islower(self) -> zbool:
        return self.in_range(ord("a"), ord("z"))

    def isnumeric(self) -> zbool:
        pass # TODO: Implement me

    def isprintable(self) -> zbool:
        return self.in_set(string.printable)

    def isspace(self) -> zbool:
        _set = [" ", "\t", "\n"]
        pass # TODO: Implement me

    def isupper(self) -> zbool:
        return self.in_range(ord("A"), ord("Z"))

    def rfind(self, sub: str, start: int = None, stop: int = None) -> zint:
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


if __name__ == "__main__":
    with ConcolicTracer() as _:
        string1 = zstr(_.context, z3.String("string_1"), "Hello World")
        string2 = zstr(_.context, z3.String("string_2"), "World")
        string3 = zstr(_.context, z3.String("string_3"), "Work")
        string4 = zstr(_.context, z3.String("string_4"), "WORK")
        empty = zstr(_.context, z3.String("empty"), " ")
        assert "Hello" in string1, "__contains__ failed"
        assert "Help" not in string1, "__contains__ failed"
        assert string1.endswith(string2, None, None), "endswith failed"
        assert not string1.endswith(string3, None, None), "endswith failed"
        assert not string3.isupper(), "isupper failed"
        assert not empty.isupper(), "isupper failed"
        assert string4.isupper(), "isupper failed"
        print("passed all tests")

