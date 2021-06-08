import open3d as o3d
import copy

# impl visualizatoin and img render

def display_inlier_outlier(pcd, ind):
    pcd_in = pcd.select_by_index(ind)  # RANSAC分割后的内部点云(拟合平面点)
    pcd_out = pcd.select_by_index(
        ind, invert=True)  # RANSAC分割后的外部点云(拟合平面之外的点)
    print("Showing outliers (red) and inliers (gray): ")
    pcd_in.paint_uniform_color([1, 0, 0])
    pcd_out.paint_uniform_color([0.8, 0.8, 0.8])
    o3d.visualization.draw_geometries([pcd_in, pcd_out])

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

def draw_help_info(source,target,threshold):
    d = source.compute_point_cloud_distance(target)
    print('help info:',max(d),min(d))
    invalid_ind = [index for index, val in enumerate(d) if val > threshold]
    invalid_pcd = source.select_by_index(invalid_ind)
    valid_pcd = source.select_by_index(invalid_ind,invert=True)
    invalid_pcd.paint_uniform_color([1, 0, 0])
    valid_pcd.paint_uniform_color([0.8, 0.8, 0.8])
    target.paint_uniform_color([0, 0.2, 0.2])
    #len_valid, len_invalid = len(d)-len(invalid_ind), len(invalid_ind)
    #print('{} valid, {} invalid, {} of the recon is valid in percentage.'.format(len_valid,len_invalid,len_valid/len(d)))
    o3d.visualization.draw_geometries([invalid_pcd, valid_pcd, target])

if __name__ == '__main__':
    pcd = o3d.io.read_point_cloud('test/constructed.pcd')
    cl, ind = pcd.remove_statistical_outlier(nb_neighbors=20,
                                             std_ratio=2.0)
    print(ind)
    print(cl.select_by_index([0]))
