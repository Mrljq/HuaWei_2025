'''
读操作
'''
from init import *
from queue import PriorityQueue
import numpy as np
from itertools import product
import sys
from collections import defaultdict
def get_score(time, obj):
    x = int(time) - int(obj.begin_time)
    if x <= 10:
        f_x = 1 - 0.005 * x
    elif x < 105:
        f_x = 1.05 - 0.01 * x
    else:
        f_x = 0
    return f_x * (obj.block_num + 1) * 0.5

class Object:
    __slots__ = ('begin_time', 'id', 'block_num', 'block_mask', 'well', 'delete_times')
    def __init__(self, begin_time, obj_id, block_num):
        self.begin_time = begin_time
        self.id = obj_id
        self.block_num = block_num
        self.block_mask = (1 << block_num) - 1  # 位掩码表示块的存在
        self.well = False
        self.delete_times = 0

    def delete_block(self, block_id):
        if self.block_mask & (1 << (block_id-1)):
            self.block_mask ^= (1 << (block_id-1))
            self.delete_times += 1
            if self.delete_times == self.block_num:
                self.well = True

class HashCollection:
    def __init__(self):
        self.hash_map = defaultdict(set)  # {object_id: set(Object)}

    def exists_block(self, obj_id, block_id):
        for obj in self.hash_map.get(obj_id, set()):
            if obj.block_mask & (1 << (block_id-1)):
                return True
        return False
    
    def exists(self, num):
        """查询是否存在指定编号的元素，O(1)时间复杂度"""
        return num in self.hash_map and len(self.hash_map[num]) > 0
    
    def clear(self,disks,obj_id):
        for disk in disks:
            index=np.where(disk.storge_space==obj_id)[0]
            if len(index)>0 :
                disk.request_num[index]-=len(self.hash_map[obj_id])       
        self.hash_map[obj_id].clear()
    

    def delete_min(self, obj_id, block_id, timestamp, disks):
        well_list = []
        delete_score = 0
        to_remove = []
        for obj in list(self.hash_map.get(obj_id, set())):
            obj.delete_block(block_id)
            if obj.well:
                well_list.append(obj.id)
                to_remove.append(obj)
                delete_score += get_score(timestamp, obj)

        if well_list:
            for disk in disks:
                indices = np.where(disk.storge_space == obj_id)[0]
                disk.request_num[indices] -= len(well_list)
        
        for obj in to_remove:
            self.hash_map[obj_id].discard(obj)
            if not self.hash_map[obj_id]:
                del self.hash_map[obj_id]
        
        return well_list, delete_score
    
    def is_empty(self):
        """判断集合是否为空"""
        return len(self.hash_map) == 0

def a_star(disks, read_queue, timestamp):
    action_map = {'r':1, 'j':3, 'p':2, 's':4}
    state = tuple(4 if disk.do_nothing else 0 for disk in disks)
    path = {disk.id: [] for disk in disks}
    finish_ids = []

    while True:
        if is_goal_state(disks, read_queue):
            # print('jieshu',file=sys.stderr)
            return path, finish_ids

        actions, new_finish = generate_optimal_actions(disks, read_queue, timestamp)
        finish_ids.extend(new_finish)
        
        for idx, action in enumerate(actions):
            disk = disks[idx]
            # print(action,file=sys.stderr)
            update_disk_state(disk, action,read_queue)
            if action=='r':
                path[disk.id].append(action)  
                if disk.do_nothing==True:
                    if path[disk.id][-1]!="#":
                        path[disk.id].append("#")   
            elif action=='j':
                target_position=np.argmax(disk.request_num)
                act=action+' '+str(target_position+1)
                path[disk.id].append(act)   
                
            elif action=='p':
                path[disk.id].append(action) 
                if disk.do_nothing==True:
                    if path[disk.id][-1]!="#":
                        path[disk.id].append("#")  
            elif action=='s':
                disk.do_nothing=True
            
            if disk.do_nothing==True and disk.left_G>0:
                if path[disk.id][-1]!="#":
                    path[disk.id].append("#")    
            
            
        
        state = tuple(action_map[action] for action in actions)

def generate_optimal_actions(disks, read_queue, timestamp):
    actions = []
    finish_ids = []
    for disk in disks:
        if disk.do_nothing:
            actions.append('s')
            continue
            
        current_pos = disk.point_index
        obj_id = disk.storge_space[current_pos]
        block_id = disk.storge_space_block[current_pos]
        
        if read_queue.exists_block(obj_id, block_id):
            if disk.left_G >= disk.read_s:
                well, _ = read_queue.delete_min(obj_id, block_id, timestamp, disks)
                finish_ids.extend(well)
                actions.append('r')
            else:
                actions.append('s')
        else:
            if disk.left_G == disk.G:
                target = np.argmax(disk.request_num)
                actions.append('j' if abs(target - current_pos) > disk.G else 'p')
            else:
                actions.append('p')
    return actions, finish_ids

def update_disk_state(disk, action,read_queue):
    if read_queue.is_empty():
        disk.do_nothing=True   
    if action == 'r':
        disk.move(2)
    elif action == 'j':
        disk.move(0, np.argmax(disk.request_num))
    elif action == 'p':
        disk.move(1)
    # stay无需操作

def is_goal_state(disks, read_queue):
    return all(disk.do_nothing for disk in disks) or read_queue.is_empty()

def read_action(timestamp, read_queue, disks, obj_state, count):
    nRead = int(input())
    # print(f'时间片{timestamp}读取请求个数为{nRead}',file=sys.stderr)
    for _ in range(nRead):
        req_id, obj_id = map(int, input().split())
        # print(f'第{req_id}个请求：\n请求编号{req_id}，请求对象编号{obj_id}',file=sys.stderr)
        block_num = obj_state.state_table[obj_id][1]
        obj = Object(timestamp, req_id, block_num)
        read_queue.hash_map[obj_id].add(obj)
        for disk in disks:
            idx = np.where(disk.storge_space == obj_id)[0]
            disk.request_num[idx] += 1

    if not read_queue.hash_map:
        print('\n'.join(['#']*10))
        print(0)
        sys.stdout.flush()
        return read_queue, disks, obj_state, count

    actions, finish_ids = a_star(disks, read_queue, timestamp)
    
    for disk in disks:
        print(''.join(actions[disk.id]))
        # print(''.join(actions[disk.id]),finish_ids,file=sys.stderr)
    print(len(finish_ids))
    for fid in finish_ids:
        print(fid)
    sys.stdout.flush()
    return read_queue, disks, obj_state, count