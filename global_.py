from init import *
from obj import *
REP_NUM = 3
#预处理
T,M,N,V,G,free_data_array=get_init_info()

read_queue={}

has_readed_obj_id=[]
obj_state = Obj_State(M)#定义的全局对象状态类：#1.state:0删除，1存在 2.tag 3.size 4.disks_id
disks_state = []
for i in range(N):
    disks_state.append(Disk_State(V, M))
div_disks_space = Div_Disk_Space(V,N,free_data_array,M)

def update_read_times(disks, obj_read):
    for disk in disks:
        for obj_id in obj_read.keys():
            indics = np.where(disk.storge_space == obj_id)[0]
            disk.read_times[indics] = len(obj_read[obj_id])

def del_read_times(disks, has_read):
    for disk in disks:
        for obj_id in has_read.keys():
            indics = np.where(disk.storge_space == obj_id)[0]
            disk.read_times[indics] = 0
        

