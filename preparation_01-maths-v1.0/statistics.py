"""
This file contains a set of functions to practice your
statistics skills.

It needs to be completed with "vanilla" Python, without
help from any library.
"""

from math import sqrt


def calculate_mean(data):
    """
    Return the mean of a python list

    If data is empty raise a ValueError

    :param data: a list of numbers
    :return: the mean of the list
    :rtype: float
    :raise ValueError:
    """

    if not data:
        raise ValueError("List cannot be empty")

    return sum(data)/len(data)


def calculate_standard_deviation(data):
    """
    Return the standard deviation of a python list using the
    population size (N) in order to calculate the variance.

    If data is empty raise a ValueError

    :param data: list of numbers
    :return: the standard deviation of the list
    :rtype: float
    :raise ValueError:
    """

    if not data:
        raise ValueError("List cannot be empty")

    xbar = calculate_mean(data)

    return sqrt(calculate_mean([(val-xbar) * (val-xbar) for val in data]))


def remove_outliers(data):
    """
    Given a list of numbers, find outliers and return a new
    list that contains all points except outliers
    We consider points lying outside 2 standard
    deviations from the mean.

    Make sure that you do not modify the original list!

    If data is empty raise a ValueError

    :param data: list of numbers
    :return: a new list without outliers
    :rtype: list
    :raise ValueError:
    """

    if not data:
        raise ValueError("List cannot be empty")

    if len(data) == 1:
        return data

    xbar = calculate_mean(data)
    std_dev = calculate_standard_deviation(data)
    max_val = xbar + (2 * std_dev)
    min_val = xbar - (2 * std_dev)

    return [val for val in data if min_val < val < max_val]
