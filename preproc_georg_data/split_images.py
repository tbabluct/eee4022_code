"""
Script to split training images used for Georg's models
Usage: 
"""
import argparse
import glob
import tensorflow as tf

def main():
    # Command line arguments
    parser = argparse.ArgumentParser(description='Sample images from an Oxford Robocar dataset')
    parser.add_argument('--srcdir', type=str, help='Source directory of complete dataset', required=True)
    parser.add_argument('--dstleft', type=str, help='Destination directory for sampled images', required=True)
    parser.add_argument('--dstright', type=str, help='Destination directory for sampled images', required=True)

    args = parser.parse_args()

    input_paths = glob.glob(args.srcdir + "*.jpg")

    for input_path in input_paths:
        in_image = tf.io.read_file(input_path)
        in_image = tf.io.decode_jpeg(in_image)
        width = tf.shape(in_image)[1] // 2

        im_left = in_image[:, :width, :]
        im_right = in_image[:, width:, :]

        filename = input_path.split('/')[-1]
        filename = filename[:-4] + '.png'
        
        tf.keras.utils.save_img(args.dstleft + filename, im_left);
        tf.keras.utils.save_img(args.dstright + filename, im_right);

        print(filename)


if __name__ == '__main__':
    main()
