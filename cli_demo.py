import open3d as o3d
from libs.recon import recon_meshrcnn,recon_openSfM
from libs.measure import mse,percentage_threshold
from libs.visualize import display_inlier_outlier, draw_registration_result, draw_help_info
from libs.outlier_remove import rm_outliner
from libs.registration import registration_prep, execute_fast_global_registration
import os

def demo():
    recon_meshrcnn(input_path='test/to_rebuild.jpg')
    recon_meshrcnn(input_path='test/target.jpg')

    def get_obj_from_dir(x): return x+'/' + \
        [f for f in os.listdir(x) if f.endswith('obj')][0]
    origin_obj_path = get_obj_from_dir('static/meshrcnn_output/target')
    target_obj_path = get_obj_from_dir('static/meshrcnn_output/to_rebuild')

    origin = o3d.io.read_triangle_mesh(origin_obj_path)
    origin.scale(0.9, center=origin.get_center())
    origin_pcd = origin.sample_points_uniformly(10000)
    rebuild = o3d.io.read_triangle_mesh(target_obj_path)
    rebuild_pcd = rebuild.sample_points_uniformly(10000)

    o3d.geometry.PointCloud.remove_non_finite_points(
        origin_pcd, remove_nan=True, remove_infinite=False)
    o3d.geometry.PointCloud.remove_non_finite_points(
        rebuild_pcd, remove_nan=True, remove_infinite=False)
    # 剔除无关点完成
    origin_inliner, _ = rm_outliner(origin_pcd)  # origin_pcd  #
    rebuild_inliner, _ = rm_outliner(rebuild_pcd)  # rebuild_pcd
    #剔除后可视化
    o3d.visualization.draw_geometries([origin_inliner])
    o3d.visualization.draw_geometries([rebuild_inliner])
    origin_inliner.paint_uniform_color([1, 0, 0])
    rebuild_inliner.paint_uniform_color([0.8, 0.8, 0.8])
    # 配准
    voxel_size = 50  # 0.05 means 5cm for this dataset
    origin_pcd_down = origin_pcd.voxel_down_sample(voxel_size)
    rebuild_pcd_down = rebuild_pcd.voxel_down_sample(voxel_size)
    source_down, target_down, source_fpfh, target_fpfh = registration_prep(
        origin_pcd_down, rebuild_pcd_down, voxel_size)
    result_fast = execute_fast_global_registration(source_down, target_down,
                                                   source_fpfh, target_fpfh,
                                                   voxel_size, True)
    tf = result_fast.transformation
    trans = source_down.transform(tf)
    draw_registration_result(source_down, target_down, tf)
    draw_help_info(trans, target_down, 200)
    res_mse = mse(trans, target_down)
    res_per = percentage_threshold(trans, target_down, 200)
    return res_mse,res_per

def demo_sfm():
    recon_openSfM('test/elephant_small')
    rebuild = o3d.io.read_point_cloud(
        'test/elephant_small/undistorted/depthmaps/merged.ply')
    down = rebuild.voxel_down_sample(0.1)
    print('down',down)
    rm_outlier_pcd, _=rm_outliner(down, 'stat')
    #cl, ind = rm_outlier_pcd.remove_radius_outlier(nb_points=16, radius=0.2)
    #print('radius',cl)
    rm_plane_pcd, _ = rm_outliner(rm_outlier_pcd, 'ransac')
    pcd_fin, _ = rm_outliner(rm_plane_pcd, 'stat')
    print('fin stat',pcd_fin)
    target = o3d.io.read_triangle_mesh(
        'static/meshrcnn_output/target/0_mesh_chair_1.000.obj')
    target = target.scale(0.001, center=target.get_center())
    tpcd = target.sample_points_uniformly(1000)

    voxel_size = 0.1
    source_down, target_down, source_fpfh, target_fpfh = registration_prep(
        tpcd, pcd_fin,voxel_size)
    result_fast = execute_fast_global_registration(source_down, target_down,
                                                   source_fpfh, target_fpfh,
                                                   voxel_size)
    tf = result_fast.transformation
    trans = source_down.transform(tf)
    draw_help_info(trans, target_down, 0.01)
    res_mse = mse(trans, target_down)
    res_per = percentage_threshold(trans, target_down, 0.01)
    return res_mse, res_per


if __name__ == '__main__':
    demo_sfm()
