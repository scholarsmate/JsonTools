"""Tests for the jtools CLI module."""


from subprocess import PIPE, Popen as popen
from unittest import TestCase

from jtools import __version__ as VERSION


class TestHelp(TestCase):
    def test_returns_usage_information(self):
        output = popen(['jtools', '-h'], stdout=PIPE).communicate()[0]
        self.assertTrue('Usage:' in output)

        output = popen(['jtools', '--help'], stdout=PIPE).communicate()[0]
        self.assertTrue('Usage:' in output)


class TestVersion(TestCase):
    def test_returns_version_information(self):
        output = popen(['jtools', '--version'], stdout=PIPE).communicate()[0]
        self.assertEqual(output.strip(), VERSION)
