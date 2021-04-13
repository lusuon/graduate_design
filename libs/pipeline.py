"""

"""
import math
import os

from libs.config import openSfM_bin_dir, test_data_dir, test_data_obj, test_data_ply
import open3d as o3d
import numpy as np


def call_openSfM(bin_dir,data_dir):
    cmd = '{} {}'.format(bin_dir, data_dir)
    os.system(cmd)

def measure_dist_between_mesh_and_point_cloud(p_path, m_path):
    point_cloud = o3d.io.read_point_cloud(p_path)
    mesh = o3d.io.read_triangle_mesh(m_path)
    point_num = len(np.asarray(point_cloud.points))
    point_cloud_sample_from_mesh = mesh.sample_points_uniformly(number_of_points=10 * point_num)
    #o3d.visualization.draw_geometries([point_cloud])
    res = point_cloud.compute_point_cloud_distance(point_cloud_sample_from_mesh)
    return sum(res) / len(res) # avg

def show():
    pc = o3d.io.read_point_cloud(r'Z:\home\lusuon\test_data\robot\undistorted\depthmaps\merged.ply')
    point_num = len(np.asarray(pc.points))
    ms = o3d.io.read_triangle_mesh(r'Z:\home\lusuon\test_data\robot\robot.obj').sample_points_uniformly(number_of_points=10 * point_num)
    o3d.visualization.draw_geometries([pc])
    o3d.visualization.draw_geometries([ms])

if __name__ == '__main__':
    #call_openSfM(openSfM_bin_dir, test_data_dir)
    #r = measure_dist_between_mesh_and_point_cloud(test_data_ply,
    #                                          test_data_obj)
    show()
