'''
读操作
'''
from init import *
from queue import PriorityQueue

from itertools import product
from itertools import islice
from copy import deepcopy

from concurrent.futures import ThreadPoolExecutor, as_completed

from my_need import div_disk_space
from heapq import heappush, heappop

class MaxPriorityItem:
    def __init__(self, priority, state):
        self.priority = priority
        self.state = state

    def __lt__(self, other):  # 定义小于操作符
        return self.priority > other.priority 


class HashCollection:
    def __init__(self):
        self.hash_map = {}  # 键为编号，值为最小堆（列表）

    def insert(self, num, time):
        """插入元素（编号，时间点）"""
        if num not in self.hash_map:
            self.hash_map[num] = []
        heappush(self.hash_map[num], time)

    def exists(self, num):
        """查询是否存在指定编号的元素，O(1)时间复杂度"""
        return num in self.hash_map and len(self.hash_map[num]) > 0

    def delete_min(self, num):
        """删除编号num的最小时间点元素，返回是否成功删除"""
        if num not in self.hash_map:
            return False
        heap = self.hash_map[num]
        if not heap:
            return False
        heappop(heap)
        if not heap:  # 堆为空时删除键以节省内存
            del self.hash_map[num]
        return True
    def is_empty(self):
        """判断集合是否为空"""
        return len(self.hash_map) == 0

# read_queue= HashCollection()
# read_queue.insert(1,10)
# read_queue.insert(1,11)
# read_queue.insert(1,13)


def a_star(disks,read_queue):
    #disk硬盘类，read_queue读取请求

    #初始化优先队列，最大的值先出
    priority_queue = PriorityQueue()

    #初始化已读请求列表
    finish_queue= HashCollection()


    #定义初始状态，
    start_state = (
    tuple(node.disk_p for node in disks), 
    tuple(node.left_G for node in disks),
    read_queue
    )


    #初始化路径
    A_path=[]
    
    #初始化状态进入优先队列
    priority_queue.put(MaxPriorityItem(0, start_state))

    #定义visited集合
    visited=set()

    while True:
        #获取优先队列中得分最高的状态
        value,state=priority_queue.get()
        
        #判读是否达到目标
        if is_goal_state(disks,read_queue):
            return  A_path
        
        #如果state访问过，则跳过该state
        if state in visited:
            continue

        #在path中加入新状态
        A_path.append(state)

        #该状态已经被访问
        visited.add(state)


        '''
        【generate_successors】函数获得当前状态的所有相邻状态
        '''
        for next_state, action_value in generate_successors(state, disks,read_queue):

            #计算新状态的g得分
            new_value = value + action_value

            #计算新状态的h得分
            heuristic = calculate_heuristic(next_state, disks,read_queue)

            #将下一个状态进入优先队列
            priority_queue.put(MaxPriorityItem(new_value + heuristic, next_state))  




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

    #条件1或者条件2即可返回A*
    return is_goal_of_diskdonothing or is_goal_of_request



def generate_successors(disks,read_queue):

    #初始化所有邻居节点
    neighbors=[]

    # 生成所有有效的动作组合（生成器）
    action_combinations = generate_valid_combinations(disks, read_queue)
    
    # 并行处理配置
    CHUNK_SIZE = 100  # 每个任务处理1000个组合
    MAX_WORKERS = 8    # 8并行
    
    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        # 将组合分块处理
        futures = []
        while True:

            #处理一小批动作集合
            chunk = list(islice(action_combinations, CHUNK_SIZE))
            if not chunk:
                break
            
            # 提交分块任务
            future = executor.submit(
                process_chunk,  # 处理单个分块的函数
                chunk=chunk,
                disks=disks,
                read_queue=read_queue
            )
            futures.append(future)
        
        # 收集结果
        for future in as_completed(futures):
            try:
                chunk_result = future.result()
                neighbors.extend(chunk_result)
            except Exception as e:
                print(f"Error processing chunk: {e}")
    
    return neighbors


def generate_valid_combinations(disks, read_queue):

    """
    1.生成有效动作组合的生成器（内存友好）
    2.disks指向全局变量
    3.read_queue指向全局变量
    """
    #初始化可行的动作组合
    valid_actions = []

    for disk in disks:

        #disk.point_sequence[0]：（起始位置，编号，长度） 0表示当前指针读取的目标
        #获取disk的当前磁头指向的编号
        current_pos = disk.point_sequence[0][1]

        #如果磁盘不能干事了，则该时间片磁盘动作结束：输出#
        if disk.do_nothing==True:
            valid_actions.append(['stay'])
        else:
            # 如果disk的磁头指向的编号存在于读请求队列中
            if read_queue.exists(current_pos):
                #如果磁头剩余token大于读取需要花费的toekn
                if disk.left_G>=disk.read_s:
                    #此disk只能读
                    valid_actions.append(['read'])
                    #这里如果不删除read_queue.delete_min(current_pos),则后续磁盘也会选择，两个磁盘可能读同一个目标
                else:
                #否则，磁盘选择结束
                    valid_actions.append(['stay'])
                    
            else:
                if disk.left_G==disk.G:
                    valid_actions.append(['jump', 'pass'])
                else:
                    valid_actions.append(['pass','stay'])
    
    # 使用惰性生成避免内存爆炸
    for combo in product(*valid_actions):
        # 快速预过滤无效组合
        if action_is_value(combo):
            yield combo



def process_chunk(chunk,  disks, read_queue):
    """处理单个分块的动作组合"""
    chunk_neighbors = []
    
    for action_combo in chunk:
        # 这里复用之前的单线程处理逻辑
        temp_disks = deepcopy(disks)
        # temp_disks = disks
        total_value = 0
        is_valid = True
        new_read_queue = deepcopy(read_queue)  ###创建副本
        # new_read_queue = read_queue

        # 并行执行动作
        for disk_idx, action in enumerate(action_combo):
            disk = temp_disks[disk_idx]
            
            try:
                # 执行动作并验证
                value = _execute_single_action(
                    disk, 
                    action,
                    new_read_queue
                )
                total_value += value
            except InvalidActionException:
                is_valid = False
                break
                
        if not is_valid:
            continue
            
        # 构建新状态（示例）
        new_state = (
            tuple(d.point_sequence[0][1] for d in temp_disks),  # 各硬盘当前位置
            tuple(d.left_G for d in temp_disks),                # 剩余token
            new_read_queue                               # 剩余请求
        )

        if is_valid:
            chunk_neighbors.append((new_state, total_value))
    
    return chunk_neighbors












class InvalidActionException(Exception):
    pass

def _execute_single_action(disk, action):
    """执行单个硬盘动作"""
    
    # 动作成本映射表
    COST_G_MAP = {
        'read': disk.read_s,
        'jump': disk.G,
        'pass': 1,
        'stay': 0
    }
    
    
    # 执行动作
    disk.left_G -= COST_G_MAP[action]
    if disk.left_G<=0:
        disk.do_nothing=True

    # 处理特殊动作效果
    if action == 'read':
        temp_score=get_read_score(disk)
        disk.move(2)

    elif action == 'jump':
        temp_score,target_position=get_jump_score(div_disk_space,disk,class_num)
        disk.move(0,target_position)
    elif action == 'pass':
        temp_score=get_pass_score(disk)
        disk.move(1)
    elif action == 'stay':
        disk.do_nothing=True
        temp_score=get_stay_score(disk)
        
    return temp_score







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
def get_jump_score(div_disk_space,disk,class_num):
    max_tag=class_num.index(max(class_num))
    target_position=div_disk_space.dif.space_point_index[disk.id][max_tag][0]
    return 0,target_position
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








def calculate_heuristic(disks,read_queue):
    h=0
    for disk in disks:
        h+=get_one_disk_h(disk,read_queue)
    

def get_one_disk_h(disk,read_queue):
    left_G=disk.left_G
    read_value=0
    read_s=disk.read_s
    current_pos = disk.point_sequence[0][1]
    p=0
    is_new_obj=0
    while left_G>0:
        # 目前地目标编号
        current_pos=disk.point_sequence[p][1]
        if read_queue.exists(current_pos):
            if is_new_obj==0:
                len_current_obj=disk.point_sequence[p][2]
            read_s=max(16,round(read_s*0.8))
            len_current_obj-=1
            if len_current_obj==1:
                is_new_obj=1
                ##得分
                read_value+=1
                p+=1
            else:
                read_value+=0.5
            left_G-=read_s
        else:
            left_G-=1
            read_s=64   
    return read_value



def read_action(timestamp,read_queue,class_num,disks):

    '''
    timestamp:每个时间片初始获取
    class_num:全局变量，表示每个类的个数
    disks:全局变量
    read_queue:全局变量
    '''
    #获取这一时间片读取对象的个数：nRead
    nRead=int(input)
    
    #获取每个读取对象地【请求编号】和【请求对象编号】
    for i in range (1,nRead+1):
        read_input = input().split() 
        #【请求编号】
        request_id = int(read_input[0])

        #【请求对象编号】
        objectId = int(read_input[1])

        #对应的【请求编号】和【时间片】插入到请求集合【read_queue】中
        read_queue.insert(request_id,timestamp)
        
        #对应的【请求对象编号】加1
        class_num[objectId]+=1


    #获得每个磁盘地动作序列
    disks_actions=get_disks_actions()

    #输出每个磁盘的动作序列
    for i in range(len(disks)):
        print(disks_actions[i])

    #获取当前时间片读取完成的编号
    finish_id=get_finish_id()

    #上报当前时间片上报读取完成的请求个数
    print(len(finish_id))

    #输出完成的编号
    for i in range(len(finish_id)):
        print(finish_id[i])

    #刷新缓冲区域
    sys.stdout.flush()

    #返回全局变量
    return read_queue,class_num,disks






def get_disks_actions(disks,read_queue):

    A_path=a_star(disks,read_queue)

    disks_actions=A_path
    return disks_actions