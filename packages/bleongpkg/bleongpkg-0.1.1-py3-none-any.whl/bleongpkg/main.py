from typing import Callable, Optional, TypeGuard, TypeVar

CallableT = TypeVar("CallableT", bound=Callable)

try:
    from bleongpkg.extra_time import now
except ImportError:
    now = None


def main():
    if has_arrow(now):
        print(now())
    else:
        print("arrow not installed")


def has_arrow(v: Optional[CallableT]) -> TypeGuard[CallableT]:
    return v is not None


"""
   |x||x||x|
 1 |x|
 2 |x||
 3 |x||x|
 4 |x||x||
 5 |x||x||x|
 6   ||x|
 7   ||x||
 8   ||x||x|
 9    |x|
10    |x||
11    |x||x|
12      ||x|
13       |x|
     || ||
"""
