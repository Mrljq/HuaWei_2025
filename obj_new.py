import sys
import numpy as np
REP_NUM = 3

import math
#===========================该类的tag正常===================
class Obj_State:
    def __init__(self,m):
        self.state_table = {}
        # self.tag_state = np.zeros(m)
        #state,tag,size
        #state:0删除，1存在 postion(list):start_position,end_position
    def del_obj(self,obj_id):
        if obj_id in self.state_table.keys():
            self.state_table.pop(obj_id)
    def insert_obj(self,obj_id,tag,size, disks_id):
        self.state_table[obj_id] = []
        self.state_table[obj_id].append(tag)
        self.state_table[obj_id].append(size)
        self.state_table[obj_id].append(disks_id)
        # self.tag_state[tag] += 1


#===========================================该类的index，tag从0开始================
class Disk_State:
    def __init__(self,storge_space,m,g,disk_id):
        self.storge_space = np.full(storge_space, 0)#0代表没有，id就是存储的对象id
        self.storge_space_block=np.full(storge_space, -1)
        self.point_index = 0 #代表磁针位置，如果与storge_space对应请-1
        self.point_sequence = None
        self.left_G = g
        self.id=disk_id
        self.G=g
        self.read_token_cost = 64
        self.read_s=64
        self.do_nothing=False
        self.unit_len=storge_space
        self.request_num=np.full(storge_space, -1)  #后续需要完成请求之后删除
        self.processed = []
        self.move_cost=1
    

    def insert(self, obj_id, size, index):#插入时将占用的空间用对象id修改，0代表没有占用,insert_type:0代表正常插入，1代表离散插入
        self.storge_space[index:index+size] = obj_id
        # print('asasasasasasasa',self.id,self.storge_space[index:index+size],file=sys.stderr)
        self.storge_space_block[index:index+size]=np.arange(1, size + 1)

    def del_obj(self, obj_id):
        # 使用numpy.where找到特定元素的所有下标
        indices = np.where(self.storge_space == obj_id)[0] #这里返回的是一个array
        # 将数组中的所有1替换为-1
        self.storge_space[self.storge_space == obj_id] = 0
        
        self.storge_space_block[indices]= 0
        return indices[0]

    def move(self, class_move, move_target=0):#0代表跳跃，1代表pass，2代表read,对于1和2 move_target设置为0
        if class_move == 0:
            self.point_index = move_target
            self.read_token_cost = 64
            self.read_s=64
            self.left_G=0
        elif class_move == 1:
            self.point_index += 1
            self.point_index=self.point_index % self.unit_len
            self.read_token_cost = 64
            self.read_s=64
            self.left_G-=1
        else:
            self.point_index += 1
            self.point_index=self.point_index % self.unit_len
            self.left_G-=self.read_s
            self.read_s = math.ceil(max(self.read_s * 0.8,16))
            
        if self.left_G<=0:
            self.do_nothing=True    
    def update_point_sequence(self):
        tem = self.find_sequences()
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
    
    def judge(self, size):
        if (self.already_storge + size) >= 0.9*len(self.storge_space):
            return False
        else:
            return True
    #====================用于计算特定对象到磁头的距离========================
    def distance_head(self, obj_id):
        indices = np.where(self.storge_space == obj_id)[0]
        return indices
    
    
#===============该类用于在插入时告诉插入位置（该类的index和tag都是从0开始的）=========================
class Div_Disk_Space:
    def __init__(self, storge_space, n ,free_data_array,m):
        self.current_point = np.zeros((n,m), dtype =int)#用于代表顺插头位置的矩阵
        self.start_point = np.zeros((n,m), dtype =int)#用于代表开始头位置的矩阵
        self.end_point = np.zeros((n,m), dtype =int)#用于代表顺插末位置的矩阵
        self.space_usage = np.zeros((n,m), dtype =int)#将末矩阵与头矩阵相减即可得到
        self.percentage = []
        self.init(free_data_array,m,storge_space)
        self.discrete_space = {}#应该是4维的：disk，tag, size，indexs
        self.discrete_space_size = np.zeros((n, m, 5))
        for i in range(n):
            self.discrete_space[i] = {}
            p = 0
            for i1 in range(len(self.percentage)):
                self.start_point[:,i1] = p
                self.current_point[:,i1] = p
                self.end_point[:,i1] = p+int(self.percentage[i1])
                p += int(self.percentage[i1])
            for i2 in range(m):#每一个硬盘一开始没有离散空间
                self.discrete_space[i][i2] = {}
                for size in range(1,6):
                    self.discrete_space[i][i2][size] = []
        #===================这里新加入一个指示当预存类满时的可存储空间==========
        self.tag_full_space = []
        self.update_usage()
        
    def init(self,free_data_array,m,storge_space):
        w_d = free_data_array[m:2*m]-free_data_array[0:m]# [3,2]-[0,2]=[3,0]
        #============================计算累计峰值============================
        cul_write = []
        for i in range(len(w_d)):
            max_ = 0
            for i1 in w_d[i]:
                if max_ + i1 > max_:
                    max_ += i1
            cul_write.append(max_)
        cul_write = np.array(cul_write, dtype=int)
        total_sum = np.sum(cul_write)
        self.percentage = storge_space *cul_write / total_sum

    def insert(self, obj_class, size, disk_id):#这里插入类时候需要把，tag-1
        if self.space_usage[disk_id][obj_class] >= size:
            self.current_point[disk_id][obj_class] += size
            return True
        else:
            return False

    def insert_discrete(self, disk_id, obj_size, tag, index, discrete_size):
        self.discrete_space[disk_id][tag][discrete_size].remove(index)
        self.discrete_space_size[disk_id][tag][discrete_size-1] -= 1
        #非等值插入，离散空间大小一定更大
        if obj_size != discrete_size:
            self.discrete_space[disk_id][tag][discrete_size-obj_size].append(index+obj_size)#加入到剩余位置
            self.discrete_space_size[disk_id][tag][discrete_size-obj_size-1] += 1

    def update_usage(self):
        self.space_usage = self.end_point - self.current_point

    def del_obj(self, disk_id, size, tag, obj_index):
        self.discrete_space[disk_id][tag][size]
        self.discrete_space[disk_id][tag][size].append(obj_index)#这里只传入首个下标
        self.discrete_space_size[disk_id][tag][size-1] += 1

