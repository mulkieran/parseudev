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
    parseudev._dm_uuid
    ==================

    Parsing a DM_UUID.

    In theory, these should be opaque, and for device-mapper only.

    In practice, they are the only indications of the device-mapper subsystem
    available.

    .. moduleauthor::  mulhern <amulhern@redhat.com>
"""

from __future__ import absolute_import

import string

from ._shared import parse

from ._shared import ParseError


class DMUUIDParse(parse.SimpleParse):
    """
    Parse a DM_UUID.

    It consists of a subsystem identifier, which only contains characters,
    and a "rest", which could be anything. Properly speaking, this is not
    a correct grammar, but it should work on existing UUIDs.
    """
    # pylint: disable=too-few-public-methods

    def parse(self, value):
        rest_char = \
           next((x for x in value if x not in string.ascii_letters), None)
        if rest_char is None:
            return (value, '')
        rest_index = value.find(rest_char)
        (subsystem, rest) = (value[:rest_index], value[rest_index:])
        if subsystem == '':
            raise ParseError('no match for %s' % value)
        return {'subsystem' : subsystem, 'rest' : rest}
