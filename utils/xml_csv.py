import argparse
import os
import glob
import pandas as pd
import xml.etree.ElementTree as ET


def xml_to_csv(path):
    xml_list = []
    for xml_file in glob.glob(path + '/*.xml'):
        tree = ET.parse(xml_file)
        root = tree.getroot()
        for member in root.findall('object'):
            bndbox = member.find('bndbox')
            value = (root.find('filename').text,
                     int(root.find('size')[0].text),
                     int(root.find('size')[1].text),
                     member[0].text,
                     int(bndbox[0].text),
                     int(bndbox[1].text),
                     int(bndbox[2].text),
                     int(bndbox[3].text)
                     )
            xml_list.append(value)
    column_name = ['filename', 'width', 'height', 'class', 'xmin', 'ymin', 'xmax', 'ymax']
    xml_df = pd.DataFrame(xml_list, columns=column_name)
    return xml_df


def main():
    for d in ['train', 'val']:
        xml_path = os.path.join(os.getcwd(), 'images', d)
        print(xml_path)
        xml_df = xml_to_csv(xml_path)
        xml_df.to_csv(f'data/{d}_labels.csv', index=False)
        print('Successfully converted xml to csv.')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='xml file to csv.')
    parser.add_argument('--model_root_path', type=str,
                        default=max, required=True,
                        help='path of new model')
    args = parser.parse_args()

    os.chdir(args.model_root_path)

    main()
