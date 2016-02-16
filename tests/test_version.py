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
    test_version
    ============

    Test version information.

    .. moduleauthor::  mulhern  <amulhern@redhat.com>
"""

from __future__ import absolute_import

import unittest

import parseudev


class VersionTest(unittest.TestCase):
    """ Tests for version. """

    def testExists(self):
        """
        Test that we can get the version.
        """

        self.assertIsNotNone(parseudev.__version__)
        self.assertIsNotNone(parseudev.__version_info__)
