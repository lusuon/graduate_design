import open3d as o3d
from libs.config import openSfM_bin_dir
import numpy as np
import copy
#import matplotlib.pyplot as plt
#import time


def draw_registration_result(source, target, transformation):
    """
    可视化
    """
    source_temp = copy.deepcopy(source)
    target_temp = copy.deepcopy(target)
    source_temp.paint_uniform_color([1, 0.706, 0])
    target_temp.paint_uniform_color([0, 0.651, 0.929])
    source_temp.transform(transformation)
    o3d.visualization.draw_geometries([source_temp, target_temp])


def preprocess_point_cloud(pcd, voxel_size):
    """
    提取几何特征
    向下采样点云，估计法线，然后计算每个点的FPFH特征。
    FPFH特征是一个描述点局部几何性质的33维向量。33维空间中的最近邻查询可以返回具有相似局部几何结构的点。
    """
    print(":: Downsample with a voxel size %.3f." % voxel_size)
    pcd_down = pcd.voxel_down_sample(voxel_size)

    radius_normal = voxel_size * 2
    print(":: Estimate normal with search radius %.3f." % radius_normal)
    pcd_down.estimate_normals(
        o3d.geometry.KDTreeSearchParamHybrid(radius=radius_normal, max_nn=30))

    radius_feature = voxel_size * 5
    print(":: Compute FPFH feature with search radius %.3f." % radius_feature)
    pcd_fpfh = o3d.pipelines.registration.compute_fpfh_feature(
        pcd_down,
        o3d.geometry.KDTreeSearchParamHybrid(radius=radius_feature, max_nn=100))
    return pcd_down, pcd_fpfh

 
def prepare_dataset(voxel_size):
    """
    从两个文件读取源点云和目标点云。 它们未对齐,以单位矩阵作为变换。    
    """
    print(":: Load two point clouds and disturb initial pose.")
    source = o3d.io.read_point_cloud(
        "test/elephant_small/undistorted/depthmaps/merged.ply")
    target = o3d.io.read_point_cloud(
        "test/elephant/undistorted/depthmaps/merged.ply")
    trans_init = np.asarray([[0.0, 0.0, 1.0, 0.0], [1.0, 0.0, 0.0, 0.0],
                             [0.0, 1.0, 0.0, 0.0], [0.0, 0.0, 0.0, 1.0]])
    source.transform(trans_init)
    #draw_registration_result(source, target, np.identity(4))

    source_down, source_fpfh = preprocess_point_cloud(source, voxel_size)
    target_down, target_fpfh = preprocess_point_cloud(target, voxel_size)
    return source, target, source_down, target_down, source_fpfh, target_fpfh


def execute_fast_global_registration(source_down, target_down, source_fpfh,
                                     target_fpfh, voxel_size):
    distance_threshold = voxel_size * 0.5
    print(":: Apply fast global registration with distance threshold %.3f"
          % distance_threshold)
    result = o3d.pipelines.registration.registration_fast_based_on_feature_matching(
        source_down, target_down, source_fpfh, target_fpfh,
        o3d.pipelines.registration.FastGlobalRegistrationOption(
            maximum_correspondence_distance=distance_threshold))
    return result


def refine_registration(source, target, source_fpfh, target_fpfh, voxel_size):
    distance_threshold = voxel_size * 0.4
    print(":: Point-to-plane ICP registration is applied on original point")
    print("   clouds to refine the alignment. This time we use a strict")
    print("   distance threshold %.3f." % distance_threshold)
    result = o3d.pipelines.registration.registration_icp(
        source, target, distance_threshold, result_ransac.transformation,
        o3d.pipelines.registration.TransformationEstimationPointToPlane())
    return result


'''
if __name__ == '__main__':
    voxel_size = 0.1  # means 5cm for this dataset
    source, target, source_down, target_down, source_fpfh, target_fpfh = prepare_dataset(
    voxel_size) 
    result_fast = execute_fast_global_registration(source_down, target_down,
                                                   source_fpfh, target_fpfh,
                                                   voxel_size) 
    print(result_fast)
    draw_registration_result(source_down, target_down, result_fast.transformation)
    import os
    from libs.config import meshrcnn_output_path
    obj_path = [fn for fn in os.listdir(meshrcnn_output_path) if fn.endswith('obj')][0]
    print(obj_path)
'''

if __name__ == '__main__':
    import os
    recon_path = r'static/meshrcnn_output/'+'to_rebuild'
    print([fn for fn in os.listdir(recon_path)
           if fn.endswith('obj')])
