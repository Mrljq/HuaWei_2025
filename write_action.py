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


def write_action(obj_state,disks_state,div_disks_space):
    n_write = int(input())
    refresh_G(disks_state, G)
    for i in range(1, n_write + 1):
        write_input = input().split()
        write_id = int(write_input[0])
        size = int(write_input[1])
        tag = int(write_input[2])
        # print('sssss',write_id, size, tag,file=sys.stderr)
        storge_list = insert_function(write_id, size, tag,obj_state,disks_state,div_disks_space)
        # print(f'{write_id,size,tag,storge_list}' , file=sys.stderr) 
        print(f"{write_id}")
        # print(write_id,storge_list,file=sys.stderr)
        # print(f'{storge_list}' , file=sys.stderr)
        for j in range(1, REP_NUM + 1):
            # print(write_id,storge_list,file=sys.stderr)
            print_next(f"{int(storge_list[j-1][0])}")
            for s1 in storge_list[j-1][1:]:
                print_next(' ')
                # print(f"{int(s[0])}", end="", file=sys.stderr)
                print_next(f"{int(s1)}")
                # print(f"{int(s[0])}", end="",file=sys.stderr)
            print()
        # print(f'{write_id,size,tag,storge_list}' , file=sys.stderr) 
    #=============================插入时候更新Div_Disk_Space和Disk_State的状态
    div_disks_space.update_usage()
    for disk in disks_state:
        disk.update_point_sequence()
    sys.stdout.flush()

#=========================每一帧将disk的token复原=========================
def refresh_G(disks, G):
    for disk in disks:
        disk.left_G = G
        disk.do_nothing=False


#==============================更新版本insert function==========================
def insert_function(obj_id,size,tag,obj_state,disks_state,div_disks_space):
    storge_list = []#返回给判题器的结果
    already_disk = []
    full_flag = False
    copy_space = np.copy(div_disks_space.space_usage)#复制的space矩阵
    #==================3个副本==================
    for obj_copy in range(3):
        tem = []
        dis_insert = False
        #======================首先进行离散插入===================
        for index in range(len(disks_state)):
            candi_dis_space = list(disks_state[index].discrete_space[tag-1].keys())
            if index not in already_disk:
                if size in disks_state[index].discrete_space[tag-1].keys():
                    if len(disks_state[index].discrete_space[tag-1][size]) > 0:
                        already_disk.append(index)
                        dis_insert = True
                        tem.append(index+1)
                        tem += list(range(disks_state[index].discrete_space[tag-1][size][0]+1, disks_state[index].discrete_space[tag-1][size][0]+size+1))
                        disks_state[index].insert(obj_id, size, disks_state[index].discrete_space[tag-1][size][0], tag-1, True)
                        copy_space[index,:] = 0#每次插入把这一行全部变成0
                        break
        #===================进行顺插======================
        if dis_insert == False:
            # 使用 np.argsort 获取排序后的索引
            top_list = np.argsort(copy_space[:,tag-1])
            index = top_list[-1]#如果空间最大的都进不去就不用考虑了
            if index not in already_disk:
                if div_disks_space.insert(tag-1, size, index):
                    tem.append(index+1)
                    disks_state[index].insert(obj_id, size, div_disks_space.dif_space_point_index[index][tag-1][1]-size, tag-1, False)
                    tem += list(range(div_disks_space.dif_space_point_index[index][tag-1][1]-size+1, div_disks_space.dif_space_point_index[index][tag-1][1]+1))
                    already_disk.append(index)
                    copy_space[index,:] = 0#每次插入把这一行全部变成0
                #===========如果出现满的情况===============
                else:
                    #=======================找到最大值的横纵下标=================
                    max_index = np.argmax(copy_space)
                    max_index= np.unravel_index(max_index, div_disks_space.space_usage.shape)
                    test_tag = max_index[1]
                    index = max_index[0]
                    if div_disks_space.insert(test_tag, size, index):
                        tem.append(index+1)
                        disks_state[index].insert(obj_id, size, div_disks_space.dif_space_point_index[index][test_tag][1]-size, test_tag, False)
                        tem += list(range(div_disks_space.dif_space_point_index[index][test_tag][1]-size+1, div_disks_space.dif_space_point_index[index][test_tag][1]+1))
                        already_disk.append(index)
                        copy_space[index,:] = 0#每次插入把这一行全部变成0
        storge_list.append(tem)
        
    #=================首先插入obj_state中=========================
    obj_state.insert_obj(obj_id, tag, size, already_disk)
    return storge_list

def insert_function(obj_id,size,tag,obj_state,disks_state,div_disks_space):
    storge_list = []#返回给判题器的结果
    already_disk = []
    copy_space = np.copy(div_disks_space.space_usage)#复制的space矩阵
    for _ in range(3):
        #=========插入状态选择========
        flags = [True,True]
        tem = []
        #===========首先进行顺插===============
        top_list = np.argsort(copy_space[:,tag-1])# 使用 np.argsort 获取排序后的索引
        index = top_list[-1]#如果空间最大的都进不去就不用考虑了
        if div_disks_space.insert(tag-1, size, index):
            tem.append(index+1)
            disks_state[index].insert(obj_id, size, div_disks_space.start_point[index][tag-1]-size)
            tem += list(range(div_disks_space.start_point[index][tag-1]-size+1, div_disks_space.start_point[index][tag-1]+1))
            already_disk.append(index)
            copy_space[index,:] = 0#每次插入把这一行全部变成0
            flags[0] = False
            flags[1] = False
        #=========顺插满了考虑类内离散插入============
        elif flags[0]:
            dis_tem = div_disks_space.discrete_space_size[:,tag-1,size-1]
            index = np.argmax(dis_tem)#找到
            if div_disks_space.discrete_space_size[index][tag-1][size-1] > 0:#如果离散个数大于1才能插入
                tem.append(index+1)
                #==========div_disks_space类的离散插入===========
                #===========================================================================修改
                disks_state[index].insert(obj_id, size, div_disks_space.start_point[index][tag-1]-size)
                tem += list(range(div_disks_space.discrete_space[index][tag-1][size-1][0]+1, div_disks_space.discrete_space[index][tag-1][size-1][0]+size+1))
                div_disks_space.insert_discrete(index, size-1, tag-1, div_disks_space.discrete_space[index][tag-1][size-1][0], size-1)
                already_disk.append(index)
                copy_space[index,:] = 0#每次插入把这一行全部变成0
                flags[1] = False
        #============类内离散满了考虑换类顺插=============
        elif flags[1]:
            #=======================找到最大值的横纵下标=================
            max_index = np.argmax(copy_space)
            max_index= np.unravel_index(max_index, div_disks_space.space_usage.shape)
            test_tag = max_index[1]
            index = max_index[0]
            if div_disks_space.insert(test_tag, size, index):
                tem.append(index+1)
                disks_state[index].insert(obj_id, size, div_disks_space.dif_space_point_index[index][test_tag][1]-size)
                tem += list(range(div_disks_space.start_point[index][tag-1]-size+1, div_disks_space.start_point[index][tag-1]+1))
                already_disk.append(index)
                copy_space[index,:] = 0#每次插入把这一行全部变成0            
        #===========换类顺插满了考虑换类离散插入=============
        else:
            dis_tem = div_disks_space.discrete_space_size[:,:,size-1:]#获得一个三维矩阵，该矩阵满足size能存下
            flat_index = np.argmax(dis_tem)
            # 使用 np.unravel_index 将扁平化索引转换为三维索引
            max_index = np.unravel_index(flat_index, dis_tem.shape) # disk, tag, size
            max_index[2] += size-1
            if div_disks_space.discrete_space_size[max_index[0]][max_index[1]][max_index[2]] > 0:#如果离散个数大于1才能插入
                tem.append(index+1)
                #==========div_disks_space类的离散插入===========
                #===========================================================================修改
                disks_state[index].insert(obj_id, size, div_disks_space.start_point[index][tag-1]-size)
                tem += list(range(div_disks_space.discrete_space[index][tag-1][size-1][0]+1, div_disks_space.discrete_space[index][tag-1][size-1][0]+size+1))
                div_disks_space.insert_discrete(index, size-1, tag-1, div_disks_space.discrete_space[index][tag-1][size-1][0], max_index[2])
                already_disk.append(index)
                copy_space[index,:] = 0#每次插入把这一行全部变成0       
        storge_list.append(tem)


