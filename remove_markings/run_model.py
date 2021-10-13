"""
Python script to run the trained road marking removal models made by Georg
Usage: python run_model.py --srcdir path --dstdir path --modelpath path
Takes all .png images from srcdir, uses the model from modelpath to remove road markings and saves them in dstdir with
the same file name.
"""

import tensorflow as tf
import glob
import numpy as np
from os import path
import argparse
import os

def load_image(filename):
    in_image = tf.io.read_file(filename)
    in_image = tf.io.decode_png(in_image)
    in_image = tf.cast(in_image, tf.float32)
    in_image = (in_image / 127.5) - 1
    
    in_image = tf.expand_dims(in_image,0)
    in_image = tf.image.crop_and_resize(in_image, [[0,0,1,1]], [0], [256, 256])
    return in_image

def save_image(image, filename):
    save_image = (image * 0.5 + 0.5) * 255
    save_image = tf.cast(save_image, tf.uint8)
    tf.keras.utils.save_img(filename, save_image);

def main():
    # Command line arguments
    parser = argparse.ArgumentParser(description='Sample images from an Oxford Robocar dataset')
    parser.add_argument('--srcdir', type=str, help='Source directory of complete dataset', required=True)
    parser.add_argument('--dstdir', type=str, help='Destination directory for sampled images', required=True)
    parser.add_argument('--modelpath', type=str, help='Destination directory for sampled images', required=True)


    args = parser.parse_args()

    # Load the model.
    model = tf.keras.models.load_model(args.modelpath, compile=False)

    input_filenames = glob.glob(args.srcdir + "*.png")

    for filename in input_filenames:
        in_image = load_image(filename)

        output_img = model(in_image, training=True)
        output_filename = args.dstdir + filename.split("/")[-1]
        save_image(output_img[0], output_filename)
        print (output_filename)

if __name__ == '__main__':
    main();