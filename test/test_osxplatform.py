#!/usr/bin/env python
import osxplatform
import unittest


class TestBrewsize(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_get_platform(self):
        self.assertEqual(osxplatform.get_platform('10.0'), 'cheetah')
        self.assertEqual(osxplatform.get_platform('10.1'), 'puma')
        self.assertEqual(osxplatform.get_platform('10.2'), 'jaguar')
        self.assertEqual(osxplatform.get_platform('10.3'), 'panther')
        self.assertEqual(osxplatform.get_platform('10.4'), 'tiger')
        self.assertEqual(osxplatform.get_platform('10.5'), 'leopard')
        self.assertEqual(osxplatform.get_platform('10.6'), 'snow_leopard')
        self.assertEqual(osxplatform.get_platform('10.7'), 'lion')
        self.assertEqual(osxplatform.get_platform('10.8'), 'mountain_lion')
        self.assertEqual(osxplatform.get_platform('10.9'), 'mavericks')
        self.assertEqual(osxplatform.get_platform('10.10'), 'yosemite')
        self.assertEqual(osxplatform.get_platform('10.11'), 'el_capitan')
        self.assertEqual(osxplatform.get_platform('10.12'), 'sierra')
        self.assertEqual(osxplatform.get_platform('10.13'), 'high_sierra')
        self.assertEqual(osxplatform.get_platform('10.14'), 'mojave')


def main():
    unittest.main()


if __name__ == "__main__":
    main()
