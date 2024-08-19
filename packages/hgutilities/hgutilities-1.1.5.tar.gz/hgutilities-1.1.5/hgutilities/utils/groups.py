import math

import numpy as np

def get_group_size(group_size, object_list):
    if group_size is None:
        group_size = len(object_list)
    return group_size

def get_group_indexes(length, group_size):
    group_size, group_count = get_group_data(length, group_size)
    end_point_indexes = get_end_point_indexes(length, group_size, group_count)
    group_indexes = construct_group_indexes(length, group_count, end_point_indexes)
    return group_indexes

def get_group_data(length, group_size):
    group_size = get_modified_group_size(length, group_size)
    group_count = math.floor(length/group_size)
    return group_size, group_count

def get_modified_group_size(list_size, average_size):
    if list_size < average_size:
        average_size = list_size
    return average_size

def get_end_point_indexes(length, group_size, group_count):
    real_group_size = length/group_count
    real_group_end_points = np.arange(0, group_count + 1) * real_group_size
    real_group_end_points = np.round(real_group_end_points, 5)
    end_point_indexes = np.ceil(real_group_end_points)
    return end_point_indexes

def construct_group_indexes(length, group_count, end_point_indexes):
    group_indexes = [np.arange(end_point_indexes[group_number],
                               end_point_indexes[group_number + 1]).astype('int')
                     for group_number in range(group_count)]
    return group_indexes

def get_group_indexes_fill(length, group_size):
    full_groups = math.floor(length / group_size)
    leftover = length - group_size*full_groups
    group_indexes = [np.arange(group_index*group_size, (group_index + 1)*group_size)
                     for group_index in range(full_groups)]
    if leftover != 0:
        group_indexes.append(np.arange(full_groups*group_size, length))
    return group_indexes

