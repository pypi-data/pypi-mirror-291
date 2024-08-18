import contextlib
import io
import json
import os
import platform
import tempfile
import time
from unittest import TestCase
from unittest.mock import (
    call,
    patch,
)

from repype.status import Status, StatusReader
from . import testsuite


def wait_for_watchdog():
    timeout = float(os.environ.get('REPYPE_WATCHDOG_TIMEOUT', 0.1))
    time.sleep(timeout)


class Status__init(TestCase):

    def test__parent_path_none(self):
        with self.assertRaises(AssertionError):
            Status()

    @testsuite.with_temporary_paths(2)
    def test__parent_path_not_none(self, path1, path2):
        status = Status(path = path1)
        with self.assertRaises(AssertionError):
            Status(parent = status, path = path2)

    @testsuite.with_temporary_paths(1)
    def test__with_path(self, path):
        status = Status(path = path)
        self.assertEqual(status.path, path)
        self.assertIsNone(status.parent)

    @testsuite.with_temporary_paths(1)
    def test__with_parent(self, path):
        status1 = Status(path = path)
        status2 = Status(parent = status1)
        self.assertIs(status2.parent, status1)
        self.assertIsNone(status2.path)


class Status__root(TestCase):

    @testsuite.with_temporary_paths(1)
    def test__no_parent(self, path):
        status = Status(path = path)
        self.assertIs(status.root, status)

    @testsuite.with_temporary_paths(1)
    def test__with_parent(self, path):
        status1 = Status(path = path)
        status2 = Status(parent = status1)
        self.assertIs(status2.root, status1)


class Status__filepath(TestCase):

    @testsuite.with_temporary_paths(1)
    def test__no_parent(self, path):
        status = Status(path = path)
        self.assertEqual(status.filepath, path / f'{status.id}.json')

    @testsuite.with_temporary_paths(1)
    def test__with_parent(self, path):
        status1 = Status(path = path)
        status2 = Status(parent = status1)
        self.assertEqual(status2.filepath, path / f'{status2.id}.json')


class Status__write_intermediate(TestCase):

    @testsuite.with_temporary_paths(1)
    def test_write(self, path):
        status = Status(path = path)
        status.write('test1')
        status.write('test2')
        with open(status.filepath) as file:
            data = json.load(file)
            self.assertEqual(data, ['test1', 'test2'])

    @testsuite.with_temporary_paths(1)
    def test_write_intermediate(self, path):
        status = Status(path = path)
        status.write('write')
        status.intermediate('intermediate')
        with open(status.filepath) as file:
            data = json.load(file)
            self.assertEqual(len(data), 2)
            self.assertEqual(data[0], 'write')
            self.assertEqual(list(data[1].keys()), ['expand', 'content_type'])
            self.assertEqual(data[1]['content_type'], 'intermediate')
        with open(data[1]['expand']) as file:
            data = json.load(file)
            self.assertEqual(data, ['intermediate'])

    @testsuite.with_temporary_paths(1)
    def test_write_intermediate_write(self, path):
        status = Status(path = path)
        status.write('write1')
        status.intermediate('intermediate')
        status.write('write2')
        with open(status.filepath) as file:
            data = json.load(file)
            self.assertEqual(data, ['write1', 'write2'])

    @testsuite.with_temporary_paths(1)
    def test_write_intermediate_none(self, path):
        status = Status(path = path)
        status.write('write1')
        status.intermediate('intermediate')
        status.intermediate(None)
        with open(status.filepath) as file:
            data = json.load(file)
            self.assertEqual(data, ['write1'])


class Status__derive(TestCase):

    @testsuite.with_temporary_paths(1)
    def test(self, path):
        status = Status(path = path)
        child = status.derive()
        self.assertEqual(status.data, [dict(expand = str(child.filepath))])
        self.assertEqual(child.data, [])
        self.assertIs(child.parent, status)


class Status__get(TestCase):

    def setUp(self):
        self.tempdir = tempfile.TemporaryDirectory()
        self.cwd = os.getcwd()
        os.chdir(self.tempdir.name)

    def tearDown(self):
        self.tempdir.cleanup()
        os.chdir(self.cwd)

    @testsuite.with_temporary_paths(1)
    def test_instance(self, path):
        status1 = Status(path = path)
        status2 = Status.get(status1)
        self.assertIs(status1, status2)

    def test_none(self):
        stdout = io.StringIO()
        with contextlib.redirect_stdout(stdout):
            status = Status.get()
        self.assertTrue(stdout.getvalue().startswith('Status written to: /'))
        self.assertTrue(stdout.getvalue().endswith(f'/.status/{status.id}.json\n'))
        status.update()
        self.assertEqual(os.listdir('.'), ['.status'])
        self.assertEqual(os.listdir('.status'), [f'{status.id}.json'])


class Status__progress(TestCase):

    @testsuite.with_temporary_paths(1)
    def test(self, path):
        intermediate_path = None
        status = Status(path = path)
        for item_idx, item in enumerate(status.progress(range(3), details = 'details')):

            if intermediate_path is None:
                with open(status.filepath) as file:
                    data = json.load(file)
                    intermediate_path = data[0]['expand']
                    
            with open(intermediate_path) as file:
                data = json.load(file)
                self.assertEqual(item, item_idx)
                self.assertEqual(
                    data,
                    [
                        dict(
                            info = 'progress',
                            details = 'details',
                            progress = item_idx / 3,
                            step = item_idx,
                            max_steps = 3,
                        ),
                    ],
                )

        # Verify that there have been three iterations, i.e. `item_idx = 0`, `item_idx = 1`, `item_idx = 2`
        self.assertEqual(item_idx, 2)
                    
        with open(status.filepath) as file:
            data = json.load(file)
            self.assertEqual(data, list())

    @testsuite.with_temporary_paths(1)
    def test_break(self, path):
        intermediate_path = None
        status = Status(path = path)

        for item_idx, item in (enumerate(status.progress(range(3), details = 'details'))):

            if intermediate_path is None:
                with open(status.filepath) as file:
                    data = json.load(file)
                    intermediate_path = data[0]['expand']
                    
            with open(intermediate_path) as file:
                data = json.load(file)
                self.assertEqual(item, item_idx)
                self.assertEqual(
                    data,
                    [
                        dict(
                            info = 'progress',
                            details = 'details',
                            progress = item_idx / 3,
                            step = item_idx,
                            max_steps = 3,
                        ),
                    ],
                )

            break

        # Verify that there has been one iterations, i.e. `item_idx = 0`
        self.assertEqual(item_idx, 0)
        
        with open(status.filepath) as file:
            data = json.load(file)
            self.assertEqual(data, list())

    @testsuite.with_temporary_paths(1)
    def test_len_override(self, path):
        status = Status(path = path)
        with self.assertRaises(AssertionError):
            for item in status.progress(range(3), len_override = 2):
                pass

        with open(status.filepath) as file:
            data = json.load(file)
            self.assertEqual(data, list())

    @testsuite.with_temporary_paths(1)
    def test_empty(self, path):
        status = Status(path = path)
        for item in status.progress(list()):
            pass

        # Verify that there have been no iterations
        self.assertFalse('item' in locals())

        with open(status.filepath) as file:
            data = json.load(file)
            self.assertEqual(data, list())

    @testsuite.with_temporary_paths(1)
    def test_error(self, path):
        intermediate_path = None
        status = Status(path = path)

        with self.assertRaises(testsuite.TestError):
            for item_idx, item in (enumerate(status.progress(range(3), details = 'details'))):

                if intermediate_path is None:
                    with open(status.filepath) as file:
                        data = json.load(file)
                        intermediate_path = data[0]['expand']
                        
                with open(intermediate_path) as file:
                    data = json.load(file)
                    self.assertEqual(item, item_idx)
                    self.assertEqual(
                        data,
                        [
                            dict(
                                info = 'progress',
                                details = 'details',
                                progress = item_idx / 3,
                                step = item_idx,
                                max_steps = 3,
                            ),
                        ],
                    )

                raise testsuite.TestError()

        # Verify that there has been one iterations, i.e. `item_idx = 0`
        self.assertEqual(item_idx, 0)
        
        with open(status.filepath) as file:
            data = json.load(file)
            self.assertEqual(data, list())


class StatusReader__init(TestCase):

    def setUp(self):
        self.tempdir = tempfile.TemporaryDirectory()
        self.status1 = Status(path = self.tempdir.name)
        self.status1.write('write1')
        self.status2 = self.status1.derive()
        self.status2.write('write2')

    def tearDown(self):
        self.tempdir.cleanup()

    @patch.object(StatusReader, 'handle_new_status')
    def test_without_intermediates(self, mock_handle_new_status):
        with StatusReader(self.status1.filepath) as status:
            self.assertEqual(status, ['write1', ['write2']])

            wait_for_watchdog()
            self.assertEqual(
                mock_handle_new_status.call_args_list,
                [
                    call([['write1', ['write2']]], [0], 'write1'),
                    call([['write1', ['write2']], ['write2']], [1, 0], 'write2'),
                ]
            )

            mock_handle_new_status.reset_mock()
            self.status2.write('write3')
            wait_for_watchdog()
            self.assertEqual(status, ['write1', ['write2', 'write3']])
            self.assertEqual(
                mock_handle_new_status.call_args_list,
                [
                    call([['write1', ['write2', 'write3']], ['write2', 'write3']], [1, 1], 'write3'),
                ]
            )

            mock_handle_new_status.reset_mock()
            status3 = self.status1.derive()
            status3.write('write4')
            wait_for_watchdog()
            self.assertEqual(status, ['write1', ['write2', 'write3'], ['write4']])
            self.assertEqual(
                mock_handle_new_status.call_args_list,
                [
                    call([['write1', ['write2', 'write3'], ['write4']], ['write4']], [2, 0], 'write4'),
                ]
            )

            mock_handle_new_status.reset_mock()
            self.status1.write('write5')
            wait_for_watchdog()
            self.assertEqual(status, ['write1', ['write2', 'write3'], ['write4'], 'write5'])
            self.assertEqual(
                mock_handle_new_status.call_args_list,
                [
                    call([['write1', ['write2', 'write3'], ['write4'], 'write5']], [3], 'write5'),
                ]
            )

    @patch.object(StatusReader, 'handle_new_status')
    def test_with_intermediates(self, mock_handle_new_status):
        with StatusReader(self.status1.filepath) as status:
            self.assertEqual(status, ['write1', ['write2']])

            self.status2.write('write3')
            wait_for_watchdog()
            self.assertEqual(status, ['write1', ['write2', 'write3']])

            mock_handle_new_status.reset_mock()
            self.status2.intermediate('interm1')
            wait_for_watchdog()
            self.assertEqual(
                status,
                [
                    'write1',
                    [
                        'write2',
                        'write3',
                        dict(
                            content_type = 'intermediate',
                            content = ['interm1'],
                        ),
                    ],
                ],
            )
            self.assertEqual(
                mock_handle_new_status.call_args_list,
                [
                    call(
                        [
                            [
                                'write1',
                                [
                                    'write2',
                                    'write3',
                                    dict(
                                        content_type = 'intermediate',
                                        content = ['interm1'],
                                    ),
                                ],
                            ],
                            [
                                'write2',
                                'write3',
                                dict(
                                    content_type = 'intermediate',
                                    content = ['interm1'],
                                ),
                            ],
                        ],
                        [1, 2],
                        dict(
                            content_type = 'intermediate',
                            content = ['interm1'],
                        ),
                    ),
                ]
            )

            mock_handle_new_status.reset_mock()
            self.status2.intermediate('interm2')
            wait_for_watchdog()
            self.assertEqual(
                status,
                [
                    'write1',
                    [
                        'write2',
                        'write3',
                        dict(
                            content_type = 'intermediate',
                            content = ['interm2'],
                        ),
                    ],
                ],
            )
            self.assertEqual(
                mock_handle_new_status.call_args_list,
                [
                    call(
                        [
                            [
                                'write1',
                                [
                                    'write2',
                                    'write3',
                                    dict(
                                        content_type = 'intermediate',
                                        content = ['interm2'],
                                    ),
                                ],
                            ],
                            [
                                'write2',
                                'write3',
                                dict(
                                    content_type = 'intermediate',
                                    content = ['interm2'],
                                ),
                            ],
                        ],
                        [1, 2],
                        dict(
                            content_type = 'intermediate',
                            content = ['interm2'],
                        ),
                    ),
                ]
            )

            mock_handle_new_status.reset_mock()
            self.status2.intermediate(None)
            wait_for_watchdog()
            self.assertEqual(
                status,
                [
                    'write1',
                    [
                        'write2',
                        'write3',
                    ],
                ],
            )
            self.assertEqual(
                mock_handle_new_status.call_args_list,
                [
                    call(
                        [
                            [
                                'write1',
                                [
                                    'write2',
                                    'write3',
                                ],
                            ],
                            [
                                'write2',
                                'write3',
                            ],
                        ],
                        [1, 2],
                        dict(
                            content_type = 'intermediate',
                            content = None,
                        ),
                    ),
                ]
            )

            mock_handle_new_status.reset_mock()
            self.status2.write('write4')
            wait_for_watchdog()
            self.assertEqual(
                mock_handle_new_status.call_args_list,
                [
                    call(
                        [
                            [
                                'write1',
                                [
                                    'write2',
                                    'write3',
                                    'write4',
                                ],
                            ],
                            [
                                'write2',
                                'write3',
                                'write4',
                            ],
                        ],
                        [1, 2],
                        'write4',
                    ),
                ]
            )