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

crimes.install()

from hello import hello

hello()  # prints "Hello world from C!"
```

All you had to do is `crimes.commit()`!

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

crimes.install()

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
