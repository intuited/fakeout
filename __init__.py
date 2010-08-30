"""Context manager and higher-level function to provide output capturing."""
from contextlib import contextmanager

def fakeout_do(f, *args, **kwargs):
    """Calls `f` with `args` and `kwargs`; returns (result, output)."""
    from StringIO import StringIO
    fake_out = StringIO()
    with fakeout(fake_out):
        return f(*args, **kwargs), fake_out.getvalue()

@contextmanager
def fakeout(fake_out):
    """Standard output from the managed context is redirected to `fake_out`."""
    import sys
    real_out = sys.__dict__['stdout']
    sys.__dict__['stdout'] = fake_out
    yield
    sys.__dict__['stdout'] = real_out
