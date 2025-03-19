'''
写操作
'''
from init import *
from global_ import *

def print_next(message):
    print(f"{message}", end="")

def do_object_write(object_unit, disk_unit, size, object_id,V):
    current_write_point = 0
    for i in range(1, V + 1):
        if disk_unit[i] == 0:
            disk_unit[i] = object_id
            current_write_point += 1
            object_unit[current_write_point] = i
            if current_write_point == size:
                break
    assert (current_write_point == size)


def write_action():
    n_write = int(input())
    refresh_G(disks_state, G)
    for i in range(1, n_write + 1):
        write_input = input().split()
        write_id = int(write_input[0])
        size = int(write_input[1])
        tag = int(write_input[2])
        storge_list = insert_function(write_id, size, tag)
        print(f"{write_id}")
        for j in range(1, REP_NUM + 1):
            for s in storge_list:
                print_next(f"{s}")
            print()
    sys.stdout.flush()

#插入函数
    #用一个循环首先judge每一个盘够不够0.9space，然后使用离散空间，然后看能不能顺存
def insert_function(obj_id,size,tag):
    storge_list = []#返回给判题器的结果
    for obj_copy in range(3):
        tem = []
        flag = True
        #首先优先找离散位置
        for index in range(len(disks_state)):
            if size in disks_state[index].discrete_space[tag].keys():
                if len(disks_state[index].discrete_space[tag][size]) >= 0:
                    #只用给硬盘insert
                    disks_state[index].insert(obj_id,size,disks_state[index].discrete_space[tag][size][0])                    
                    tem.append(index)
                    tem += list(range(disks_state[index].discrete_space[tag][size][0], disks_state[index].discrete_space[tag][size][0]+size))
                    disks_state[index].discrete_space[tag][size].remove(disks_state[index].discrete_space[tag][size][0])
                    flag = False
                    break
        #顺插
        if flag:
            index = np.argmin(div_disks_space.space_usage[:,tag])
            if disks_state[index].judge(size):
                if div_disks_space.insert(tag,size,index):
                    disks_state[index].insert(obj_id,size,div_disks_space.dif_space_point_index[index][tag][1]-size)
                    tem.append(index)
                    tem += list(range(disks_state[index].discrete_space[tag][size][0], disks_state[index].discrete_space[tag][size][0]+size))
                    break
        storge_list.append(tem)
    return storge_list

#=========================每一帧将disk的token复原=========================
def refresh_G(disks, G):
    for disk in disks:
        disk.left_G = G