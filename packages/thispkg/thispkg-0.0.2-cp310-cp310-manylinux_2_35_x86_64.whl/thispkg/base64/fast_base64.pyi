from typing import Union

def b64encode(s: Union[bytes, bytearray, memoryview]) -> bytes:
    """
    Encode the bytes-like object s using Base64 and return a bytes object.
    """
    ...

def b64decode(s: Union[bytes, bytearray, memoryview, str]) -> bytes:
    """
    Decode the Base64 encoded bytes-like object or ASCII string s.
    Returns a bytes object.
    """
    ...

def urlsafe_b64encode(s: Union[bytes, bytearray, memoryview]) -> bytes:
    """
    Encode bytes-like object s using the URL- and filesystem-safe Base64 alphabet.
    Returns a bytes object.
    """
    ...

def urlsafe_b64decode(s: Union[bytes, bytearray, memoryview, str]) -> bytes:
    """
    Decode bytes-like object or ASCII string s using the URL- and filesystem-safe Base64 alphabet.
    Returns a bytes object.
    """
    ...
