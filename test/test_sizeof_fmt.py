#!/usr/bin/env python
import sizeof_fmt
import unittest

class TestSizeof_fmt(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_sizeof_fmt(self):
        val = 1024
        self.assertEqual(sizeof_fmt.sizeof_fmt(val), '1.0KiB')
        self.assertEqual(sizeof_fmt.sizeof_fmt(1225), '1.2KiB')
        val *= 1024;
        self.assertEqual(sizeof_fmt.sizeof_fmt(val), '1.0MiB')
        val *= 1024;
        self.assertEqual(sizeof_fmt.sizeof_fmt(val), '1.0GiB')
        val *= 1024;
        self.assertEqual(sizeof_fmt.sizeof_fmt(val), '1.0TiB')
        val *= 1024;
        self.assertEqual(sizeof_fmt.sizeof_fmt(val), '1.0PiB')
        val *= 1024;
        self.assertEqual(sizeof_fmt.sizeof_fmt(val), '1.0EiB')
        val *= 1024;
        self.assertEqual(sizeof_fmt.sizeof_fmt(val), '1.0ZiB')
        val *= 1024;
        self.assertEqual(sizeof_fmt.sizeof_fmt(val), '1.0YiB')
        val *= 1024;
        self.assertEqual(sizeof_fmt.sizeof_fmt(val), '1024.0YiB')

    def test_create_all_pairs(self):
        pass

def main():
    unittest.main()

if __name__ == "__main__":
    main()
