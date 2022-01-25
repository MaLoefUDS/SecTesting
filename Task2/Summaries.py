import z3
import fuzzingbook.ConcolicFuzzer
from fuzzingbook.ConcolicFuzzer import zstr, zint, zbool, fresh_name, ConcolicTracer

class zint(zint):
    def __abs__(self) -> zint:
        pass # TODO: Implement me

class zstr(zstr):
    def __len__(self): # Do not change me
        return self._len

    def __contains__(self, m: str) -> zbool:
        no_match = zint(self.context, z3.IntVal(-1), -1)
        find = self.find(m)
        return zbool(self.context, find.z != no_match.z, self.v.find(m) != -1)

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

    def on_all(self, cond) -> zbool:
        z3s = list()
        pys = list()
        for char in self:
            z3_cond, py_cond = cond(char)
            z3s.append(z3_cond)
            pys.append(py_cond)
        return zbool(self.context, z3.And(z3s), all(pys))

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
        def upper_check(char):
            ordinal = zint(self.context, z3.IntVal(ord(char)), ord(char))
            z3_cond = z3.And([(ordinal >= ord("A")).z, (ordinal <= ord("Z")).z])
            py_cond = ord("A") <= ordinal.v <= ord("Z")
            return z3_cond, py_cond
        return self.on_all(upper_check)

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
        assert "Hello" in string1, "__contains__ failed"
        assert "Help" not in string1, "__contains__ failed"
        assert string1.endswith(string2, None, None), "endswith failed"
        assert not string1.endswith(string3, None, None), "endswith failed"
        assert not string3.isupper(), "isupper failed"
        assert string4.isupper(), "isupper failed"
        print("passed all tests")

