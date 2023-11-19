# Crimes

Blur the line between C and Python.

First, write some C code:

```c
/* hello.c */
#include <stdio.h>

void hello(void) {
    printf("Hello world from C!\n");
}
```

Then import that C code into Python:

```python
import crimes

crimes.commit()

from hello import hello

hello()  # prints "Hello world from C!"
```

All you had to do is call `crimes.commit()`!

## What if I am a terrible C programmer?

Not to worry! `crimes` will print your syntax errors as part of the normal Python traceback:

```c
/* hello.c */
#include <stdio.h>

/* missing ')' on the next line: */
void hello(void {
    printf("Hello world from C!\n");
}
```

```python
import crimes

crimes.commit()

from hello import hello  # raises an error here
```

Gives you this error:

```
Traceback (most recent call last):
  File "/tmp/example.py", line 6, in <module>
    from hello import hello  # type: ignore
    ^^^^^^^^^^^^^^^^^^^^^^^
  File "/tmp/hello.c", line 5, in hello.c
    void hello(void {
                    ^
crimes.exceptions.CCompileError: expected ';', ',' or ')' before '{' token
```

# Install

> [!WARNING] This is currently pretty hacky.
> I provide absolutely no guarantee that this will work on your machine.
> Here's how I got it working on my machine, which running macOS.
> I highly doubt this library works at all on Windows.

First, install the library:

```sh
pip install crimes
```

Next, make sure you have a compatible version of GCC.
Any version of GCC 9.0 or greater should work. On most Linux distros,
you probably already have this installed. On macOS though... Apple
thought it was a good idea to symlink `gcc` to `clang`. This does not
work. So first, install _actual_ GCC using brew:

```sh
brew install gcc@13
```

Next, before using this module, make sure that `CC` is set to use
`gcc-13`. You can do this universally like this:

```sh
export CC=gcc-13
```

...but I prefer to do it per-process:

```sh
env CC=gcc-13 python3 my-program-that-commits-crimes.py
```


# Copying

Copyright © 2023 Eddie Antonio Santos. Apache-2.0 licensed. See
`LICENSE` for details. _Especially_ the Disclaimer of Warranty!
