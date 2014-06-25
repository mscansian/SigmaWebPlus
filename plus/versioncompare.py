#!/usr/bin/env python
 
# This code was written by Krzysztof Kowalczyk (http://blog.kowalczyk.info)
# and is placed in public domain.
 
def v2fhelper(v, suff, version, weight):
    parts = v.split(suff)
    if 2 != len(parts):
        return v
    version[4] = weight
    version[5] = parts[1]
    return parts[0]
 
# Convert a Mozilla-style version string into a floating-point number
#   1.2.3.4, 1.2a5, 2.3.4b1pre, 3.0rc2, etc
def version2float(v):
    version = [
        0, 0, 0, 0, # 4-part numerical revision
        4, # Alpha, beta, RC or (default) final
        0, # Alpha, beta, or RC version revision
        1  # Pre or (default) final
    ]
    parts = v.split("pre")
    if 2 == len(parts):
        version[6] = 0
        v = parts[0]
 
    v = v2fhelper(v, "a",  version, 1)
    v = v2fhelper(v, "b",  version, 2)
    v = v2fhelper(v, "rc", version, 3)
 
    parts = v.split(".")[:4]
    for (p, i) in zip(parts, range(len(parts))):
        version[i] = p
    ver = float(version[0])
    ver += float(version[1]) / 100.
    ver += float(version[2]) / 10000.
    ver += float(version[3]) / 1000000.
    ver += float(version[4]) / 100000000.
    ver += float(version[5]) / 10000000000.
    ver += float(version[6]) / 1000000000000.
    return ver
 
 
# Return True if ver1 > ver2 using semantics of comparing version
# numbers
def ProgramVersionGreater(ver1, ver2):
    v1f = version2float(ver1)
    v2f = version2float(ver2)
    return v1f > v2f
 
def tests():
    assert ProgramVersionGreater("1", "0.9")
    assert ProgramVersionGreater("0.0.0.2", "0.0.0.1")
    assert ProgramVersionGreater("1.0", "0.9")
    assert ProgramVersionGreater("2.0.1", "2.0.0")
    assert ProgramVersionGreater("2.0.1", "2.0")
    assert ProgramVersionGreater("2.0.1", "2")
    assert ProgramVersionGreater("0.9.1", "0.9.0")
    assert ProgramVersionGreater("0.9.2", "0.9.1")
    assert ProgramVersionGreater("0.9.11", "0.9.2")
    assert ProgramVersionGreater("0.9.12", "0.9.11")
    assert ProgramVersionGreater("0.10", "0.9")
    assert ProgramVersionGreater("2.0", "2.0b35")
    assert ProgramVersionGreater("1.10.3", "1.10.3b3")
    assert ProgramVersionGreater("88", "88a12")
    assert ProgramVersionGreater("0.0.33", "0.0.33rc23")
    print("All tests passed")
 
if __name__ == "__main__":
    tests()