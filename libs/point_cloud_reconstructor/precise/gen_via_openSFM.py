import os

from libs.config import openSfM_bin_dir, test_data_dir


def call_openSfM(bin_dir,data_dir):
    cmd = '{} {}'.format(bin_dir, data_dir)
    print(cmd)
    os.system(cmd)

if __name__ == '__main__':
    call_openSfM(openSfM_bin_dir,test_data_dir)