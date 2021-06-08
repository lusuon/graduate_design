import open3d as o3d


def rm_outliner(pcd, method='stat'):
    processed_pcd, out_pcd = pcd, None
    if method == 'stat':
        processed_pcd,out_pcd = rm_by_stat(pcd)
    elif method == 'ransac':
        processed_pcd, out_pcd = rm_by_ransc(pcd)
    else:
        pass
    return processed_pcd,out_pcd

def rm_by_ransc(pcd):
    print("ransc oulier removal")
    plane_model, inliers = pcd.segment_plane(
        distance_threshold=0.06, ransac_n=10, num_iterations=10)
    # distance_threshold为距离阈值参数，ransac_n为RANSAC迭代的点数，num_iterations为最大迭代次数
    #cl,ind = plane_model,inliers
    pcd_in = pcd.select_by_index(inliers, invert=True)  # RANSAC分割后的外部点云(拟合平面之外的点)
    pcd_out = pcd.select_by_index(
        inliers)  # RANSAC分割后的内部点云(拟合平面点)
    """    
    print("Showing outliers (red) and inliers (gray): ")
    pcd_in.paint_uniform_color([1, 0, 0])
    pcd_out.paint_uniform_color([0.8, 0.8, 0.8])
    o3d.visualization.draw_geometries([pcd_in, pcd_out])
    """
    return pcd_in,pcd_out

def rm_by_stat(pcd):
    cl, ind = pcd.remove_statistical_outlier(nb_neighbors=20,
                                             std_ratio=2.0)
    pcd_in = cl.select_by_index(ind)
    pcd_out = cl.select_by_index(ind,invert=True)
    return pcd_in,pcd_out
