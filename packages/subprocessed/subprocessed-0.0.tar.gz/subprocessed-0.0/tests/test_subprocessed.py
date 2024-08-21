# -*- coding: utf-8 -*-

"""Tests of the ``subprocessed`` decorator."""

import multiprocessing
import sys
import warnings

import pytest

from subprocessed import subprocessed


def test_no_input_no_output():
    """Test the execution of a function without any input or output."""

    @subprocessed(check_delay=None)
    def _no_input_no_output():
        print("The function is executed")

    output = _no_input_no_output()  # pylint: disable=assignment-from-no-return
    assert output is None


def test_input_no_output():
    """Test the execution of a function with input and without output."""

    @subprocessed(check_delay=None)
    def _input_no_output(elt):
        print(f"Received elements: {elt!r}")

    output = _input_no_output(3)  # pylint: disable=assignment-from-no-return
    assert output is None
    output = _input_no_output(elt=3)  # pylint: disable=assignment-from-no-return
    assert output is None

    with pytest.raises(TypeError) as exc_info:
        _input_no_output()  # pylint: disable=no-value-for-parameter
    assert str(exc_info.value).endswith(
        "_input_no_output() missing 1 required positional argument: 'elt'"
    )


def test_no_input_output():
    """Test the execution of a function without input and with output."""

    @subprocessed(check_delay=None)
    def _no_input_output():
        return 3

    output = _no_input_output()
    assert output == 3


def test_input_output():
    """Test the execution of a function with both input and output."""

    @subprocessed(check_delay=None)
    def _input_output(elt_a, elt_b):
        return elt_a * elt_b, 4

    multi, const = _input_output(3, 4)
    assert multi == 12
    assert const == 4
    multi, const = _input_output(elt_a=3, elt_b=4)
    assert multi == 12
    assert const == 4


def test_exception():
    """Test the execution of a function that raise an exception."""

    @subprocessed(check_delay=None)
    def _exception():
        raise ValueError("Dummy exception raised")

    with pytest.raises(ValueError) as exc_info:
        _exception()
    assert str(exc_info.value) == "Dummy exception raised"


def test_return_exception():
    """Test the execution of a function that return an exception."""

    @subprocessed(check_delay=None)
    def _return_exception():
        return ValueError

    exception = _return_exception()
    assert exception is ValueError


def test_cmp_process():
    """Test that the process ID is different in the function."""
    main_process = multiprocessing.current_process()

    @subprocessed(check_delay=None)
    def _cmp_process():
        sub_process = multiprocessing.current_process()
        return main_process != sub_process

    assert _cmp_process()


def test_exit():
    """Test that the exit of the subprocess exit the main process."""

    @subprocessed
    def _exit():
        sys.exit(0)

    with pytest.raises(SystemExit):
        _exit()


def test_crash():
    """Test that the crash of the subprocess do not induce a deadlock."""
    exit_code = 1

    @subprocessed
    def _crash():
        sys.exit(exit_code)

    with pytest.raises(multiprocessing.ProcessError) as exc_info:
        _crash()
    assert str(exc_info.value) == f"Subprocess ended with exit code {exit_code}"


def test_warnings():
    """Test the execution of a function that emit warnings."""

    @subprocessed(check_delay=None)
    def _warnings():
        for i in range(3):
            warnings.warn(f"Warning number {i}", RuntimeWarning)
        for i in range(5):
            warnings.warn(f"Warning number {i}", UserWarning)

    with pytest.warns((RuntimeWarning, UserWarning)) as records:
        _warnings()
    assert len(records) == 3 + 5
    for i in range(3):
        assert records[i].category == RuntimeWarning
        assert records[i].message.args[0] == f"Warning number {i}"
    for i in range(5):
        assert records[3 + i].category == UserWarning
        assert records[3 + i].message.args[0] == f"Warning number {i}"
