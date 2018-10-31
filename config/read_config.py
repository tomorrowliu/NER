import os
import configparser

cur_path = os.path.dirname(os.path.realpath(__file__))

config_path = os.path.join(cur_path, 'config.ini')

conf = configparser.ConfigParser()
conf.read(config_path)

train_brat_path = conf.get('config', 'train_brat_path')
train_ref_path = conf.get('config', 'train_crf_path')
train_brat_files = conf.items('train_brat_files')


