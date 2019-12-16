import xml.etree.ElementTree as ET
import pickle
import os
from os import listdir, getcwd
from os.path import join
from tqdm import tqdm

classes = ["Window"]

# Change paths ar 3 lines indicated with ### change path here ###

def convert(size, box):
    dw = 1./(size[0])
    dh = 1./(size[1])
    x = (box[0] + box[1])/2.0 - 1
    y = (box[2] + box[3])/2.0 - 1
    w = box[1] - box[0]
    h = box[3] - box[2]
    x = x*dw
    w = w*dw
    y = y*dh
    h = h*dh
    return (x,y,w,h)

def convert_annotation(image_id):
    in_file = open('%s.xml'%(image_id))
    # Path to the new text files which we generate in this script
    out_file = open('/home/andreas/Documents/OIDv4_ToolKit/OID/Dataset/validation/Window1000/annotations_txt/%s.txt'%(image_id), 'w')     ### change here ###

    tree=ET.parse(in_file)
    root = tree.getroot()
    size = root.find('size')
    w = int(size.find('width').text)
    h = int(size.find('height').text)

    for obj in root.iter('object'):
        difficult = obj.find('difficult').text
        cls = obj.find('name').text
        if cls not in classes or int(difficult)==1:
            continue
        cls_id = classes.index(cls)
        xmlbox = obj.find('bndbox')
        b = (float(xmlbox.find('xmin').text), float(xmlbox.find('xmax').text), float(xmlbox.find('ymin').text), float(xmlbox.find('ymax').text))
        bb = convert((w,h), b)  #returns x,y,w,h normalized
        out_file.write(str(cls_id) + " " + " ".join([str(a) for a in bb]) + '\n')

    in_file.close()
    out_file.close()

##############################################################################

# Path to directory where the XML files are stored
path = 'OID/Dataset/validation/Window1000/annotations'   ### change here ###

# Change current directory to specified directory
os.chdir(path)

# Path to txt-file which we generate and which summarized the train/validation dataset in one text file
textfile = '/home/andreas/Documents/OIDv4_ToolKit/OID/Dataset/validation/Window1000/validation_window1000.txt' ### change here twice train/validation ###

with open(textfile, 'w') as file_out:
    # For every file in this directory
    for image_id_ending in tqdm(os.listdir(os.getcwd())):
        print('Current file: ' + image_id_ending)
        image_id = image_id_ending[:-4]
        # convert the annotation to yolo format
        convert_annotation(image_id)
        #write image path to txt file
        line = '/data/obj/' + image_id + '.jpg\n'
        file_out.write(line)

file_out.close()
