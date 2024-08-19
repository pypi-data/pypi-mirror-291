from abc import ABC, abstractmethod
import re


# SI prefixes (powers of 10)
KILO = 1000
MEGA = KILO * 1000
GIGA = MEGA * 1000
TERA = GIGA * 1000

# Binary prefixes (powers of 2)
KIBI = 1024
MEBI = KIBI * 1024
GIBI = MEBI * 1024
TEBI = GIBI * 1024


class SizeFilter(ABC):
    def __init__(self, limit):
        self.limit = limit
    
    @abstractmethod
    def is_within(self, size):
        return None

    @classmethod
    def from_string(cls, s):
        try:
            return cls.parse_opt(s)
        except:
            raise Exception("'%s' is not a valid size constraint. See 'fd --help'." % s)

    @staticmethod
    def parse_opt(s):
        pattern = re.compile(r"(?i)^([+-]?)(\d+)(b|[kmgt]i?b?)$")

        m = pattern.match(s)
        
        if not m:
            raise Exception

        limit_kind = m.group(1)
        quantity = int(m.group(2))

        unit = m.group(3).lower() if m.group(3) else "b"

        if unit.startswith("ki"):
            multiplier = KIBI
        elif unit.startswith("k"):
            multiplier = KILO
        elif unit.startswith("mi"):
            multiplier = MEBI
        elif unit.startswith("m"):
            multiplier = MEGA
        elif unit.startswith("gi"):
            multiplier = GIBI
        elif unit.startswith("g"):
            multiplier = GIGA
        elif unit.startswith("ti"):
            multiplier = TEBI
        elif unit.startswith("t"):
            multiplier = TERA
        elif unit == "b":
            multiplier = 1
        else:
            raise Exception

        size = quantity * multiplier

        if limit_kind == "+":
            return Min(size)
        elif limit_kind == "-":
            return Max(size)
        elif limit_kind == "":
            return Equals(size)
        else:
            raise Exception


class Max(SizeFilter):
    def is_within(self, size):
        return size <= self.limit


class Min(SizeFilter):
    def is_within(self, size):
        return size >= self.limit


class Equals(SizeFilter):
    def is_within(self, size):
        return size == self.limit


SizeFilter.register(Max)
SizeFilter.register(Min)
SizeFilter.register(Equals)
