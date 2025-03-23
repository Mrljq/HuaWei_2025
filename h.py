'''
读操作
'''
from init import *
from queue import PriorityQueue

from itertools import product,islice
from copy import deepcopy

from concurrent.futures import ThreadPoolExecutor, as_completed
import math
# from my_need import div_disk_space
from heapq import heappush, heappop

class MaxPriorityItem:
    def __init__(self, priority, state):
        self.priority = priority
        self.state = state

    def __lt__(self, other):  # 定义小于操作符
        return self.priority > other.priority 

def get_score(time,obj):
    obj_read_star_id=obj.begin_time
    obj_read_end_id=time
    obj_size=obj.block_num
    x=int(obj_read_end_id)-int(obj_read_star_id)
    f_x=0
    if x>=0 and x<=10:
        f_x=1-0.005*x
    elif x>10 and x<105:
        f_x=1.05-0.01*x
    g_x=(obj_size+1)*0.5
    return f_x*g_x  
# class Object:
#     def __init__(self, begin_time, obj_id, block_num):
#         self.block = {i+1:1 for i in range(block_num)}
#         self.begin_time = begin_time
#         self.id = obj_id         # 不可变唯一标识符
#         self.well = False
#         self.delete_times = 0
#         self.block_num = block_num

#     def delete(self, tar_block_num):
#         if self.block.get(tar_block_num, 0) == 1:
#             self.block[tar_block_num] = 0
#             self.delete_times += 1
#             # 当所有块都被删除时标记为可清除
#             if self.delete_times >= self.block_num:  # 使用>=增强鲁棒性
#                 self.well = True

#     def __hash__(self):
#         return hash(self.id)  # 基于不可变ID计算哈希值

#     def __eq__(self, other):
#         return isinstance(other, Object) and self.id == other.id

# class HashCollection:
#     def __init__(self):
#         self.hash_map = {}  # {num: set(Object)}

#     def insert(self, num, obj):
#         """安全插入对象"""
#         if not isinstance(obj, Object):
#             raise TypeError("只能插入Object实例")
            
#         if num not in self.hash_map:
#             self.hash_map[num] = set()
#         self.hash_map[num].add(obj)

#     def exists(self, num):
#         """存在性检查优化"""
#         return bool(self.hash_map.get(num, None))

#     def exists_block(self, num, block_id):
#         """块存在性检查优化"""
#         objs = self.hash_map.get(num, set())
#         return any(obj.block.get(int(block_id), 0) == 1 for obj in objs)

#     def clear(self, disks, obj_id):
#         """安全清除对象"""
#         objs = self.hash_map.get(obj_id, set())
#         if not objs:
#             return

#         # 更新磁盘状态
#         for disk in disks:
#             indices = np.where(disk.storge_space == obj_id)[0]
#             if len(indices) > 0:
#                 disk.request_num[indices] -= len(objs)
        
#         # 清除对象集合
#         del self.hash_map[obj_id]

#     def delete_min(self, num, block_num, time, disks):
#         """安全删除操作"""
#         well_list = []
#         to_remove = []
#         delete_score = 0
        
#         # 创建集合副本避免迭代时修改
#         current_objs = list(self.hash_map.get(num, set()))
        
#         # 第一阶段：标记待删除对象
#         for obj in current_objs:
#             original_well = obj.well
#             obj.delete(block_num)
            
#             # 检查状态变化
#             if not original_well and obj.well:
#                 well_list.append(obj.id)
#                 to_remove.append(obj)
#                 score = get_score(time, obj)  # 假设已定义get_score
#                 delete_score += score

#         # 第二阶段：执行删除操作
#         if num in self.hash_map:
#             for obj in to_remove:
#                 self.hash_map[num].discard(obj)  # 安全删除
            
#             # 清除空集合
#             if not self.hash_map[num]:
#                 del self.hash_map[num]

#         # 第三阶段：更新磁盘状态
#         if well_list:
#             for disk in disks:
#                 indices = np.where(disk.storge_space == num)[0]
#                 if len(indices) > 0:
#                     disk.request_num[indices] -= len(well_list)

#         # 调试输出优化
#         if num == 132:
#             current = self.hash_map.get(num, set())
#             print(f"[DEBUG] 对象132当前数量：{len(current)}", file=sys.stderr)
#             for obj in current:
#                 state = (
#                     f"ID:{obj.id} Blocks:{obj.block} "
#                     f"Deleted:{obj.delete_times}/{obj.block_num} "
#                     f"Status:{'WELL' if obj.well else 'ALIVE'}"
#                 )
#                 print(state, file=sys.stderr)
                
#         return well_list, delete_score

#     def is_empty(self):
#         """空检查优化"""
#         return not bool(self.hash_map)
class Object():
    def __init__(self,begin_time,id,block_num):
        self.block={}
        self.begin_time=begin_time 
        self.id=id  
        self.well=False
        self.delete_times=0
        self.block_num=block_num
        for i in range(block_num):
            self.block[i+1]=1


    def delete(self,tar_block_num):
        if self.block[tar_block_num]==1:
            self.block[tar_block_num]=0
            self.delete_times+=1
            if self.delete_times==self.block_num:
                self.delete_times=0
                self.well=True    
    def __hash__(self):
        return hash(self.id)  # 基于不可变id计算哈希

    def __eq__(self, other):
        return self.id == other.id  # 根据id判断相等性
    
        
   


class HashCollection:
    def __init__(self):
        self.hash_map = {}  

    def insert(self, num ,Object):
        """插入元素（编号，时间点）"""
        if num not in self.hash_map:
            self.hash_map[num] = set()
        self.hash_map[num].add(Object)

    def exists(self, num):
        """查询是否存在指定编号的元素，O(1)时间复杂度"""
        return num in self.hash_map and len(self.hash_map[num]) > 0

    def exists_block(self, num, block_id):
        """检查指定编号的特定块是否存在"""
        if num not in self.hash_map:
            return False
        for obj in self.hash_map[num]:
            # print(obj.block,file=sys.stderr)
            if obj.block[int(block_id)] == 1:
                return True
        return False
    
    def clear(self,disks,obj_id):
        for disk in disks:
            index=np.where(disk.storge_space==obj_id)[0]
            if len(index)>0 :
                disk.request_num[index]-=len(self.hash_map[obj_id])       
        self.hash_map[obj_id].clear()
        
    def delete_min(self, num,block_num,time,disks):
        """num对象编号：objectID"""
        well_list=[]
        to_remove=[]
        delete_score=0
        list_obj = self.hash_map.get(num, set()).copy()
        
    
        for obj in list_obj:
            #这里会改变obj的某些值
            obj.delete(block_num)
           
            if obj.well:
                well_list.append(obj.id)
                to_remove.append(obj)
                score=get_score(time,obj)
                delete_score+=score  
        if len(well_list)>0:
            for disk in disks:
                index=np.where(disk.storge_space==num)[0]
                if len(index)>0 :
                    disk.request_num[index]-=len(well_list)       
        # 在迭代结束后删除对象
        for obj in to_remove:
            self.hash_map[num].remove(obj)  
            
        return well_list,delete_score                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           
      
    def is_empty(self):
        """判断集合是否为空"""
        return len(self.hash_map) == 0


def a_star(disks,read_queue,timestamp,obj_state):
    # print('现在处理到A星算法',file=sys.stderr)
    #disk硬盘类，read_queue读取请求

    #初始化优先队列，最大的值先出
    priority_queue = PriorityQueue()

    '''
    0:开始
    1:read
    2:pass
    3:jump
    4:#
    '''
    #定义初始状态，(0,0,0,0,0,0,0,0,0,0)
    start_state =tuple(0 for i in range(len(disks))) 

    #初始化路径
    A_path={}
    
    #初始化请求id
    finish_id=[]
    
    #初始化状态进入优先队列
    priority_queue.put(MaxPriorityItem(0, start_state))
    c=1
    while True:
        c+=1
        # if c>100:
        #     print(dsa)
        
        #获取优先队列中得分最高的状态
        item =priority_queue.get()
        priority_queue.queue.clear()
        value = item.priority  # 获取优先级
        state = item.state  # 获取状态

        #根据state更新状态
        A_path=updata_all_state(state,disks,read_queue,A_path,timestamp,obj_state)
        # print(A_path)
        
        #判读是否达到目标
        if is_goal_state(disks,read_queue):
            # print('A星算法结束',file=sys.stderr)
            return  A_path,finish_id
        
        '''
        【generate_successors】函数获得当前状态的所有相邻状态
        '''
        neighbors,well_list=generate_successors(disks,read_queue,timestamp)
        
        if len(well_list)>0:
            finish_id.extend(well_list)
            
        for action_value,next_state  in neighbors:
            #计算新状态的g得分
            new_value = value + int(action_value)

            #计算新状态的h得分
            # heuristic = calculate_heuristic(next_state,disks,read_queue)
            
            heuristic=0
            #将下一个状态进入优先队列
            priority_queue.put(MaxPriorityItem(new_value + heuristic, next_state))  


def updata_all_state(state,disks,read_queue,A_path,timestamp,obj_state):
    # well_list=[]
    for disk in disks:
        # print(state,file=sys.stderr)
        if state[disk.id]==0 :
            #开始
            A_path[disk.id]=[]
            continue
        elif state[disk.id]==1:
            #read
            
            current_pos=disk.point_index
            target_block_id=disk.storge_space_block[current_pos]
            obj_id=disk.storge_space[current_pos]
            A_path[disk.id].append("r")
            disk.move(2)
            if disk.do_nothing==True:
                if A_path[disk.id][-1]!="#":
                    A_path[disk.id].append("#")    
            
        elif state[disk.id]==2:
            #pass
            
            A_path[disk.id].append("p")
            disk.move(1)
            
            if disk.do_nothing==True:
                if A_path[disk.id][-1]!="#":
                    A_path[disk.id].append("#")
        elif state[disk.id]==3:
            #jump
            # target_position=disk.get_jump_positon()
            target_position=np.argmax(disk.request_num)
            A_path[disk.id].append("j "+str(target_position+1))
            disk.move(0,target_position)
        elif state[disk.id]==4:
            disk.do_nothing=True
        if disk.do_nothing==True and disk.left_G>0:
                if A_path[disk.id][-1]!="#":
                    A_path[disk.id].append("#")    
    # print(state[4],disks[4].left_G,disks[4].do_nothing,file=sys.stderr)        
    return A_path
        
def is_goal_state(disks,read_queue):
    '''
    1.读取队列为空
    2.剩余token为0
    '''
    is_goal_of_diskdonothing=True
    is_goal_of_request=False
    for disk in disks:
        if disk.do_nothing:  ##disk类需要声明do_nothing，True表示此时无法进行任何行动
            continue
        #如果仍然有硬盘do_nothing值为false，判断条件2不成立
        is_goal_of_diskdonothing=False
    #如果请求队列为空
    if read_queue.is_empty():
        is_goal_of_request==True
        # print("kong",file=sys.stderr)
        

    #条件1或者条件2即可返回A*
    return is_goal_of_diskdonothing or is_goal_of_request



def generate_successors(disks,read_queue,timestamp):
    # print('现在寻找所有邻居状态',file=sys.stderr)
    
    #初始化所有邻居节点
    neighbors=[]

    # 生成所有有效的动作组合（生成器）[(r,r,r,r,r,p,p,p,p,j).......]
    action_combinations,well_list = generate_valid_combinations(disks, read_queue,timestamp)
    # print(len(action_combinations),file=sys.stderr)
    neighbors=process_chunk(action_combinations,disks, read_queue)
    return neighbors,well_list
   



import itertools
def generate_valid_combinations(disks, read_queue,timestamp):
    # print('现在寻找所有可行动作序列',file=sys.stderr)
    
    valid_actions = []
    well_list = []
    for disk in disks:
        disk_id = disk.id

        current_pos=disk.point_index
        obj_id=disk.storge_space[current_pos]
        target_block_id=disk.storge_space_block[current_pos]
        
        if disk.do_nothing:
            actions = ['stay']
            valid_actions.append(actions)
            continue
        if read_queue.exists_block(obj_id,target_block_id):
            if disk.left_G >= disk.read_s:
                valid_actions.append(['read'])
                well_list1,_=read_queue.delete_min(obj_id,target_block_id,timestamp,disks)
                well_list.extend(well_list1)
            else:
                valid_actions.append(['stay'])
            continue
        if disk.left_G == disk.G:
            # actions = ["jump", "pass"]  
            action=get_begin_action(disk)
            valid_actions.append(action)
        else:
            valid_actions.append(['pass'])   
    return list(itertools.product(*valid_actions)),well_list

def get_begin_action(disk):
    target_position=np.argmax(disk.request_num)
    if abs(target_position-disk.point_index)>disk.G:
        return ['jump']
    else:
        return ['pass']

def process_chunk(chunk,  disks, read_queue):
    
    # print('处理单进程',file=sys.stderr)
    """处理单个分块的动作组合"""
    chunk_neighbors = []
    ACTION_MAP = {
        'read': 1,
        'jump': 3,
        'pass': 2,
        'stay': 4
    }
    for action_combo in chunk:
        temp_disks = disks
        # temp_disks = disks
        total_value = 0
        # new_read_queue = deepcopy(read_queue)  ###创建副本
        new_read_queue = read_queue

        # 并行执行动作
        state_temp=[]
        for disk_idx, action in enumerate(action_combo):
            # print(disk_idx,action,file=sys.stderr)
            disk = temp_disks[disk_idx]
            
         
            value = _execute_single_action(
                disk, 
                action
            )
            total_value += value

            state_temp.append(ACTION_MAP[action]) 
 
        # 构建新状态（示例）
        new_state = tuple(state_temp)
        chunk_neighbors.append((total_value,new_state))
    # print(chunk_neighbors[0],file=sys.stderr)
    return chunk_neighbors




def _execute_single_action(disk, action):
    """执行单个硬盘动作"""  
    if action == 'read':
        temp_score=get_read_score(disk)
    elif action == 'jump':
        temp_score=get_jump_score()
    elif action == 'pass':
        temp_score=get_pass_score()
    elif action == 'stay':
        temp_score=get_stay_score()
    return temp_score




def get_read_score(disk):
    base_score=0.5
    current_pos=disk.point_index
    X=disk.storge_space[current_pos]
    if X==disk.storge_space[current_pos+1]:
        #基础得分
        return base_score
    else:
        #基础得分+真实得分
        return base_score+get_reall_read_score(disk)    
def get_pass_score():
    return 0
def get_jump_score():
    return -.1
def get_stay_score():
    return 0

def get_reall_read_score(disk):
    return 0.5
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
    # print(next_state,file=sys.stderr)
    h=0
    for disk in disks:
        h+=get_one_disk_h(next_state[disk.id],disk,read_queue)
    return h
    

def get_one_disk_h(state,disk,read_queue):
    read_value=0
    now_left_G=disk.left_G
    now_pos=disk.point_index
    now_read_s=disk.read_s
    fu=0
    if state==1:
        #read
        next_read_s=math.ceil(max(now_read_s * 0.8,16))
        next_left_G=(now_left_G-next_read_s)+(fu*disk.G)
        next_pos=1+now_pos
        
    elif state==2:
        #jump
        next_read_s=64
        next_left_G=0+(fu*disk.G)
        next_pos=np.argmax(disk.request_num)

        
    elif state==3:
        #pass
        next_read_s=64
        next_left_G=(now_left_G-1)+(fu*disk.G)
        next_pos=1+now_pos
    
    else:
        #stay
        next_read_s=math.ceil(max(now_read_s * 0.8,16))
        next_left_G=0+(fu*disk.G)
        next_pos=now_pos
    
    next_pos=next_pos % disk.unit_len    
    # have_read=set()
    while next_left_G>0:
        # 目前地目标编号
        pos_obj_id=disk.storge_space[next_pos]

        # obj_id=disk.storge_space[current_pos]
        target_block_id=disk.storge_space_block[next_pos]
        if read_queue.exists_block(pos_obj_id,target_block_id):
            next_read_s=math.ceil(max(next_read_s * 0.8,16))

            if disk.storge_space[next_pos]!=disk.storge_space[next_pos+1]:
                read_value+=1
            else:
                read_value+=0.5
            next_left_G-=next_read_s
            pos_obj_id+=1
        else:
            next_left_G-=1
            next_read_s=64    
        next_pos+=1
        next_pos=next_pos % disk.unit_len                   
    return read_value


def read_action(timestamp,read_queue,disks,obj_state,count):

    '''
    timestamp:每个时间片初始获取 int
    disks:全局变量,包含10个硬盘 [disk]
    read_queue:全局变量
    obj_state:每个类的信息
    '''
    #############初始化################
    '''
    read_queue=HashCollection()
    '''
    # obj_state = Obj_State(M)
    ###################################
    count=count
    #获取这一时间片读取对象的个数：nRead
    nRead=int(input())
    # print(f'时间片{timestamp}读取请求个数为{nRead}',file=sys.stderr)
    #获取每个读取对象的【请求编号】和【请求对象编号】
    for i in range (1,nRead+1):
        read_input = input().split() 
        #【请求编号】
        
        request_id = int(read_input[0])
        
        #【请求对象编号】
        objectId = int(read_input[1])
        if objectId==132:
            count+=1
        # print(f'第{i}个请求：\n请求编号{request_id}，请求对象编号{objectId}',file=sys.stderr)
        #获取对象编号为objectID的block个数
        # print(obj_state.state_table[objectId],file=sys.stderr)
        obj_block_num=obj_state.state_table[objectId][1]
        
        for disk in disks:
            index = np.where(disk.storge_space == objectId)[0]
            # print(disk.id,index,objectId,file=sys.stderr)
            
            # print(disk.id,index,file=sys.stderr)
            if len(index)>0:
                disk.request_num[index]+=1
        #封装obj
        obj=Object(timestamp,request_id,obj_block_num)

        #对应的【请求编号】和【时间片】插入到请求集合【read_queue】中
        read_queue.insert(objectId,obj)
        

    #如果请求队列为空，直接返回
    if not len(read_queue.hash_map):
        for i in range(len(disks)):
            print('#')
        print(0)
        #刷新缓冲区域
        sys.stdout.flush()
        #返回全局变量
        return read_queue,disks,obj_state,count


    #获得每个磁盘地动作序列/获取当前时间片读取完成的编号
    disks_actions,finish_id=get_disks_actions(disks,read_queue,timestamp,obj_state)
    # disks_actions[i]="rrrpp#"
    ####

    #输出每个磁盘的动作序列
    for i in range(len(disks)):

        print(''.join(disks_actions[i]))
        # print(len(''.join(disks_actions[i])),file=sys.stderr)
        # print(''.join(disks_actions[i]),file=sys.stderr)


    #上报当前时间片上报读取完成的请求个数
    print(len(finish_id))
    # print(len(finish_id),file=sys.stderr)
    #输出完成的编号
    for i in range(len(finish_id)):
        print(finish_id[i])
        # print(finish_id[i],file=sys.stderr)

    #刷新缓冲区域
    sys.stdout.flush()

    #返回全局变量
    # print(count,file=sys.stderr)
    return read_queue,disks,obj_state,count






def get_disks_actions(disks,read_queue,timestamp,obj_state):
    A_path,finish_id=a_star(disks,read_queue,timestamp,obj_state)
    # if int(timestamp) == 1978:
    #     print(A_path,file=sys.stderr)
    # print(finish_id[0],file=sys.stderr)
    return A_path,finish_id