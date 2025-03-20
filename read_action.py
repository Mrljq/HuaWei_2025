'''
读操作
'''
from init import *
from queue import PriorityQueue

from itertools import product
from itertools import islice
from copy import deepcopy

from concurrent.futures import ThreadPoolExecutor, as_completed
from global_ import *
from heapq import heappush, heappop

def read_action(N):
    
    nRead = int(input())
    
    for i in range(1, nRead + 1):
        read_input = input().split()
        request_id = int(read_input[0])
        objectId = int(read_input[1])
        
        if objectId in read_queue.keys():
            read_queue[objectId].appned(request_id)
        else:
            read_queue.update({objectId:[request_id]})
    update_read_times(disks_state, read_queue)
    all_results,has_finished=greedy_algorithm(disks_state,read_queue)
    del_read_times(disks_state, has_finished)
    for result in all_results:
        action= ''.join(result) 
        print(action)
    print(len(has_finished))
    for id in has_finished:
        print(id)  
    sys.stdout.flush()
    
# def find_target(read_queue):
    
#     return None

def delet_queue(read_queue,has_readed):
    has_finished=[]
    has_readed_obj_id.extend(has_readed)
    for obj_id in has_readed:
        has_finished.extend(read_queue[obj_id])
        #read_queue[obj_id]=[]
        read_queue.pop(obj_id)
        
    return has_finished

def greedy_algorithm(disks,read_queue):
    #disk硬盘类，read_queue读取请求
    all_results = []
    for disk in disks:
        if disk.do_nothing==True:
            print('#')  #stay
            continue
        
        results=find_trace(disk,read_queue)
        if disk.left_G==disk.G:
            if results:
                valid_action,has_readed,new_disk=results
                read_queue.delet(has_readed)
                disk=new_disk
            else:
                valid_action=['j']
                target=0 #find_target(read_queue)
                disk.move(0,target)
        else:
            valid_action,has_readed,new_disk=results
            has_finished=delet_queue(read_queue,has_readed)
            disk=new_disk

        all_results.append(valid_action)
        
    return all_results,has_finished


   
def find_trace(disk,read_queue):
    valid_action = []
    new_disk=deepcopy(disk)
    has_readed=[]
    #score=0
    while new_disk.left_G>0:
     
        if new_disk.get_id(new_disk.point_index) in read_queue.keys():
            try_result=read_id(disk)
            if try_result:
                disk1,action=try_result
                new_disk=disk1
                del disk1
                valid_action.extend(action)
                has_readed.append(new_disk.get_id(new_disk.point_index))
            else:
                valid_action.append('#')
                break
            # new_disk.move(2)   # read
            # valid_action.append('r')
            # new_disk.left_G-=new_disk.read_s
            
            #score+=get_read_score(new_disk)
        else:
            new_disk.move(1)
            valid_action.append('p')
            new_disk.left_G-=1
    if valid_action[-1]!='#':
        valid_action.append('#')
        

    if len(has_readed)>0:   #超参数
        return [valid_action,has_readed,new_disk]
    else:
        return None


def read_id(disk):
    disk1=deepcopy(disk)
    size=disk1.find_sequences()[0][2]
    action=[]
    for _ in range(size):
        disk1.move(2) 
        disk1.left_G-=disk1.read_s
        action.appned('r')
        if disk1<0:
            del disk1
            return None,['#']
    return disk1,action
    







def generate_valid_combinations(disks, read_queue):
    """生成有效动作组合的生成器（内存友好）"""
    
    for disk in disks:
        if disk.do_nothing==True:
            print('#')  #stay
            continue
        all_results = []
        for read_id,req_id in read_queue:

            target_pos=disk.get_target_pos(read_id)
            if   not target_pos: #disk.has_obj(item):
                continue
            current_pos = disk.point_index

            if disk.left_G==disk.G:
                valid_action=['jump']
                new_disk=deepcopy(disk)
                new_disk.left_G=0
                has_readed=[]
                results_score=0
                all_results.append([valid_action,has_readed,results_score,new_disk])
            
            results=find_trace(disk,read_id,target_pos,read_queue)
            if results!= None:
                all_results.append(results)
        
        index=get_max_score(results)
        action=results[index][0]
        has_readed=results[index][1]
        disk=results[index][3]

        read_queue.delet(has_readed)#差个函数没实现
        

        

        
            
def get_max_score(results):
    max_index=0
    max_score=-100
    for i ,result in  enumerate(results):
        if max_score<result[2]:
            max_score=result[2]
            max_index=i
    return max_index


    






def action_is_value():
    return True

def get_read_score(disk):
    base_score=0
    if disk.point_sequence[0][2]>1:
        #基础得分
        return base_score
    else:
        #基础得分+真实得分
        return base_score+get_reall_read_score(disk)
    
def get_pass_score():
    return 0
def get_jump_score():
    return 0
def get_stay_score():
    return 0

def get_reall_read_score(disk):
    obj_read_star_id=0
    obj_read_end_id=disk.id
    obj_size=2
    x=obj_read_end_id-obj_read_star_id
    f_x=0
    if x>=0 and x<=10:
        f_x=1-0.005*x
    elif x>10 and x<105:
        f_x=1.05-0.01*x
    g_x=(obj_size+1)*0.5
    return f_x*g_x








def calculate_heuristic(next_state,disks,read_queue):
    None
    
def read_action():
    None
