
'''
初始化
'''
import sys
import numpy as np
from obj import *


FRE_PER_SLICING = 1800
MAX_DISK_NUM = (10 + 1)
MAX_DISK_SIZE = (16384 + 1)
MAX_REQUEST_NUM = (30000000 + 1)
MAX_OBJECT_NUM = (100000 + 1)

EXTRA_TIME = 105

disk = [[0 for _ in range(MAX_DISK_SIZE)] for _ in range(MAX_DISK_NUM)]
disk_point = [0 for _ in range(MAX_DISK_NUM)]
_id = [0 for _ in range(MAX_OBJECT_NUM)]

current_request = 0
current_phase = 0


req_object_ids = [0] * MAX_REQUEST_NUM
req_prev_ids = [0] * MAX_REQUEST_NUM
req_is_dones = [False] * MAX_REQUEST_NUM

objects = [Object() for _ in range(MAX_OBJECT_NUM)]


def get_init_info():
    user_input = input().split()
    T = int(user_input[0])  #时间片个数
    M = int(user_input[1])  #对象标签个数
    N = int(user_input[2])  #硬盘个数
    V = int(user_input[3])  #每个硬盘存储单元
    G = int(user_input[4])  #每个时间片最多消耗令牌数

    free_data=[]
    free_del=[]
    free_write=[]
    free_read=[]
    # 预处理
    for item in range(1, M * 3 + 1):
        data=input()
        free_data.append(data.split())
    free_data_array = np.array(free_data,dtype=int)
    # np.save('C:/Users/lijia/Desktop/huawei_race/HuaWei_2025/interactor/my_array.npy', free_data_array)
    free_del=free_data_array[0:M]
    free_write=free_data_array[M:2*M]
    free_read=free_data_array[2*M:3*M]
    print(free_write-free_del, file=sys.stderr)    

    pre_trategy(free_data_array,M)



    #初始化成功
    print("OK")
    sys.stdout.flush()
    
    return T,M,N,V,G



def pre_trategy(free_data_array,m):
    w_d = free_data_array[m:2*m]-free_data_array[0:m]
    #============================计算累计峰值============================
    cul_write = []
    for i in range(len(w_d)):
        max_ = 0
        for i1 in w_d[i]:
            if max_ + i1 > max_:
                max_ += i1
        cul_write.append(max_)
    cul_write = np.array(cul_write, dtype=int)
    total_sum = np.sum(cul_write)
    percentages = cul_write / total_sum
    print(percentages, file=sys.stderr) 
    return percentages


def timestamp_action():
    timestamp = input().split()[1]
    print(f"TIMESTAMP {timestamp}")
    sys.stdout.flush()