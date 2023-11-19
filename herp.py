from language_bender.unorganized import compile_and_run

if __name__ == "__main__":
    libhello = compile_and_run("hello.c")
    libhello.hello()
