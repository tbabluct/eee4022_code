import argparse
import os
import re
import matplotlib.pyplot as plt
from datetime import datetime as dt
from image import load_image
from camera_model import CameraModel
from PIL import Image

parser = argparse.ArgumentParser(description='Play back images from a given directory')

parser.add_argument('dir', type=str, help='Directory containing images.')
parser.add_argument('--models_dir', type=str, default=None, help='(optional) Directory containing camera model. If supplied, images will be undistorted before display')
parser.add_argument('--scale', type=float, default=1.0, help='(optional) factor by which to scale images before display')

args = parser.parse_args()

camera = re.search('(stereo|mono_(left|right|rear))', args.dir).group(0)

timestamps_path = os.path.join(os.path.join(args.dir, os.pardir, camera + '.timestamps'))
if not os.path.isfile(timestamps_path):
  timestamps_path = os.path.join(args.dir, os.pardir, os.pardir, camera + '.timestamps')
  if not os.path.isfile(timestamps_path):
      raise IOError("Could not find timestamps file")

model = None
if args.models_dir:
    model = CameraModel(args.models_dir, args.dir)

current_chunk = 0
timestamps_file = open(timestamps_path)
os.makedirs(os.path.join("pre_processed", args.dir))
for line in timestamps_file:
    tokens = line.split()
    datetime = dt.utcfromtimestamp(int(tokens[0])/1000000)
    chunk = int(tokens[1])

    filename = os.path.join(args.dir, tokens[0] + '.png')
    if not os.path.isfile(filename):
        if chunk != current_chunk:
            print("Chunk " + str(chunk) + " not found")
            current_chunk = chunk
        continue

    current_chunk = chunk

    img_arr = load_image(filename, model)
    img_obj = Image.fromarray(img_arr, "RGB")
    save_path = os.path.join("pre_processed", filename)
    img_obj.save(save_path)