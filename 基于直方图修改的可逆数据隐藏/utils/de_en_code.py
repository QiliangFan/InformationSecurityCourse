from numba import jit


def encode_to_bin(byte_list):
    """
    one byte for 8 bits
    """
    temp = ["{0:0>8}".format(bin(c).lstrip("0b")) for c in byte_list]
    result_str = "".join(temp)
    return result_str


def str_to_bytes(binary_str:str):
    """
    one byte for 8 bits
    """
    return bytes(binary_str, encoding="utf-8")