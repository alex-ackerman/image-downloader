#!/usr/bin/env python3

import argparse
import os
from PIL import Image
from typing import Tuple, List, Callable

def main(input_dir: str, output_dir: str):
    print(f'[+] cropping images in dir {input_dir}')
    for filename, path in readdir(input_dir, lambda filename: filename.endswith('.jpg')):
        print(f' [+] {filename} ({path}) ... ', end='', flush=True)
        with Image.open(path) as im:
            rgb_im = im.convert('RGB')
            cropped = crop(rgb_im)
            cropped_file_path = f'{output_dir}/{filename}'
            cropped.save(cropped_file_path)
            print('done')


def crop(im: Image.Image) -> Image.Image:
    x_mod = 0.08888889
    y_mod = 0.11081081
    width, height = im.size
    left = width * x_mod
    top = height * y_mod
    right = width - left
    bottom = top + 165
    return im.crop((left, top, right, bottom))

def readdir(dir: str, file_filter: Callable[[str], bool] = lambda f : True) -> Tuple[str, str]:
    for f in os.listdir(dir):
        if file_filter(f):
            yield (f, os.path.join(dir, f))

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--input_dir', required=True, type=str)
    parser.add_argument('--output_dir', required=True, type=str)
    args = parser.parse_args()

    main(args.input_dir, args.output_dir)