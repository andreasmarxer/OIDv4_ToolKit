# Code adapted by Andreas Marxer, ASL ETH
# Original source: https://github.com/experiencor/raccoon_dataset/blob/master/xml_to_csv.py

import os
import glob
import pandas as pd
import xml.etree.ElementTree as ET
from tqdm import tqdm


def xml_to_csv(path):
    xml_list = []
    for xml_file in tqdm(glob.glob(path + '/*.xml')):
        tree = ET.parse(xml_file)
        root = tree.getroot()
        for member in root.findall('object'):
            value = (root.find('filename').text,
                     int(root.find('size')[0].text),
                     int(root.find('size')[1].text),
                     member[0].text,
                     int(member[4][0].text),
                     int(member[4][1].text),
                     int(member[4][2].text),
                     int(member[4][3].text)
                     )
            xml_list.append(value)
    column_name = ['filename', 'width', 'height', 'class', 'xmin', 'ymin', 'xmax', 'ymax']
    xml_df = pd.DataFrame(xml_list, columns=column_name)
    return xml_df


def main():

    path = 'OID/Dataset/validation/Window/'
    path_in = path + 'annotations'

    image_path = os.path.join(os.getcwd(), path_in)
    xml_df = xml_to_csv(image_path)
    xml_df.to_csv(path + 'labels.csv', index=None)
    print('Successfully converted XML! ')
    print('CSV saved in: '+ path )


main()
