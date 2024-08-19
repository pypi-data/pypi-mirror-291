from collections import Counter
from functools import lru_cache


@lru_cache(maxsize=10)
def count(to_counter: str):
    if not isinstance(to_counter, str):
        raise TypeError("Input is not a string")
    # Filter to remove all kind of spaces from counting.
    filtered_str = ''.join(char for char in to_counter if char not in (' ', '\t', '\n'))
    counter_dict = Counter(filtered_str)
    count_ones = (value for value in counter_dict.values() if value == 1)
    return sum(count_ones)
