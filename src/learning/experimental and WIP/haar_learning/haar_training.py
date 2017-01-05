import cv2
import glob
import os
import tempfile
from PIL import Image
import time

OPEN_CV_FOLDER = r'C:\Python27\Lib\opencv\build\x64\vc14\bin'

backgrounds_folder = r'C:\Users\Neon\PycharmProjects\pytomatic\samples\Pokemon_go\training_data\negatives'
samples_folder =r'C:\Users\Neon\PycharmProjects\pytomatic\samples\Pokemon_go\training_data\pokestops'
output_vector_folder = r"C:\Users\Neon\PycharmProjects\pytomatic\samples\Pokemon_go\training_data\vector"


#Setting up the path for the create_sample command
create_command = OPEN_CV_FOLDER+r'\opencv_createsamples.exe'
print create_command

#Creating listings for the imagefiles
bg_lst = (glob.glob(backgrounds_folder + '/*'))
sample_lst = (glob.glob(samples_folder + '/*'))


tf = open('bg.dat','wt')
#Creating .dat file for negatives/backgrounds
for image in bg_lst:
    if '.jpg' not in image:
        continue
    tf.write(image+'\n')
tf.write('\n')


print 'Number of backgrounds found {0}'.format(len(bg_lst))
print 'Number of samples found \t{0}'.format(len(sample_lst))

create_string = r'{CV_exe} -img {image_name} -num {number} -bg {negatives} -vec {out_vector} -bgthresh 0'

#Create samples using method 1
#os.system(create_string.format(CV_exe=create_command,image_name=sample_lst[0],number=100,negatives='bg.dat',out_vector='out.vec'))
#time.sleep(0.1)
#print '\n\n\n'


#Create samples using method 2
#We can use the description file method since we got positive already cropped samples to use as a base
'''
$ find  /cygdrive/c/Users/Neon/PycharmProjects/pytomatic/samples/Pokemon_go/training_data/pokestops -name '*.png' -exec identify -format '%i 1 0 0 %w %h' \{\} \; > desc_file.dat
This command can be done with python
'''

tf = open('desc_file.dat','wt')
for image in sample_lst:
    if '.png' not in image:
        continue
    tmp_img = Image.open(image)
    width, height = tmp_img.size
    tf.write('{file} 1 0 0 {w} {h}\r\n'.format(file=image,w=width,h=height))
tf.close()

#2. Create training samples from some
#Create the .vec file
vec_string = r'{create_command} -info desc_file.dat -vec vector.vec'
os.system(vec_string.format(create_command=create_command))


#Create test samples

create_test_string = '{CV_exe} -img {img} -num {num} -bg {bg} -info {info} -maxxangle 0.6 -maxyangle 0 -maxzangle 0.3 -maxidev 100 -bgcolor 0 -bgthresh 0'
os.system(create_test_string.format(CV_exe=create_command,img=sample_lst[0],bg='bg.dat',num=10,info='desc_file.dat'))


#Showing the result
show_string = r'{CV_exe} -vec {vector}'
#os.system(show_string.format(CV_exe=create_command,vector='alt_out.vec'))
time.sleep(1)
print '\n\n\n'