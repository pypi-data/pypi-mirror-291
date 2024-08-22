"""
Modified Base32 encoding that doesn't use padding and keeps sorting order.

Based on base64 standard library module, modified to use Douglas Crockford's
alphabet (but not other features).
"""

from typing import Final

P32_ALPHABET: Final = "0123456789abcdefghjkmnpqrstvwxyz"

_encode_table = None
_decode_table = None


def p32encode(s: bytes | bytearray) -> str:
    """
    Encodes bytes-like objects using Base32 encoding with Crockford's alphabet.
    """

    if not isinstance(s, bytes | bytearray):
        raise TypeError(f"a bytes or bytearray is required, not '{type(s)}'")

    global _encode_table

    if _encode_table is None:
        _encode_table = [a + b for a in P32_ALPHABET for b in P32_ALPHABET]

    leftover = len(s) % 5
    # Pad the last quantum with zero bits if necessary
    if leftover:
        s = s + b'\0' * (5 - leftover)  # Don't use += !

    encoded = ""
    for i in range(0, len(s), 5):
        c = int.from_bytes(s[i: i + 5], byteorder="big")
        encoded += (
            _encode_table[c >> 30] +           # bits 1 - 10
            _encode_table[(c >> 20) & 0x3ff] + # bits 11 - 20
            _encode_table[(c >> 10) & 0x3ff] + # bits 21 - 30
            _encode_table[c & 0x3ff]           # bits 31 - 40
        )

    # Adjust for any leftover partial quanta
    if leftover == 1:
        encoded = encoded[:-6]
    elif leftover == 2:
        encoded = encoded[:-4]
    elif leftover == 3:
        encoded = encoded[:-3]
    elif leftover == 4:
        encoded = encoded[:-1]

    return encoded


def p32decode(s: str) -> bytes:
    """
    Decodes bytes from Base32 encoding with Crockford's alphabet.
    """

    global _decode_table

    if _decode_table is None:
        _decode_table = {v: k for k, v in enumerate(P32_ALPHABET)}

    s = s.lower()

    # Calculate "padding" we should use
    leftover = len(s) % 8
    padchars = 8 - leftover if leftover else 0
    if padchars not in {0, 1, 3, 4, 6}:
        raise ValueError("Incorrect padding")

    # Now decode the full quanta
    decoded = bytearray()
    for i in range(0, len(s), 8):
        quanta = s[i : i + 8]
        acc = 0
        try:
            for c in quanta:
                acc = (acc << 5) + _decode_table[c]
        except KeyError:
            raise ValueError(f'Non-base32 digit found: "{c!r}"') from None
        decoded += acc.to_bytes(5)  # big endian

    if padchars and decoded:
        acc <<= 5 * padchars
        last = acc.to_bytes(5)  # big endian
        leftover = (43 - 5 * padchars) // 8  # 1: 4, 3: 3, 4: 2, 6: 1
        decoded[-5:] = last[:leftover]

    return bytes(decoded)
