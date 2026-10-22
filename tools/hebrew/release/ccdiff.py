#!/usr/bin/env python3
"""Compare crosscore frame dumps between cores, after reducing every pixel to RGB565 (cores differ
in pixel format, and XRGB8888 rounding is not a difference).

  ccdiff.py REF_DIR DIR... -> per shot: differing pixel count against REF_DIR, and PNGs of each
"""
import os, struct, sys, zlib

def load(path):
    d = open(path, 'rb').read()
    w, h = struct.unpack('<II', d[:8]); px = d[8:]
    out = []
    for i in range(w * h):
        b, g, r = px[i * 4], px[i * 4 + 1], px[i * 4 + 2]
        out.append(((r >> 3) << 11) | ((g >> 2) << 5) | (b >> 3))
    return w, h, out

def png(path, w, h, pix565):
    rows = []
    for y in range(h):
        row = bytearray([0])
        for x in range(w):
            v = pix565[y * w + x]
            row += bytes([((v >> 11) & 31) << 3, ((v >> 5) & 63) << 2, (v & 31) << 3])
        rows.append(bytes(row))
    def chunk(t, data):
        c = t + data
        return struct.pack('>I', len(data)) + c + struct.pack('>I', zlib.crc32(c) & 0xffffffff)
    open(path, 'wb').write(b'\x89PNG\r\n\x1a\n' + chunk(b'IHDR', struct.pack('>IIBBBBB', w, h, 8, 2, 0, 0, 0))
                          + chunk(b'IDAT', zlib.compress(b''.join(rows), 9)) + chunk(b'IEND', b''))

if len(sys.argv) < 3 or sys.argv[1] in ('-h', '--help'):
    sys.exit('usage: ccdiff.py REF_DIR DIR...')
for d in sys.argv[1:]:
    if not os.path.isdir(d):
        sys.exit('ccdiff.py: %s is not a directory' % d)
ref = sys.argv[1]
for d in [ref] + sys.argv[2:]:
    for f in sorted(os.listdir(d)):
        if f.endswith('.raw'):
            w, h, p = load(os.path.join(d, f)); png(os.path.join(d, f[:-4] + '.png'), w, h, p)
shots = sorted(f for f in os.listdir(ref) if f.endswith('.raw'))
print('%-10s' % 'shot' + ''.join('%14s' % os.path.basename(d.rstrip('/')) for d in sys.argv[2:]))
for s in shots:
    w, h, a = load(os.path.join(ref, s))
    cells = []
    for d in sys.argv[2:]:
        p = os.path.join(d, s)
        if not os.path.exists(p):
            cells.append('missing'); continue
        w2, h2, b = load(p)
        cells.append('size %dx%d' % (w2, h2) if (w2, h2) != (w, h) else str(sum(1 for x, y in zip(a, b) if x != y)))
    print('%-10s' % s[:-4] + ''.join('%14s' % c for c in cells))
