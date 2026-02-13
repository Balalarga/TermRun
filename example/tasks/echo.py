""" Simple echo functions
"""
import invoke

from termrun import term_runnable


@term_runnable(title="Hello World")
def generic_echo(ctx: invoke.Context):
    ctx.run("echo Hello World")


@term_runnable(title="PosixOnly. Hello World", os_filter="posix")
def echo_for_posix(ctx: invoke.Context):
    ctx.run("echo Hello Posix World")

@term_runnable(title="WindowsOnly. Hello World", os_filter="nt")
def echo_for_windows(ctx: invoke.Context):
    ctx.run("echo Hello Windows World")
