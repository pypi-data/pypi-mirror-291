try:
    from bleongpkg.extra_time import now
except ImportError:
    _has_arrow = False
else:
    _has_arrow = True


def main():
    if _has_arrow:
        print(now())
    else:
        print("arrow not installed")


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
