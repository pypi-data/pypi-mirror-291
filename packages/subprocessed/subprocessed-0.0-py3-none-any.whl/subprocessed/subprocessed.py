# -*- coding: utf-8 -*-

"""Decorate a function to execute it inside a subprocess.

The subprocessed function wil not pollute the main process with global
variables, Fortran 77 common variables and so on.
"""

import functools
import logging
import multiprocessing
import sys
import traceback
import typing
import warnings


def _subcall(
    outputs_sender,
    exception_sender,
    traceback_sender,
    warnings_sender,
    subfunction: typing.Callable,
    *subargs,
    **subkwargs,
):
    """Executor of the function in the subprocess.

    Execute the given function with all given inputs and send back every output,
    warnings or exception in the given pipes.
    """
    with warnings.catch_warnings(record=True) as warns:
        try:
            warnings.simplefilter("always")
            outputs = subfunction(*subargs, **subkwargs)
            exception_sender.send(None)
            traceback_sender.send(None)
            outputs_sender.send(outputs)
            warnings_sender.send(warns)
        except Exception as exception:  # pylint: disable=broad-except
            exception_sender.send(exception)
            traceback_sender.send(traceback.format_exc())
            outputs_sender.send(None)
            warnings_sender.send(warns)


def subprocessed(
    function: typing.Union[typing.Callable, None] = None,
    *,
    check_delay: typing.Union[float, None] = 1,
) -> typing.Callable:
    """Decorate a function to execute it inside a subprocess.

    The subprocessed function wil not pollute the main process with global
    variables, Fortran 77 common variables and so on.

    Parameters
    ----------
    check_delay
        Subprocess crash checking frequency in second. By default, the
        subprocess is checked every second. Use ``None`` if you want to
        deactivate the subprocess checking.

    Raises
    ------
    multiprocessing.ProcessError
        If the subprocess crash.
    """
    logger = logging.getLogger(__name__)

    def _inner(_function):
        @functools.wraps(_function)
        def _wrapper(*args, **kwargs):
            # Create the communication pipes
            exception_pipe = multiprocessing.Pipe(duplex=False)
            backtrace_pipe = multiprocessing.Pipe(duplex=False)
            outputs_pipe = multiprocessing.Pipe(duplex=False)
            warnings_pipe = multiprocessing.Pipe(duplex=False)

            # Create the subprocess and start it
            logger.debug("subprocessed: create the subprocess")
            process = multiprocessing.Process(
                target=_subcall,
                args=[
                    outputs_pipe[1],
                    exception_pipe[1],
                    backtrace_pipe[1],
                    warnings_pipe[1],
                    _function,
                ]
                + list(args),
                kwargs=dict(kwargs),
            )
            logger.debug("subprocessed: start the subprocess")
            process.start()

            # Wait for something in the pipe and check the subprocess status
            if check_delay is None:
                logger.debug("subprocessed: deactivate subprocess status checking")
            else:
                logger.debug("subprocessed: check the subprocess every %g seconds", check_delay)
            while not exception_pipe[0].poll(timeout=check_delay):
                # Look if the subprocess has ended
                logger.debug("subprocessed: check the subprocess status")
                if process.exitcode is not None:
                    # Exit the parent process if the child process exit properly
                    if process.exitcode == 0:
                        logger.debug("subprocessed: the subprocess has exited")
                        sys.exit(0)

                    # Raise an exception if the child process crashed
                    logger.debug("subprocessed: the subprocess has crashed")
                    raise multiprocessing.ProcessError(
                        f"Subprocess ended with exit code {process.exitcode}"
                    )

            # Get the output in the pipe
            logger.debug("subprocessed: receive the outputs from the pipes")
            exception = exception_pipe[0].recv()
            backtrace = backtrace_pipe[0].recv()
            outputs = outputs_pipe[0].recv()
            warns = warnings_pipe[0].recv()

            # Wait the process to finish
            # Note: 'join' must be called after 'recv' because, if you are
            #       sending/receiving a large object, you will fall into a
            #       deadlock. It cannot be tested so be careful!
            logger.debug("subprocessed: wait the subprocess to finish")
            process.join()

            # Send the warning messages
            logger.debug("subprocessed: check if warnings were emitted in the subprocess")
            if warns:
                logger.debug("subprocessed: emit the warnings of the subprocess")
                for warn in warns:
                    warnings.showwarning(
                        message=warn.message,
                        category=warn.category,
                        filename=warn.filename,
                        lineno=warn.lineno,
                        file=warn.file,
                        line=warn.line,
                    )

            # Raise the exception of the function
            logger.debug("subprocessed: check if the subprocess raised an exception")
            if exception is not None:
                logger.debug(
                    "subprocessed: an exception occurs with the following backtrace:\n%s",
                    backtrace,
                )
                logger.debug("subprocessed: raise the exception of the subprocess")
                raise exception

            # End the subprocess
            logger.debug("subprocessed: terminate the subprocess")
            process.terminate()

            logger.debug("subprocessed: return the output")
            return outputs

        return _wrapper

    # Manage decorator's optional parameters
    if function is None:
        return _inner
    return _inner(function)


__all__ = ["subprocessed"]
