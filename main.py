
from init import *

from delete_action import *

from write_action import *

from read_action import*

from obj import *

from global_ import *

# #预处理
# T,M,N,V,G,free_data_array=get_init_info()


# obj_state = Obj_State()#定义的全局对象状态类：#1.state:0删除，1存在 2.tag 3.size 4.disks_id
# disks_state = []
# for i in range(N):
#     disks_state.append(Disk_State(V, M))
# div_disks_space = Div_Disk_Space(V,N,free_data_array,M)



#插入函数
    #用一个循环首先judge每一个盘够不够0.9space，然后使用离散空间，然后看能不能顺存
def insert_function(obj_id,size,tag):
    storge_list = []#返回给判题器的结果
    for obj_copy in range(3):
        #首先优先找离散位置
        for index in range(len(disks_state)):
            if size in disks_state[index].discrete_space[tag].keys():
                if len(disks_state[index].discrete_space[tag][size]) >= 0:
                    #只用给硬盘insert
                    disks_state[index].insert(obj_id,size,disks_state[index].discrete_space[tag][size][0])
                    tem = []
                    tem.append(index)
                    tem += list(range(disks_state[index].discrete_space[tag][size][0], disks_state[index].discrete_space[tag][size][0]+size))
                    disks_state[index].discrete_space[tag][size].remove(disks_state[index].discrete_space[tag][size][0])
                    break
        #顺插
        for index in range(len(disks_state)):
            if disks_state[index].judge(size):
                if div_disks_space.insert(tag,size,index):
                    disks_state[index].insert(obj_id,size,div_disks_space.dif_space_point_index[index][tag][1]-size)
                    tem = []
                    tem.append(index)
                    tem += list(range(disks_state[index].discrete_space[tag][size][0], disks_state[index].discrete_space[tag][size][0]+size))
                    break
# print( , file=sys.stderr)
if __name__ == '__main__':
    
    


 
    for item in range(1, N + 1):
        disk_point[item] = 1
    for item in range(1, T + EXTRA_TIME + 1):
        timestamp_action()
        delete_action()
        write_action(N,V)
        read_action(N)
