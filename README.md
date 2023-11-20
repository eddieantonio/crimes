# Language bender

Blur the line between C and Python

```c
/* libhello.c */
#include <stdio.h>

void hello(void) {
    printf("Hello, world from C!\n");
}
```

```python
import language_bender
language_bender.install()

from libhello import hello

hello()  # prints "Hello, world from C!"
```
