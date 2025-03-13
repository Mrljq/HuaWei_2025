from init import *
from obj import *

#预处理
T,M,N,V,G,free_data_array=get_init_info()


obj_state = Obj_State()#定义的全局对象状态类：#1.state:0删除，1存在 2.tag 3.size 4.disks_id
disks_state = []
for i in range(N):
    disks_state.append(Disk_State(V, M))
div_disks_space = Div_Disk_Space(V,N,free_data_array,M)