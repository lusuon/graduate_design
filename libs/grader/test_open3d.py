import open3d as o3d

print("Load a ply point cloud, print it, and render it")
ply = o3d.io.read_point_cloud(r"D:\PROJECTS\graduate_design_project\test\merged.ply")
obj = o3d.io.read_triangle_mesh(r"D:\PROJECTS\graduate_design_project\test\1ba533f6962ee7c1ac51268fdb437a9e.obj")
# print(obj)
# o3d.io.write_point_cloud("constructed.pcd", ply)
obj_pcd = obj.sample_points_uniformly(number_of_points=6363)
# o3d.io.write_point_cloud("origin.pcd", obj_pcd)

# print(ply)
# o3d.visualization.draw_geometries([obj_pcd])
res1 = ply.compute_point_cloud_distance(obj_pcd)
res2 = obj_pcd.compute_point_cloud_distance(ply)
print('res1 with len {}:{}'.format(len(res1), res1[:10]))
print('res2 with len {}:{}'.format(len(res2), res2[:10]))
