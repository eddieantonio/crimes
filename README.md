# Language bender

Blur the line between C and Python

```c
/* hello.c */
#include <stdio.h>

void hello(void) {
    printf("Hello, world from C!\n");
}
```

```python
import language_bender
language_bender.install()

from hello import hello

hello()  # prints "Hello, world from C!"
```

## What if I am a terrible C programmer?

Not to worry! `language_bender` will print your syntax errors in Python:

```c
/* hello.c */
#include <stdio.h>

/* missing ')' on the next line: */
void hello(void {
    printf("Hello, world from C!\n");
}
```

```python
import language_bender
language_bender.install()

from hello import hello  # raises an error here
```

Gives you this error:

```
Traceback (most recent call last):
  File "/Users/eddie/Programming/language-bender/example.py", line 6, in <module>
    from hello import hello  # type: ignore
    ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/eddie/Programming/language-bender/hello.c", line 5, in hello.c
    void hello(void {
                    ^
language_bender.exceptions.CCompileError: expected ';', ',' or ')' before '{' token
```
