
"""Validations."""

from ..utils import load_source as ls


def load_source(ictx, param, value):
    return ls(value)
