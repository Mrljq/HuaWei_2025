
from init import *

from delete_action import *

from write_action import *

from read_actionght import*

from obj import *

from global_ import *

# #预处理
# T,M,N,V,G,free_data_array=get_init_info()


# obj_state = Obj_State()#定义的全局对象状态类：#1.state:0删除，1存在 2.tag 3.size 4.disks_id
# disks_state = []
# for i in range(N):
#     disks_state.append(Disk_State(V, M))
# div_disks_space = Div_Disk_Space(V,N,free_data_array,M)




# print( , file=sys.stderr)
if __name__ == '__main__':
    # print('timestamp',file=sys.stderr)
    
    read_queue_ght=HashCollection()

 
    for item in range(1, N + 1):
        disk_point[item] = 1
    for item in range(1, T + EXTRA_TIME + 1):
        timestamp=timestamp_action()
        # print(timestamp,file=sys.stderr)
        
        delete_action(timestamp)
        
        write_action(obj_state,disks_state,div_disks_space)
        
        read_queue_ght,disks_state,obj_state=read_action(timestamp,read_queue_ght,disks_state,obj_state)
        print(timestamp,file=sys.stderr)
        # if int(timestamp)>3:
        #     break
      
