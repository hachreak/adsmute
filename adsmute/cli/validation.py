# -*- coding: utf-8 -*-
#
# This file is part of adsmute.
# Copyright 2020 Leonardo Rossi <leonardo.rossi@studenti.unipr.it>.

"""Validations."""

from ..utils import load_source as ls, load_file as lf


def load_source(ictx, param, value):
    return ls(value)


def load_file(ictx, param, value):
    return lf(value)
