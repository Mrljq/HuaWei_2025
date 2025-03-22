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
        # print(f'{write_id,size,tag,storge_list}' , file=sys.stderr) 
        print(f"{write_id}")
        
        for j in range(1, REP_NUM + 1):
            print_next(f"{int(storge_list[j-1][0])}")
            for s1 in storge_list[j-1][1:]:
                print_next(' ')
                # print(f"{int(s[0])}", end="", file=sys.stderr)
                print_next(f"{int(s1)}")
                # print(f"{int(s[0])}", end="",file=sys.stderr)
            print()
        print(f'{write_id,size,tag,storge_list}' , file=sys.stderr) 
    #=============================插入时候更新Div_Disk_Space和Disk_State的状态
    div_disks_space.update_usage()
    for disk in disks_state:
        disk.update_point_sequence()
    sys.stdout.flush()

# #插入函数
#     #用一个循环首先judge每一个盘够不够0.9space，然后使用离散空间，然后看能不能顺存
# def insert_function(obj_id,size,tag):
#     storge_list = []#返回给判题器的结果
#     al_disk = []
#     for obj_copy in range(3):
#         tem = []
#         flag = True
#         #首先优先找离散位置
#         for index in range(len(disks_state)):
#             if index not in al_disk:
#                 if size in disks_state[index].discrete_space[tag].keys():
#                     if len(disks_state[index].discrete_space[tag][size]) >= 0:
#                         #只用给硬盘insert
#                         disks_state[index].insert(obj_id,size,disks_state[index].discrete_space[tag][size][0])                    
#                         tem.append(index+1)    
#                         al_disk.append(index)       
#                         tem += list(range(disks_state[index].discrete_space[tag][size][0]+1, disks_state[index].discrete_space[tag][size][0]+size+1))
#                         disks_state[index].discrete_space[tag][size].remove(disks_state[index].discrete_space[tag][size][0])
#                         flag = False
#                         break
#         #顺插
#         if flag:
#             # 使用 np.argsort 获取排序后的索引
#             top_3_list = np.argsort(div_disks_space.space_usage[:,tag-1])[:3]
#             for index in top_3_list:
#                 if index not in al_disk:

#                     if disks_state[index].judge(size):

#                         if div_disks_space.insert(tag,size,index):
#                             disks_state[index].insert(obj_id,size,div_disks_space.dif_space_point_index[index][tag-1][1]-size)
#                             tem.append(index+1)
#                             al_disk.append(index)    
#                             tem += list(range(div_disks_space.dif_space_point_index[index][tag-1][1]-size+1, div_disks_space.dif_space_point_index[index][tag-1][1]+1))
#                             # print(f'{obj_id,obj_copy,tem}' , file=sys.stderr) 
#                             break
#         storge_list.append(tem)
#         obj_state.insert_obj(obj_id, tag, size, [storge_list[0][0],storge_list[1][0],storge_list[2][0]])
#         # print(f'{obj_copy, index,storge_list}' , file=sys.stderr) 
#     return storge_list

#=========================每一帧将disk的token复原=========================
def refresh_G(disks, G):
    for disk in disks:
        disk.left_G = G

#==============================更新版本insert function==========================
def insert_function(obj_id,size,tag):
    storge_list = []#返回给判题器的结果
    already_disk = []
    #==================3个副本==================
    for obj_copy in range(3):
        tem = []
        dis_insert = False
        #======================首先进行离散插入===================
        for index in range(len(disks_state)):
            if index not in already_disk:
                if size in disks_state[index].discrete_space[tag-1].keys():
                    if len(disks_state[index].discrete_space[tag-1][size]) > 0:
                        disks_state[index].insert(obj_id, size, disks_state[index].discrete_space[tag-1][size][0], tag-1, True)
                        already_disk.append(index)
                        dis_insert = True
                        tem.append(index+1)
                        tem += list(range(disks_state[index].discrete_space[tag-1][size][0]+1, disks_state[index].discrete_space[tag-1][size][0]+size+1))
                        break
        #===================进行顺插======================
        if dis_insert == False:
            # 使用 np.argsort 获取排序后的索引
            top_3_list = np.argsort(div_disks_space.space_usage[:,tag-1])[:3]
            for index in top_3_list:
                if index not in already_disk:
                    if div_disks_space.insert(tag-1, size, index):
                        tem.append(index+1)
                        tem += list(range(div_disks_space.dif_space_point_index[index][tag-1][1]-size+1, div_disks_space.dif_space_point_index[index][tag-1][1]+1))
                        already_disk.append(index)
                        break
        storge_list.append(tem)
    #=================首先插入obj_state中=========================
    obj_state.insert_obj(obj_id, tag, size, already_disk)
    return storge_list