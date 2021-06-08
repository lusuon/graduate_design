from libs.recon import recon_meshrcnn, recon_openSfM
from libs.outlier_remove import rm_outliner
from libs.registration import registration
from libs.measure import mse,percentage_threshold
from cli_demo import demo, demo_sfm
import os
import open3d as o3d


def pipeline(method='fast', target_is_mesh=True, target_path='test/chair_target.obj',demo_show=False):
    if not demo_show:
        # 1. recon
        recon_is_mesh, recon_res_path = recon(method)
        # 2.preprocess
        recon_pcd, target_pcd = preprocess(
            recon_is_mesh, recon_res_path, target_is_mesh, target_path)    
        # 3.scoring
        score = mse(recon_pcd, target_pcd)
        percentage = percentage_threshold(recon_pcd,target_pcd,200)
    elif method =='fast' and demo_show:
        score,percentage = demo()
    elif method == 'precise' and demo_show:
        score,percentage = demo_sfm()
    else:
        score,percentage = 0,0
    return score,percentage


def recon(method):
    print('method:',method)
    if method == 'precise':
        is_mesh = False
        recon_res_path = recon_openSfM()
    else:
        is_mesh = True
        recon_res_path = recon_meshrcnn()
    return is_mesh,recon_res_path

def preprocess(recon_is_mesh,recon_path,target_is_mesh,target_path):
    recon_pcd, target_pcd = None,None
    # make sure output pcd
    if recon_is_mesh:
        recon_obj_path = recon_path+'to_rebuild/'+[fn for fn in os.listdir(recon_path+'to_rebuild')
         if fn.endswith('obj')][0]
        recon_mesh = o3d.io.read_triangle_mesh(recon_obj_path)
        recon_pcd = recon_mesh.sample_points_uniformly(number_of_points=10000)
    else:
        recon_pcd = o3d.io.read_point_cloud(recon_path)
    # make sure output pcd 
    if target_is_mesh:
        target_mesh = o3d.io.read_triangle_mesh(target_path)
        target_pcd = target_mesh.sample_points_uniformly(
            number_of_points=10000)
    else:
        target_pcd = o3d.io.read_point_cloud(target_path)
    # voxelization
    voxel_size = 0.05
    voxel_down_recon = recon_pcd.voxel_down_sample(voxel_size=voxel_size)
    voxel_down_target = target_pcd.voxel_down_sample(voxel_size=voxel_size)
    # rm_outlier, assume that target is no need to remove outliners
    recon_pcd,outliers = rm_outliner(voxel_down_recon)
    # registration
    recon_pcd,target_pcd = registration(recon_pcd,target_pcd,voxel_size)
    return recon_pcd,target_pcd

