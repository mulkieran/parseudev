# -*- coding: utf-8 -*-
# Copyright (C) 2015 Anne Mulhern <amulhern@redhat.com>

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
    parseudev._lookup
    =================

    A partial map from udev property names to parsers.

    .. moduleauthor::  mulhern <amulhern@redhat.com>
"""

from __future__ import absolute_import

from ._id_path import IdPathParse
from ._id_path import IdPathParsers

from ._shared import OpaqueValueError


class Lookup(object): # pragma: no cover
    """
    Given a udev property name, returns a parser.
    """
    # pylint: disable=too-few-public-methods

    _OPAQUE = ["DM_UUID"]

    _MAP = {
       "ID_PATH" : IdPathParse(IdPathParsers.PARSERS),
       "ID_SAS_PATH" : IdPathParse(IdPathParsers.PARSERS)
    }

    @classmethod
    def lookup(cls, property_name):
        """
        Lookup a parser for the property name.

        :param str property_name: the name of the property
        :returns: a parser or None if not found
        :rtype: parse.Parse or NoneType
        :raises OpaqueValueError: if property should not be parsed
        """

        if property_name in cls._OPAQUE:
            raise OpaqueValueError(property_name)
        return cls._MAP.get(property_name)
