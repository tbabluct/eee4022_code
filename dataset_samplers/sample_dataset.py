import argparse
import shutil
import glob, os

parser = argparse.ArgumentParser(description='Sample images from an Oxford Robocar dataset')
parser.add_argument('--srcdir', type=str, help='Source directory of complete dataset', required=True)
parser.add_argument('--dstdir', type=str, help='Destination directory for sampled images', required=True)
parser.add_argument('-n', type=int, help='Sample every n images', required=True)
parser.add_argument('--prefix', type=str, default='', help='Optional prefix to original filename')

args = parser.parse_args()

# Get a list of filenames
input_filenames = glob.glob(args.srcdir + "*.png")
input_filenames = input_filenames[0:-1:args.n] # sample every n imagesS

for filename in input_filenames:
    output_filename = filename.split('/')[-1]
    output_filename = args.prefix + output_filename
    shutil.copy2(filename, args.dstdir + output_filename)

# Finish statement
print ("{} files copied from {} to {}".format(len(input_filenames), args.srcdir, args.dstdir))
