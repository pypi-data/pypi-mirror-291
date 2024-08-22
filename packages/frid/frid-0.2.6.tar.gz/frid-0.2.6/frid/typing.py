from abc import ABC
from dataclasses import asdict, is_dataclass
from datetime import date as dateonly, time as timeonly, datetime
from collections.abc import Mapping, Sequence, Set
from enum import Enum
from typing import Generic, Literal, NamedTuple, TypeVar, final

# Quick union types used in many places
BlobTypes = bytes|bytearray|memoryview
DateTypes = dateonly|timeonly|datetime   # Note that datetime in Python is deriveed from date

# FRID types follow (Flexibly represented inteactive data)

_T = TypeVar('_T')
_B = TypeVar('_B', bound='FridBasic')
_M = TypeVar('_M', bound='FridMixin')

class FridBeing(Enum):
    """This "being or not being" class introduces two special values, PRESENT and MISSING.
    The main purpose is to be used for values of a map. If the value
    is PRESENT for a key, it means the key is present but there is
    no meaningful associated value. If the value is MISSING for a key,
    the the entry in the map should be handled as it is not there.
    """
    PRESENT = True
    MISSING = False
    def __bool__(self):
        return self.value
    def strfr(self) -> str:
        return "+." if self.value else "-."
    @classmethod
    def parse(cls, s: str) -> 'FridBeing|None':
        match s:
            case '+.':
                return PRESENT
            case '-.':
                return MISSING
            case _:
                return None

PresentType = Literal[FridBeing.PRESENT]
MissingType = Literal[FridBeing.MISSING]
PRESENT: PresentType = FridBeing.PRESENT
MISSING: MissingType = FridBeing.MISSING

class FridBasic(ABC):
    """The abstract base class that handles some basic datatypes in string format.
    - The constructor must at least accept a single string-formated positional argument.
    - If the constractor raises an exception then the format is not accepted.
    - When a string is parsed and a list of FridBasic data types are given
      as options, their constructors will be tried one by one until the one
      raises no exception.
    - The directed class should overwrite either frid_repr() to return a string,
      or overwrite __str__() because frid_repr() calls __str__() by default.
    Note that the string representaion here if rather limited:
    - The entire string should contain only quote free characters (letters,
      numbers, and +-._ and a few other, see is_quote_free_char()).
    - It must not be a quote-free string (otherwise it is handled as a string).
    - It must not be parsed as first-order pri, like constants, numbers,
    datetimes, blobs, etc.
    - The main purpose is to allow user-defined numerical types, such as
      complex numbers, fractional numbers, dimensional quantities, etc.
    """
    def frid_repr(self) -> str:
        """Convert the data to string representation."""
        return self.__str__()
    @classmethod
    def frid_from(cls: type[_B], s: str, /, *args, **kwargs) -> _B|None:
        """Construct from string reprentation"""
        return cls(s, *args, **kwargs) # type: ignore

class FridMixin(ABC):
    """The abstract base frid class to be loadable and dumpable.

    A frid class needs to implement three methods:
    - A class method `frid_keys()` that returns a list of acceptable keys
      for the class (default includes the class name);
    - A class method `frid_from()` that constructs and object of this class
      with the name, and a set of positional and keyword arguments
      (default is to check the name against acceptable keys, and then call
      the constructor with these arguments).
    - A instance method `frid_repr()` that converts the object to a triplet:
      a name, a list of positional values, and a dict of keyword values
      (this method is abstract).
    """
    @classmethod
    def frid_keys(cls) -> Sequence[str]:
        """The list of keys that the class provides; the default containing class name only."""
        return [cls.__name__]

    @classmethod
    def frid_from(cls: type[_M], data: 'FridNameArgs') -> _M:
        """Construct an instance with given name and arguments."""
        assert data.name in cls.frid_keys()
        return cls(*data.args, **data.kwds)

    def frid_repr(self) -> 'FridNameArgs':
        """Converts an instance to a triplet of name, a list of positional values,
        and a dict of keyword values.

        The default implementation handles dataclasses derived from this Mixin,
        but raises a NotImplementedError for other types of classes.
        """
        if is_dataclass(self):
            return FridNameArgs(self.__class__.__name__, (), asdict(self))
        raise NotImplementedError

# The Prime types must all be immutable and hashable
FridPrime = str|float|int|bool|BlobTypes|DateTypes|FridBasic|None
FridExtra = FridMixin|Set[FridPrime]  # Only set of primes, no other
FridMapVT = Mapping|Sequence|FridPrime|FridExtra|FridBeing  # Allow PRESENT/MISSING for dict
StrKeyMap = Mapping[str,FridMapVT]
FridSeqVT = StrKeyMap|Sequence|Set|FridPrime|FridMixin
FridArray = Sequence[FridSeqVT]
FridValue = StrKeyMap|FridArray|FridPrime|FridExtra

class FridNameArgs(NamedTuple):
    """This is a named tuple used to create and represent FridMixin."""
    name: str
    args: FridArray
    kwds: StrKeyMap

FridTypeName = Literal['frid','text','blob','list','dict','real','date','null','bool','']
FridTypeSize = tuple[FridTypeName,int]

@final
class ValueArgs(Generic[_T]):
    """Container to hold a value of specific type with positional and keyword arguments."""
    __slots__ = ('data', 'args', 'kwds')
    def __init__(self, data: _T, *args, **kwds):
        self.data = data
        self.args = args
        self.kwds = kwds
    def __args_to_str(self):
        sargs = [repr(x) for x in self.args]
        sargs.extend(str(k) + "=" + repr(v) for k, v in self.kwds.items())
        return "(" + ", ".join(sargs) + ")"
    def __str__(self):
        return str(self.data) + self.__args_to_str()
    def __repr__(self):
        return repr(self.data) + self.__args_to_str()
