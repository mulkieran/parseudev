# -*- coding: utf-8 -*-
# Copyright (C) 2016 Anne Mulhern <amulhern@redhat.com>

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

    Parsing DM_UUID values.

    .. moduleauthor::  mulhern <amulhern@redhat.com>
"""

from __future__ import absolute_import

from ._shared import Field
from ._shared import ParseError
from ._shared import Parser


class DMUUIDParsers(object):
    """
    Aggregate parsers.
    """
    # pylint: disable=too-few-public-methods

    PARSERS = {
       'layer' : Parser(r'(cdata)|(cmeta)|(pool)|(real)|(tdata)|(tmeta)', ()),
       'partition' : Parser(r'part%s', (Field('partition', regexp=r'[^-]'),)),
       'component' : Parser(r'[^-]', ()),
       'uuid' : Parser(r'.+', ())
    }


class DMUUIDParse(object):
    """
    Represents a DM_UUID.
    """
    # pylint: disable=too-few-public-methods

    def __init__(self, parsers):
        """
        Initializer.

        :param parsers: parser objects to parse with
        :type parsers: dict of str * Parser
        """
        self.parsers = parsers

    def parse(self, value):
        """
        Parse a DM_UUID field.

        :param str value: the value to parse
        :returns: a dict of discovered components
        :rtype: dict of str * str
        :raises ParseError: on failure
        """
        match_dict = dict()

        partition = self.parsers['partition'].match(value)
        if partition is not None:
            partition_str = partition['partition']
            match_dict['partition'] = partition_str
            value = value[len(partition['total']) + 1:]

        component = self.parsers['component'].match(value)
        if component is None:
            raise ParseError('no component found in value %s' % value)

        component_str = component['total']
        match_dict['component'] = component_str
        value = value[len(component_str) + 1:]

        fields = value.rsplit('-', 1)
        if len(fields) == 2:
            (left, right) = fields
            layer = self.parsers['layer'].match(right)
            if layer is not None:
                layer_str = layer['total']
                match_dict['layer'] = layer_str
                value = left

        uuid = self.parsers['uuid'].match(value)
        if uuid is None:
            raise ParseError('no uuid found in value %s' % value)

        uuid_str = uuid['total']
        match_dict['uuid'] = uuid_str

        return match_dict
