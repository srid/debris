# I keep utility and wrapper code here
# So simply do `from debris import foo' to use the feature `foo'

try:
    from cStringIO import StringIO
except ImportError:
    from StringIO import StringIO


def file_write_to_string(file_writer):
    """Call `file_writer' with a file-like object as argument and return
    the written contents of that file
    """
    sio = StringIO()
    
    try:
        file_writer(sio)
        text = sio.getvalue()
    finally:
        sio.close()
        
    return text
