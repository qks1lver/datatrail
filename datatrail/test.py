#!/usr/bin/env python3

"""
Copyright 2018 Jiun Yang Yen

MIT License

"""

import logger
import unittest
import os
from datetime import datetime

class TestLogger(unittest.TestCase):

    def test_init(self):

        if os.path.isfile(logger._dtrail):
            os.remove(logger._dtrail)

        self.assertTrue(logger.init())
        self.assertTrue(os.path.isfile(logger._dtrail))
        self.assertEqual(logger._dtrail_log, os.path.abspath(logger._dtrail))
        self.assertFalse(logger.init())
        self.assertTrue(logger.init(force=True))
        self.assertTrue(os.path.isfile(logger._dtrail))

        with open(logger._dtrail, 'r') as f:
            _ = f.readline()
            l = f.readline()
        exp_l = '\tInitialized at %s\n' % logger._dtrail_log
        self.assertEqual(l, exp_l)

        os.remove(logger._dtrail)

    def test_run(self):

        self.assertFalse(os.path.isfile(logger._dtrail))
        self.assertEqual(logger.run(max, [2, 1, 3]), -1)
        logger.init()
        self.assertEqual(logger.run(max, [2, 1, 3]), 3)
        self.assertEqual(logger.run(min, [2, 1, 3]), 1)

        with open(logger._dtrail_log, 'r') as f:
            for i,l in enumerate(f):
                if i == 4:
                    self.assertEqual(l, '\tmax([2, 1, 3],)\n')
                elif i == 5:
                    self.assertEqual(l, '\t@RETURN=3\n')
                elif i == 8:
                    self.assertEqual(l, '\tmin([2, 1, 3],)\n')
                elif i == 9:
                    self.assertEqual(l, '\t@RETURN=1\n')

        os.remove(logger._dtrail)

    def test_make(self):

        p_file = 'test.txt'
        if os.path.isfile(p_file):
            os.remove(p_file)
        if os.path.isfile(logger._dtrail):
            os.remove(logger._dtrail)

        self.assertEqual(logger.make(p_file), -1)
        logger.init()
        self.assertEqual(logger.make(p_file), 1)
        self.assertTrue(os.path.isfile(p_file))
        self.assertEqual(logger.make(p_file), 0)
        self.assertEqual(logger.make(p_file, overwrite=True), 1)
        os.remove(p_file)
        os.remove(logger._dtrail)

    def test_remove(self):

        p_file = self.make_file('test')
        if os.path.isfile(logger._dtrail):
            os.remove(logger._dtrail)

        self.assertTrue(os.path.isfile(p_file))
        self.assertEqual(logger.remove(p_file), -1)
        logger.init()
        self.assertEqual(logger.remove(p_file), 1)
        self.assertFalse(os.path.isfile(p_file))
        self.assertEqual(logger.remove(p_file), 0)
        os.remove(logger._dtrail)

    def test_rename(self):

        p_file = self.make_file('test.txt')
        p_dest = 'tset.txt'
        if os.path.isfile(logger._dtrail):
            os.remove(logger._dtrail)

        self.assertTrue(os.path.isfile(p_file))
        self.assertFalse(os.path.isfile(p_dest))
        self.assertEqual(logger.rename(p_file, p_dest), -1)
        logger.init()
        self.assertEqual(logger.rename(p_dest, p_dest), -2)
        self.assertEqual(logger.rename(p_file, p_dest), 1)
        self.assertFalse(os.path.isfile(p_file))
        self.assertTrue(os.path.isfile(p_dest))
        os.remove(logger._dtrail)
        os.remove(p_dest)

    def test_copy(self):

        p_test0 = self.make_file('test0')
        if os.path.isfile('test1'):
            os.remove('test1')
        if not os.path.isdir('testdir'):
            os.makedirs('testdir')

        self.assertEqual(logger.copy(p_test0, 'test1'), -1)
        logger.init()
        self.assertEqual(logger.copy('test1'), -2)
        self.assertEqual(logger.copy(p_test0, 'nosuchdir/'), 0)
        p_test0copy = logger.copy(p_test0)
        self.assertIn('/test0-copy%s'%datetime.now().strftime('%Y%m%d%H%M'), p_test0copy)
        p_test1 = logger.copy(p_test0, 'test1')
        self.assertEqual(p_test1, os.path.abspath('test1'))
        p_test1copy = logger.copy(p_test0, 'test1')
        self.assertIn('/test1-copy%s' % datetime.now().strftime('%Y%m%d%H%M'), p_test1copy)
        p_test0dircopy = logger.copy(p_test0, 'testdir')
        self.assertIn('testdir/test0-copy%s' % datetime.now().strftime('%Y%m%d%H%M'), p_test0dircopy)

        os.remove(logger._dtrail)
        os.remove(p_test0)
        os.remove(p_test0copy)
        os.remove(p_test1)
        os.remove(p_test1copy)
        os.remove(p_test0dircopy)
        os.removedirs('testdir')

    def test_move(self):

        p_test = self.make_file('test0')
        if os.path.isfile('test1'):
            os.remove('test1')
        if not os.path.isdir('testdir'):
            os.makedirs('testdir')

        self.assertEqual(logger.move(p_test, 'testdir'), -1)
        logger.init()
        self.assertEqual(logger.move('test1', 'testdir'), -2)
        self.assertEqual(logger.move(p_test, 'nosuchdir/'), 0)
        p_test = logger.move(p_test, 'testdir')
        self.assertIn('testdir/test0', p_test)
        self.assertTrue(os.path.isfile(p_test))
        self.assertFalse(os.path.isfile('test0'))
        p_test = logger.move(p_test, 'test1')
        self.assertTrue(os.path.isfile('test1'))
        self.assertFalse(os.path.isfile('testdir/test0'))
        self.assertEqual(p_test, os.path.abspath('test1'))
        self.assertEqual(logger.move(p_test, 'test1'), -3)
        _ = self.make_file('test0')
        self.assertEqual(logger.move(p_test, 'test0'), -4)
        p_test = logger.move(p_test, 'test0', overwrite=True)
        self.assertIn('test0', p_test)
        self.assertFalse(os.path.isfile('test1'))

        os.remove(logger._dtrail)
        os.removedirs('testdir')
        os.remove(p_test)

    def make_file(self, fname):

        with open(fname, 'w+') as f:
            f.write('')

        return(fname)

if __name__ == '__main__':
    unittest.main()
