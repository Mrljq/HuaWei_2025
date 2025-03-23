
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


import time

# print( , file=sys.stderr)
if __name__ == '__main__':
    # print('timestamp',file=sys.stderr)
    
    # read_queue_ght=OptimizedHashCollection()
    read_queue_ght= HashCollection()

    count=0
    del_time=write_time=read_time=0
    for item in range(1, N + 1):
        disk_point[item] = 1
    for item in range(1, T + EXTRA_TIME + 1):
        timestamp=timestamp_action()
        # if int(timestamp)>18000:
        #     print(timestamp,file=sys.stderr)
        
        del_begin_time=time.time() 
        delete_action(timestamp,read_queue_ght)
        del_end_time=time.time() 
        del_time+=del_end_time-del_begin_time
        if int(timestamp) % 1800==0:
            print('delete_time',del_time,file=sys.stderr)
            del_time=0
            
            
        wr_begin_time=time.time()    
        write_action(obj_state,disks_state,div_disks_space)
        wr_end_time=time.time() 
        write_time+=wr_end_time-wr_begin_time
        if int(timestamp) % 1800==0:
            print('write_time',write_time,file=sys.stderr)
            write_time=0
          
            
        re_begin_time=time.time()    
        read_queue_ght,disks_state,obj_state,count=read_action(timestamp,read_queue_ght,disks_state,obj_state,count)
        re_end_time=time.time() 
        read_time+=re_end_time-re_begin_time
        if int(timestamp) % 1800==0:
            print('read_time',read_time,file=sys.stderr)
            read_time=0
        # print(timestamp,file=sys.stderr)

        # print(count,timestamp,file=sys.stderr)
      
