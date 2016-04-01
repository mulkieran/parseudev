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
    parseudev._shared
    =================

    Some classes that parsers share.

    .. moduleauthor::  mulhern <amulhern@redhat.com>
"""

from __future__ import absolute_import

import re


class Parser(object):
    """
    A generic parser object.
    """

    def __init__(self, format_string, fields):
        """
        Initializer.

        :param str format_string: string used to format this id by udev
        :param fields: list of fields that fill the string

        ``format_string`` must content itself with basic C-style format
        codes, beginning with '%' as '%s', '%d'.
        """
        self.format_string = '%s' % format_string
        self.fields = fields
        self._prefix = self.format_string.split('%', 1)[0]

        # pylint: disable=protected-access
        substitution_list = [
           ('(?P<%s>%s)' % (f.name, f._regexp)) for f in self.fields
        ]
        regexp = self.format_string % tuple(substitution_list)
        self._regexp = re.compile('(?P<total>%s)' % regexp)

    @property
    def prefix(self):
        """
        A partially distinguishing prefix.

        Some parsers may use the same prefix.

        :returns: a prefix that distinguishes the parser from other parsers
        :rtype: str
        """
        return self._prefix

    @property
    def keys(self):
        """
        Keys within the regular expression.

        :returns: a list of the keys useful for finding portions of a match
        :rtype: list of str
        """
        return [f.name for f in self.fields] + ['total']

    def match(self, value):
        """
        Match ``value`` if possible.

        :returns: a dict representing the match, or None
        :rtype: dict or NoneType
        """
        result = self._regexp.match(value)
        return result.groupdict() if result is not None else None


class Field(object):
    """
    A field in a parser regular expression.
    """
    # pylint: disable=too-few-public-methods

    def __init__(self, name, regexp=r'.+', description=None):
        """
        Initializer.

        :param str name: the name of the field
        :param str regexp: regular expression to match the field

        The best choice of regular expression may generally define a language
        that is a superset of the actual language of the field.
        Since the containing regular expression will constrain matches, the
        regular expression does not need to be the most precise.
        In general, '.*' may be good enough.
        """
        self.name = name
        self._regexp = regexp
        self.description = description


class ParseError(Exception):
    """ Parse exception. """
    pass


class OpaqueValueError(Exception):
    """ Exception raised when looking up parser for an opaque value. """

    def __init__(self, name): # pragma: no cover
        """
        Initializer.

        :param str name: name of property to parse
        """
        # pylint: disable=super-init-not-called
        self._name = name

    def __str__(self): # pragma: no cover
        return "%s is an opaque value" % self._name
