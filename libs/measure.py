
# impl methods of measurement algorithms
def mse(p1, p2):
    m1 = p1.compute_point_cloud_distance(p2)
    m2 = p2.compute_point_cloud_distance(p1)
    return sum(m1) / len(m1) + sum(m2) / len(m2)  # sum of 2 mse


def percentage_threshold(source,target,threshold):
    d = source.compute_point_cloud_distance(target)
    print('d amx and min:',max(d), min(d))
    invalid_ind = [index for index, val in enumerate(d) if val > threshold]
    len_valid = len(d)-len(invalid_ind)
    print(len_valid, len(d), len_valid/len(d))
    return len_valid/len(d)
