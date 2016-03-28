# -*- coding: utf-8 -*-
# Copyright (C) 2016 mulhern <amulhern@redhat.com>

# This library is free software; you can redistribute it and/or modify it
# under the terms of the GNU Lesser General Public License as published by the
# Free Software Foundation; either version 2.1 of the License, or (at your
# option) any later version.

# This library is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
# FITNESS FOR A PARTICULAR PURPOSE.  See the GNU Lesser General Public License
# for more details.

# You should have received a copy of the GNU Lesser General Public License
# along with this library; if not, write to the Free Software Foundation,
# Inc., 51 Franklin St, Fifth Floor, Boston, MA 02110-1301 USA


"""
    parseudev._shared._parse
    ========================

    Abstract parents of parse classes.

    .. moduleauthor::  mulhern <amulhern@redhat.com>
"""

from __future__ import absolute_import

import abc

from six import add_metaclass


@add_metaclass(abc.ABCMeta)
class Parse(object):
    """
    Very abstract class for aggregating parsers.
    """
    # pylint: disable=too-few-public-methods

    @abc.abstractmethod
    def parse(self, value):
        """
        Parse the value.

        :param str value: the value to parse
        :returns: the result of parsing
        :rtype: object
        :raises: ParseError on failure
        """
        raise NotImplementedError() # pragma: no cover


@add_metaclass(abc.ABCMeta)
class OrderedParse(Parse):
    """
    A parser where the order of the elements parsed matters.
    """
    # pylint: disable=too-few-public-methods

    @abc.abstractmethod
    def parse(self, value):
        """
        Parse the value.

        :param str value: the value to parse
        :returns: the result of parsing
        :rtype: list of tuple of Parser * dict
        :raises: ParseError on failure
        """
        raise NotImplementedError() # pragma: no cover


@add_metaclass(abc.ABCMeta)
class SimpleParse(Parse):
    """
    A parser with a definite set of keys and no ordering.

    If the keys are not all matched, then no value is returned.
    """
    # pylint: disable=too-few-public-methods

    @abc.abstractmethod
    def parse(self, value):
        """
        Parse the value.

        :param str value: the value to parse
        :returns: the result of parsing
        :rtype: dict or NoneType
        :raises: ParseError on failure
        """
        raise NotImplementedError() # pragma: no cover


@add_metaclass(abc.ABCMeta)
class PartialParse(SimpleParse):
    """
    Extends SimpleParse by allowing only a partial match for keys.
    """
    # pylint: disable=too-few-public-methods

    @abc.abstractmethod
    def keys(self):
        """
        The possible keys for this parse.
        """
        raise NotImplementedError() # pragma: no cover
