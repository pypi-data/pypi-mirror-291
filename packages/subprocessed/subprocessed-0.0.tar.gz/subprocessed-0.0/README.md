# subprocessed

Execute a function in a subprocess instead of using the main process.

It allows you to protect your main process from ugly things done in the
functionalities you are using:
- Global variables definition.
- `sys.path` modification.
- Segmentation fault and other wild crashes.
- Static C/C++ variables.
- Fortran 77 `COMMON`.
- Etc.

## Install

Install `subprocessed` from `pip`:
```sh
pip install subprocessed
```

## Usage

### Decorate your function with `subprocessed`

After installation, you can use the `subprocessed` decorator as follow:
```python
from subprocessed import subprocessed

@subprocessed
def do_ugly_things(a: int, b: str, c: float):
    """Function hiding ugly thing done by the ``ugly`` module."""
    import ugly # Hide also your imports!
    return ugly.do_horrible_things(parameters)

# Call serenely your module
result1, output1 = do_ugly_things(1, "dummy", c=3.7)
result2, output2 = do_ugly_things(2, "meh", c=100.5)
```

#### Get what's happening in the decorated function seamlessly

Everything happening in the subprocessed function is transmitted to the main
process:
- Returned values.
- Raised Exceptions.
- Send warnings.
- Proper exit with zero exit code.

#### Check if the subprocess is alive... or not

By default, the subprocess status is automatically checked every second.
You can control that with the `check_delay` parameter when decorating your
function.

```python
from subprocessed import subprocessed
@subprocessed(check_delay=0.1)  # Check the subprocess every 100 ms
def do_ugly_things():
    pass
```

If the subprocess has died, a `multiprocessing.ProcessError` is raised.

#### Deactivate the subprocess checking

You can also completely deactivate the verification with `None`:

```python
from subprocessed import subprocessed
@subprocessed(check_delay=None)  # No checking
def do_ugly_things():
    pass
```

> Remember when doing that: if the subprocess crashes, the execution of the main
> process will be blocked.

## Known limitations

### Serializable inputs and outputs

Transmitting objects between processes is possible only if they are serializable.

### Daemon child processes cannot create children processes

An exception will be raised if you try to execute a subprocessed function in a
daemon child process.

### Only compatible with POSIX systems

This forks Python process so it is not possible to use it on Windows and MacOS.
