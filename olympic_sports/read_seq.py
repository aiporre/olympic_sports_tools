# This file was taken from the following gist, made by @psycharo :
# https://gist.github.com/psycharo/7e6422a491d93e1e3219/

import struct
from skimage import io
from simplejpeg import decode_jpeg, decode_jpeg_header

def read_header(ifile):
    feed = ifile.read(4)
    norpix = ifile.read(24)
    version = struct.unpack('@i', ifile.read(4))
    length = struct.unpack('@i', ifile.read(4))
    assert (length != 1024)
    descr = ifile.read(512)
    params = [struct.unpack('@i', ifile.read(4))[0] for i in range(0, 9)]
    fps = struct.unpack('@d', ifile.read(8))
    # skipping the rest
    ifile.read(432)
    image_ext = {100: 'raw', 102: 'jpg', 201: 'jpg', 1: 'png', 2: 'png'}
    return {'w': params[0], 'h': params[1],
            'bdepth': params[2],
            'ext': image_ext[params[5]],
            'format': params[5],
            'size': params[4],
            'true_size': params[8],
            'num_frames': params[6]}


def read_seq(path):
    ifile = open(path, 'rb')
    params = read_header(ifile)
    bytes = open(path, 'rb').read()

    # this is freaking magic, but it works
    extra = 8
    s = 1024
    seek = [0] * (params['num_frames'] + 1)
    seek[0] = 1024

    images = []

    # this crashes in the last iteration, so we reduce it by one iteration
    for i in range(0, params['num_frames'] - 1):
        tmp = struct.unpack_from('@I', bytes[s:s + 4])[0]
        s = seek[i] + tmp + extra
        if i == 0:
            val = struct.unpack_from('@B', bytes[s:s + 1])[0]
            if val != 0:
                s -= 4
            else:
                extra += 8
                s += 8
        seek[i + 1] = s
        nbytes = struct.unpack_from('@i', bytes[s:s + 4])[0]
        I = bytes[s + 4:s + nbytes]
        img = decode_jpeg(I)
        images.append(img)
    return images
