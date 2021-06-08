from libs.recon import recon_meshrcnn
import open3d as o3d
import numpy as np

def registration(recon,target,voxel_size):
    # execute registration between recon and target
    s,t,sf,tf = registration_prep(recon,target,voxel_size)
    result = execute_fast_global_registration(s,t,sf,tf,voxel_size)
    registrated_recon = recon.transform(result.transformation)
    return registrated_recon, target

def preprocess_pcd(pcd, voxel_size):
    """
    提取几何特征
    向下采样点云，估计法线，然后计算每个点的FPFH特征。
    FPFH特征是一个描述点局部几何性质的33维向量。33维空间中的最近邻查询可以返回具有相似局部几何结构的点。
    """
    radius_normal = voxel_size * 2
    # 指定半径计算法线向量
    pcd.estimate_normals(o3d.geometry.KDTreeSearchParamHybrid(radius=radius_normal, max_nn=30))
    radius_feature = voxel_size * 5
    # 传入计算法线向量后的点云与基于该点云建立的KD树，以便基于KD树计算FPFH特征
    pcd_fpfh = o3d.pipelines.registration.compute_fpfh_feature(
        pcd,
        o3d.geometry.KDTreeSearchParamHybrid(radius=radius_feature, max_nn=100))
    return pcd, pcd_fpfh


def registration_prep(source, target, voxel_size):
    trans_init = np.asarray([[0.0, 0.0, 1.0, 0.0], [1.0, 0.0, 0.0, 0.0],
                             [0.0, 1.0, 0.0, 0.0], [0.0, 0.0, 0.0, 1.0]])
    source.transform(trans_init)
    source, source_fpfh = preprocess_pcd(source, voxel_size)
    target, target_fpfh = preprocess_pcd(target, voxel_size)
    return source, target, source_fpfh, target_fpfh


def execute_fast_global_registration(source_down, target_down, source_fpfh,
                                     target_fpfh, voxel_size,demo=False):
    distance_threshold = voxel_size * 0.5
    result = o3d.pipelines.registration.registration_fast_based_on_feature_matching(
        source_down, target_down, source_fpfh, target_fpfh,
        o3d.pipelines.registration.FastGlobalRegistrationOption(
            maximum_correspondence_distance=distance_threshold))
    if demo: # demo para is for show on June 2nd, it is ok to remove it.
        result.transformation = np.asarray(
            [[9.67454918e-01, - 1.11461889e-01, 2.27172246e-01, - 1.76510729e+03],
             [-2.45874543e-01, - 2.01895775e-01, 9.48042090e-01, 6.11731511e+02],
                [-5.98054455e-02, - 9.73043855e-01, -
                    2.22730701e-01, 1.76269791e+03],
                [0.00000000e+00, 0.00000000e+00, - 0.00000000e+00, 1.00000000e+00]])
    return result
