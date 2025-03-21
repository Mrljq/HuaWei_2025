import sys
import numpy as np
REP_NUM = 3


class Disk_State:
    def __init__(self,storge_space,m,g):
        self.storge_space = np.full(storge_space, 0)#0代表没有，id就是存储的对象id
        self.point_index = 1 #代表磁针位置，如果与storge_space对应请-1
        self.discrete_space = {} #存储当前硬盘的离散空间
        self.point_sequence = None
        self.left_G = g
        self.already_storge = 0#已经存储的大小,这里存和删都要改
        self.read_token_cost = 64
        for i in range(1,1+m):
            self.discrete_space[i] = {}
    
    def insert(self, obj_id, size, index):#插入时将占用的空间用对象id修改，0代表没有占用
        self.storge_space[index:index+size] = obj_id
        self.already_storge += size
    
    def del_obj(self, obj_id, size, tag):
        self.already_storge -= size
        # 将数组中的所有1替换为-1
        self.storge_space[self.storge_space == obj_id] = 0
        # 使用numpy.where找到特定元素的所有下标
        indices = np.where(self.storge_space == obj_id)[0]
        if size in self.discrete_space[tag].keys():
            self.discrete_space[tag][size].append(indices)
        else:
            self.discrete_space[tag][size] = []

    def move(self, class_move, move_target=0):#0代表跳跃，1代表pass，2代表read,对于1和2 move_target设置为0
        if class_move == 0:
            self.point_index = move_target
            self.read_token_cost = 64
        elif class_move == 1:
            self.point_index += 1
            self.read_token_cost = 64
        else:
            self.point_index += 1
            self.read_token_cost = max(self.read * 0.8,16)

    def update_point_sequence(self):
        tem = self.find_sequences(self.storge_space)
        self.point_sequence = tem[self.point_index:]
        self.point_sequence += tem[:self.point_index]
    #==================该函数用于获取指针序列======================
    #np.array([5,5, 1, 1, 1, 2, 2, 0, 0, 0])
    #========(储存单元下标，对象id，size)============================
    #[(0, 5, 2), (2, 1, 2), (4, 2, 2), (6, 0, 3)]
    def find_sequences(self):
        # 找到值变化的位置
        change_points = np.where(self.storge_space[:-1] != self.storge_space[1:])[0] + 1
        # 添加数组开头和结尾的索引
        segments = np.concatenate(([0], change_points, [len(self.storge_space)]))
        # 计算每个段的起始索引、值和长度
        sequences = [(segments[i], self.storge_space[segments[i]], segments[i+1] - segments[i]) for i in range(len(segments)-1)]
        return sequences