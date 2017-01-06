from __future__ import print_function
import glob
from PIL import Image
import os
import random
import tempfile
import traceback

verbose = False

# TODO: Add a argparser

# Step 1: Create file lists that we are going to use
# Lets let it be regexy by directly adding the strings to the glob function

#http://serebii.net/pokemongo/pokemon.shtml
#https://www.upload.ee/download/6011813/71ff34f4b15e108e745f/Pok_mon_GO_-_151_Pok_mon.zip

root = r"C:\Users\Neon\PycharmProjects\pytomatic\samples\Pokemon_go\training_data"
negative_search_str = root+r"\negatives\*.*"
positive_search_str = root+r"\pokemon\*.*"
output_vector_file_name = "test.txt"



picture_transforms_per_background = 30 # Number of transforms per background
background_num = -1 # Number of background to randomly pick
positive_num = -1 # Number of positives to use

negative_lst = glob.glob(negative_search_str)
positive_lst = glob.glob(positive_search_str)


if len(negative_lst) == 0:
    print("Was unable to find any negative pictures\n\taborting...")
    exit(1)

if len(positive_lst) == 0:
    print("Was unable to find any positive pictures\n\taborting...")
    exit(1)

if verbose:
    for line in negative_lst:
        print(line)

if verbose:
    for line in positive_lst:
        print(line)


if background_num == -1:
    background_num = len(negative_lst)

if positive_num == -1:
    positive_num = len(positive_lst)

print("Settings:\n\t"
      "{:<{padding}s}{:<8d}\n\t{:<{padding}s}{:<8d}\n\t{:<{padding}s}{:<8d}\n\t{:<{padding}s}{:<8d}\n\t"
      "{:<{padding}s}{:<8d}\n\t{:<{padding}s}{:<8d}"
      .format("Positive images: ", len(positive_lst),
              "Background: ", len(negative_lst),
              "Picture transforms per neg: ",picture_transforms_per_background,
              "Positive images to use: ", positive_num,
              "Background to use: ",background_num,
              "Total number to be created: ",positive_num*background_num,
              padding=30))

# Create a description file for each of the posetive samples with the following format:
# [filename] [# of objects] [[x y width height] [... 2nd object] ...]
# [filename] [# of objects] [[x y width height] [... 2nd object] ...]
# [filename] [# of objects] [[x y width height] [... 2nd object] ...]

# NOTE: At the moment all the positive samples are precut this means the following
# filename 1 0 0 width_of_picture height_of_picture

tf = open('description_file.dat','wt')
for image_name in positive_lst:
    try:
        image = Image.open(image_name)
        width, height = image.size
        tf.write('{file} 1 0 0 {w} {h}\r\n'.format(file=image_name, w=width, h=height))
    except IOError as e:
        print("Unable to open {0}".format(image_name))
        print(e)
        pass
tf.close()

# NOTE: This would then call on the cvCreateTestSamples in opencv_createsamples program for each image and output a lot of
# images and an updates info.dat file
# https://github.com/opencv/opencv/blob/master/apps/createsamples/utility.cpp#L1304

# What we want to do now is create new samples based on the positives with random negatives/background
# And then we want to write the VEC files involved

cmd = 'opencv_createsamples -img "{pos_img}" -bg "{bgs}" -vec "{vec_file}" -num "{num}" ' \
      '-bgcolor 0 -bgthresh 0 -maxxangle 0 -maxyangle 0 maxzangle 0 -maxidev 40 -w 24 -h 24'

positive_lst_random = random.sample(positive_lst,positive_num)
negative_lst_random = random.sample(negative_lst,background_num)

bg_file = open('background.txt','wt')
for image_name in negative_lst_random:
    bg_file.write(os.path.normpath(image_name) + '\n')

cwd = os.getcwd()
print(cwd)
for positive_image_name in positive_lst_random:
    os.system(cmd.format(pos_img=os.path.normpath(positive_image_name),
                         bgs = bg_file.name,
                         vec_file = cwd + r'\\vectors\\' + os.path.basename(positive_image_name) + os.path.basename(bg_file.name) + '.vec',
                         num=picture_transforms_per_background))



os.system('python mergevec.py -v vectors -o merged_vectors.vec')

training_cmd = 'opencv_traincascade -data classifier -vec merged_vectors.vec -bg ./background.txt -numStages 13 -precalcvalBufSize 4096 -precalcIdxBufSize 4096 -maxFalseAlarmRate 0.50 -mode ALL -minHitRate 0.99'

os.system(training_cmd.format(bg_file = './background.txt'))
