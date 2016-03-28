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
    tests.test_parsing
    ==================

    Test parsing values that happen to be synthesized from other values
    such that they need to be parsed.

    .. moduleauthor:: mulhern <amulhern@redhat.com>
"""


from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import glob
import os

from itertools import groupby

import pyudev

import parseudev

import pytest

from hypothesis import given
from hypothesis import settings
from hypothesis import strategies

_CONTEXT = pyudev.Context()
_DEVICES = _CONTEXT.list_devices()


class TestIDPATH(object):
    """
    Test parsing ID_PATH values.
    """
    # pylint: disable=too-few-public-methods
    _devices = [d for d in _DEVICES if d.get('ID_PATH') is not None]
    @pytest.mark.skipif(
       len(_devices) == 0,
       reason="no devices with ID_PATH property"
    )
    @given(strategies.sampled_from(_devices))
    @settings(min_satisfying_examples=1)
    def test_parsing(self, a_device):
        """
        Test that parsing is satisfactory on all examples.
        """
        parsers = parseudev.IdPathParsers.PARSERS
        id_path = a_device.get('ID_PATH')
        parser = parseudev.IdPathParse(parsers)
        result = parser.parse(id_path)
        assert isinstance(result, list) and result != []
        assert all(
           any(r[1]['total'].startswith(p.prefix) for p in parsers) \
                   for r in result
        )
        assert not any(r[1]['total'].startswith('-') for r in result)

    _devices = [d for d in _DEVICES if d.get('ID_SAS_PATH') is not None]
    @pytest.mark.skipif(
       len(_devices) == 0,
       reason="no devices with ID_SAS_PATH property"
    )
    @given(strategies.sampled_from(_devices))
    @settings(min_satisfying_examples=1)
    def test_parsing_sas_path(self, a_device):
        """
        Test that parsing is satisfactory on all examples.
        """
        parsers = parseudev.IdPathParsers.PARSERS
        id_path = a_device.get('ID_SAS_PATH')
        parser = parseudev.IdPathParse(parsers)
        result = parser.parse(id_path)
        assert isinstance(result, list) and result != []
        assert all(
           any(r[1]['total'].startswith(p.prefix) for p in parsers) \
                   for r in result
        )
        assert not any(r[1]['total'].startswith('-') for r in result)

    def test_failure(self):
        """
        Test at least one failure.
        """
        id_path = 'pci-0000_09_00_0-sas0x5000155359566200-lun-0'
        parser = parseudev.IdPathParse(parseudev.IdPathParsers.PARSERS)
        with pytest.raises(parseudev.ParseError):
            parser.parse(id_path)


class TestDevlinks(object):
    """
    Test ``Devlinks`` methods.
    """
    # pylint: disable=too-few-public-methods

    def _symbolic_non_device_number_links(self):
        """
        Finds all symbolic links that are not in device number directories,
        /dev/block and /dev/char.

        Returns a generator of these links.
        """
        files = glob.glob('/dev/*') + glob.glob('/dev/*/*')
        return (
           f for f in files \
              if os.path.islink(f) and \
              os.path.dirname(f) not in ('/dev/char', '/dev/block')
        )

    _devices = [d for d in _DEVICES if list(d.device_links)]
    @pytest.mark.skipif(
       len(_devices) == 0,
       reason="no devices with device links"
    )
    @given(strategies.sampled_from(_devices))
    @settings(max_examples=10, min_satisfying_examples=1)
    def test_devlinks(self, a_device):
        """
        Verify that device links are in "by-.*" categories or no category.
        """
        device_links = (parseudev.Devlink(d) for d in a_device.device_links)

        def sort_func(dl):
            """
            :returns: category of device link
            :rtype: str
            """
            key = dl.category
            return key if key is not None else ""

        devlinks = sorted(device_links, key=sort_func)

        categories = list(k for k, g in groupby(devlinks, sort_func))
        assert all(c == "" or c.startswith("by-") for c in categories)

        assert all((d.category is None and d.value is None) or \
           (d.category is not None and d.value is not None) \
           for d in devlinks)

        assert all(d.path == str(d) for d in devlinks)

        assert all(os.path.exists(d.path) for d in devlinks)

        # check that all links in filesystem that point to this device
        # and should have corresponding device links do
        device_node = a_device.device_node
        for link in self._symbolic_non_device_number_links():
            realfile = os.path.realpath(link)
            if os.path.exists(realfile) and \
               os.path.samefile(realfile, device_node):
                assert parseudev.Devlink(link) in devlinks


class TestPCIAddress(object):
    """
    Test parsing a PCI address object.
    """
    # pylint: disable=too-few-public-methods

    _devices = [d for d in _DEVICES if d.subsystem == 'pci']
    @pytest.mark.skipif(
       len(_devices) == 0,
       reason="no devices with subsystem pci"
    )
    @given(strategies.sampled_from(_devices))
    @settings(min_satisfying_examples=1)
    def test_parsing_pci(self, a_device):
        """
        Test correct parsing of pci-addresses.
        """
        parser = parseudev.PCIAddressParse()
        result = parser.parse(a_device.sys_name)
        assert all(result[k] != "" for k in result.keys())

    def testExceptions(self):
        """
        Test exception.
        """
        parser = parseudev.PCIAddressParse()
        with pytest.raises(parseudev.ParseError):
            parser.parse("junk")


class TestDMUUID(object):
    """
    Test parsing a DM_UUID str.
    """
    # pylint: disable=too-few-public-methods
    _devices = [d for d in _DEVICES if d.get('DM_UUID') is not None]
    @pytest.mark.skipif(
       len(_devices) == 0,
       reason="no devices with DM_UUID property"
    )
    @given(strategies.sampled_from(_devices))
    @settings(min_satisfying_examples=1)
    def test_parsing_dmuuid(self, a_device):
        """
        Test parsing of DM_UUIDs.
        """
        value = a_device['DM_UUID']
        parser = parseudev.DMUUIDParse()
        result = parser.parse(value)
        assert 'uuid' in result
        assert 'component' in result
        assert len(result) <= 4
        assert set(result.keys()) <= set(parser.keys)

        if value.startswith('part'):
            assert 'partition' in result
        else:
            assert 'partition' not in result

    def testException(self):
        """
        Test exceptions.
        """
        parser = parseudev.DMUUIDParse()
        with pytest.raises(parseudev.ParseError):
            parser.parse('')
        with pytest.raises(parseudev.ParseError):
            parser.parse('j')
