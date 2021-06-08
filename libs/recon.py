import os
from libs.config import openSfM_bin_dir, data_for_sfm_dir,meshrcnn_input_path,meshrcnn_output_path,sfm_output_path


def recon_openSfM(data_dir=data_for_sfm_dir):
    open_sfm_cmd = '{} {}'.format(openSfM_bin_dir, data_dir)
    os.system(open_sfm_cmd)
    return sfm_output_path


def recon_meshrcnn(input_path = meshrcnn_input_path,output_path = meshrcnn_output_path):
    meshrcnn_cmd = "python libs/meshrcnn/demo/demo.py \
    --config-file libs/meshrcnn/configs/pix3d/meshrcnn_R50_FPN.yaml \
    --input {input_path} \
    --output {output_path} \
    --onlyhighest MODEL.WEIGHTS meshrcnn://meshrcnn_R50.pth".format(input_path=input_path,output_path=output_path)
    os.system(meshrcnn_cmd)
    return output_path
