""" Simple echo functions
"""
import invoke

from termrun import term_runnable


@term_runnable(title="Hello World")
def build_win64_server_development(ctx: invoke.Context):
    ctx.run("echo Hello World")


@term_runnable(title="PosixOnly. Hello World", os_filter="posix")
def build_win64_server_development(ctx: invoke.Context):
    ctx.run("echo Hello World")

@term_runnable(title="WindowsOnly. Hello World", os_filter="nt")
def build_win64_server_development(ctx: invoke.Context):
    ctx.run("echo Hello World")
