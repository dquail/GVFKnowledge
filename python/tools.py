"""
Various utility functions
"""

#import math


def get_next_pow2(number):
    """ Gets the next highest power of two for number
    """
    return 2**int(math.ceil(math.log(number, 2)))