from keras.preprocessing.image import img_to_array
from keras.preprocessing.image import save_img
import matplotlib.pyplot as plt
import os
import cv2
import glob
import numpy as np
import tensorflow as tf
import random


def print_count_from_folders(train_dir,test_dir,class_names):

    print('====== Number of images per directory and class ======')
    for path_folder in [train_dir, test_dir]:
        print('FOLDER: '+ path_folder)
        for item_class in class_names:
            path = os.path.join(path_folder, item_class)

            print(item_class + " - "+ str(len(os.listdir(path))))
        print('====================================================')


def create_data_from_folder(dir_path,img_width,img_height,class_names):
    data = []

    for item_class in class_names:
        path = os.path.join(dir_path, item_class)

        for img in os.listdir(path):
            try:
                pic_array = cv2.imread(os.path.join(path, img))
                pic_resized = cv2.resize(pic_array, (img_width, img_height))
                # print(pic_resized.shape)
                data.append([pic_resized, class_names.index(item_class)])
            except Exception as e:
                pass
    return data

def separate_imgs_labels(data_array):
  x = []
  y = []
  for item in data_array:
    x.append(item[0]) #img
    y.append(item[1]) #labels

  # converting x & y to numpy array as they are list
  x = np.array(x)
  y = np.array(y)
  return x, y

## Para crear nuevas muestras

# Ref: https://www.kaggle.com/dhayalkarsahilr/easy-image-augmentation-techniques
def apply_transformation_img(class_dir,image, image_name):

    # flip horizontally
    flip = tf.image.flip_left_right(image)

    # central crop
    central_crop = tf.image.central_crop(image, central_fraction=0.8)

    # rotate 90
    rotate90 = tf.keras.preprocessing.image.random_rotation(image, 90, row_axis=0, col_axis=1, channel_axis=2,
                                                            fill_mode='nearest', cval=0.0, interpolation_order=1)
    # adjust brightness
    brightness = tf.image.random_brightness(image, 0.07)

    # rotate 180
    rotate180 = tf.image.rot90(image, k=2)

    # rotate 45
    rotate45 = tf.keras.preprocessing.image.random_rotation(image, 45, row_axis=0, col_axis=1, channel_axis=2,
                                                            fill_mode='nearest', cval=0.0, interpolation_order=1)

    # captions for different transformations
    label = ['flipped', 'central_crop', 'rotate 90', 'adjusted brightness', 'rotate 180', 'rotate 45']

    # list containing transformations
    transformations = [flip, central_crop, rotate90, brightness, rotate180, rotate45]

    # fig = plt.figure(1,figsize=(8,6))

    for i in range(len(transformations)):
        '''plt.subplot(3,3,i+1)
        plt.imshow(transformations[i])
  
        # format axes 
        plt.xticks([])  # remove x axis ticks        
        plt.yticks([])  # remove y axis ticks
  
        # set the image x axis label
        plt.xlabel(label[i], fontsize = 16)'''

        img_array = img_to_array(transformations[i])
        #save_img(class_dir + 'garbage-pics/train/trash/trash_' + image_name + '_' + str(i + 1) + '.jpg', img_array)
        save_img(class_dir + 'trash_' + image_name + '_' + str(i + 1) + '.jpg', img_array)

    # fig.tight_layout()
    # plt.show()


def iterate_images_for_transformation(class_path, img_names, n_samples):
    random.seed(1234)
    rand_val = random.sample(range(len(img_names)), n_samples)


    for i in range(0, n_samples):
        idx = rand_val[i]
        #print(idx)
        img_name = img_names[idx].split(".")[0]

        img_test = plt.imread(class_path + str(img_names[idx]))[:, :, :3]
        apply_transformation_img(class_path, img_test, img_name)

# Get a list of all the file paths that ends with .jpg from a specific directory
def list_transformed_images(class_path, delete=False): # Use param delete to remove the images created
  fileList = glob.glob(class_path + '*_*.jpg')

  # Print list of images created
  for name in fileList:
      print(name)


  print(len(fileList))

  if (delete):
    # Iterate over the list of filepaths & remove each file.
    print('Deleting '+ str(len(fileList)) + ' images')
    for filePath in fileList:
        try:
            os.remove(filePath)
        except:
          print("Error while deleting file : ", filePath)
