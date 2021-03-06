import string

import fuzzingbook.ConcolicFuzzer
import z3
from fuzzingbook.ConcolicFuzzer import zstr, zint, zbool, ConcolicTracer, fresh_name, zord, zchr


class zint(zint):
    def __abs__(self) -> zint:
        if self < 0:
            return zint(self.context, self.z * -1, self.v * -1)
        else:
            return self


class zstr(zstr):
    def __len__(self):  # Do not change me
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
        # First letter is uppercase, the rest is lowercase
        empty = ""
        ne = 'empty_%d' % fresh_name()
        result = zstr.create(self.context, ne, empty)
        # Don't know what this line does 🤔
        self.context[1].append(z3.StringVal(empty) == result.z)

        for index, i in enumerate(self):
            if index == 0:
                i = i.upper()
            else:
                i = i.lower()
            result += i
        return result

    def endswith(self, other: zstr, start: int = None, stop: int = None) -> zbool:
        assert start is None, 'No need to handle this parameter'
        assert stop is None, 'No need to handle this parameter'
        # IDEA:
        # Len(self) >= Len(other)
        # for i in range(len(other)):
        #    INDEX = Len(self) - Len(other) + i
        #    self[INDEX] == other[i]
        # These Constraints
        z, v = self._zv(other)
        return zbool(self.context, z3.SuffixOf(z, self.z), self.v.endswith(v))

    def isalnum(self) -> zbool:
        not_empty = self.length() > 0
        if not_empty:
            z3s = list()
            pys = list()
            for i in range(len(self)):
                is_alpha = self[i].isalpha()
                # isdecimal and isnumeric uses isdigit, as we only considered ASCII-Characters
                is_digit = self[i].isdigit()
                z3s.append(z3.Or([is_alpha.z, is_digit.z]))
                pys.append(is_alpha.v or is_digit.v)
            return zbool(self.context, z3.And(z3s), all(pys))
        else:
            return zbool(self.context, not_empty, False)

    def isalpha(self) -> zbool:
        not_empty = self.length() > 0
        is_alpha = self.in_set(string.ascii_letters)
        return zbool(self.context, z3.And([not_empty.z, is_alpha.z]), not_empty and is_alpha.v)

    def isdecimal(self) -> zbool:
        not_empty = self.length() > 0
        is_decimal = self.in_set(string.digits)
        return zbool(self.context, z3.And([not_empty.z, is_decimal.z]), not_empty and is_decimal.v)

    def isdigit(self) -> zbool:
        # We only consider ASCII-Characters therefore isdecimal is enough
        return self.isdecimal()

    def islower(self) -> zbool:
        return self.in_range(ord("a"), ord("z"))

    def isnumeric(self) -> zbool:
        # We only consider ASCII-Characters therefore isdecimal is enough
        return self.isdecimal()

    def isprintable(self) -> zbool:
        return self.in_set(string.printable)

    def isspace(self) -> zbool:
        return self.in_set(string.whitespace)

    def isupper(self) -> zbool:
        # Using not quite right-version as other version confuse z3 and produces weird unicode characters
        """
        not_empty = self.length() > 0
        if not_empty:
            z3s_or1 = list()
            z3s_or2 = list()
            for c in self:
                oz = zord(self.context, c.z)

                is_upper = z3.And([oz >= ord('A'), oz <= ord('Z')])
                z3s_or1.append(is_upper)

                is_lower = z3.And([oz >= ord('a'), oz <= ord('z')])
                z3s_or2.append(is_lower)
            return zbool(self.context, z3.And([z3.Or(z3s_or1), z3.Not(z3.Or(z3s_or2))]), self.v.isupper())
        else:
            return zbool(self.context, not_empty, False)
        """
        return self.in_set(string.ascii_uppercase)

    def rfind(self, sub: str, start: int = None, stop: int = None) -> zint:
        assert start is None, 'No need to handle this parameter'
        assert stop is None, 'No need to handle this parameter'
        z, v = self._zv(sub)
        length = z3.Length(self.z)
        sub_length = z3.Length(z)
        last = zint(self.context, length - sub_length, len(self) - len(sub))
        while True:
            index = zint(self.context, z3.IndexOf(self.z, z, last), self.v.find(v, last.v))
            if index.v != -1:
                break
            last = last - 1
            if last.v < 0:
                break
        return index



    def swapcase(self) -> zstr:
        # TODO fix this shit, constraints not working / solvable
        empty = ""
        ne = 'empty_%d' % fresh_name()
        result = zstr.create(self.context, ne, empty)
        self.context[1].append(z3.StringVal(empty) == result.z)

        for index, i in enumerate(self):
            if i.isupper():
                i = i.lower()
            elif i.islower():
                i = i.upper()
            result += i
        return result

    def title(self) -> zstr:
        # Every word starts with a capital letter
        empty = ""
        ne = 'empty_%d' % fresh_name()
        result = zstr.create(self.context, ne, empty)
        # Don't know what this line does 🤔
        self.context[1].append(z3.StringVal(empty) == result.z)
        cdiff = (ord('a') - ord('A'))

        pc = ""
        for index, i in enumerate(self):
            if index == 0:
                i = i.upper()
                pc = i
            else:
                # Idea is to only "upper" the character, when the previous character is not alpha
                # and the current character is lowercase
                pc_oz = zord(self.context, pc.z)

                pc_rz1 = z3.And([pc_oz >= ord('a'), pc_oz <= ord('z')])
                pc_rz2 = z3.And([pc_oz >= ord('A'), pc_oz <= ord('Z')])
                pc_rz = z3.Not(z3.Or([pc_rz1, pc_rz2]))

                oz = zord(self.context, i.z)
                uz = zchr(self.context, oz - cdiff)
                rz_1 = z3.And([oz >= ord('a'), oz <= ord('z')])
                rz = z3.And([pc_rz, rz_1])
                ov = ord(i.v)
                uv = chr(ov - cdiff)

                if zbool(self.context, rz, not pc.v.isalpha() and i.v.islower()):
                    i = zstr(self.context, uz, uv)
                else:
                    i = zstr(self.context, i.z, i.v)
                pc = i
            result += i
        return result


def setup_summary():
    fuzzingbook.ConcolicFuzzer.__dict__['zstr'] = zstr
    fuzzingbook.ConcolicFuzzer.__dict__['zint'] = zint
    fuzzingbook.ConcolicFuzzer.Z3_OPTIONS = '-T:5'  # Set solver timeout to 5 seconds. Might be possible to reduce this given a strong CPU, or must be increased with a weak CPU.


if __name__ == "__main__":
    with ConcolicTracer() as _:
        string1 = zstr(_.context, z3.String("string_1"), "Hello World")
        string2 = zstr(_.context, z3.String("string_2"), "World")
        string3 = zstr(_.context, z3.String("string_3"), "Work")
        string4 = zstr(_.context, z3.String("string_4"), "WORK")
        string5 = zstr(_.context, z3.String("string_5"), "A#")
        empty = zstr(_.context, z3.String("empty"), " ")
        assert "Hello" in string1, "__contains__ failed"
        assert "Help" not in string1, "__contains__ failed"
        assert string1.endswith(string2, None, None), "endswith failed"
        assert not string1.endswith(string3, None, None), "endswith failed"
        assert not string3.isupper(), "isupper failed"
        assert not empty.isupper(), "isupper failed"
        assert string4.isupper(), "isupper failed"
        assert string5.isupper(), "isupper failed"
        print("passed all tests")
