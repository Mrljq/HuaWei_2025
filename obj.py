'''
定义一些类
'''
import numpy as np

REP_NUM = 3




# class Object:
#     def __init__(self):
#         self.replica = [0 for _ in range(REP_NUM + 1)]
#         self.unit = [[] for _ in range(REP_NUM + 1)]
#         self.size = 0
#         self.lastRequestPoint = 0
#         self.isDelete = False

class Obj_State:
    def __init__(self,m):
        self.state_table = {}
        self.tag_state = np.zeros(m)
        #state,tag,size
        #state:0删除，1存在 postion(list):start_position,end_position
    def del_obj(self,obj_id):
        if obj_id in self.state_table.keys():
            self.state_table[obj_id][0] = 0
    def insert_obj(self,obj_id,tag,size, disks_id):
        self.state_table[obj_id] = []
        self.state_table[obj_id].append(1)
        self.state_table[obj_id].append(tag)
        self.state_table[obj_id].append(size)
        self.state_table[obj_id].append(disks_id)
        self.tag_state[tag] += 1

obj_state = Obj_State()

class Disk_State:
    def __init__(self, storge_space, m):
        self.storge_space = np.full(storge_space, -1)
        self.point_index = 0
        self.read_s = 64
        self.point_sequence
        self.point_
        self.left_G
        self.already_storge = 0#已经存储的大小
        self.discrete_space = {} #离散空间
        for i in m:
            self.discrete_space[i] = {}
    
    def insert(self, obj_id, size, index):#插入时将占用的空间用对象id修改，-1代表没有占用
        self.storge_space[index:index+size] = obj_id
        self.already_storge += size
    
    def move(self, class_move, move_target=0):#0代表跳跃，1代表pass，2代表read,对于1和2 move_target设置为0
        if class_move == 0:
            self.point_index = move_target
            self.read_s = 64
        elif class_move == 1:
            self.point_index += 1
            self.read_s = 64
        else:
            self.point_index += 1
            self.read_s = max(self.read * 0.8,16)
    
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
    
    def del_obj(self, obj_id):
        # 计算数组中1的个数
        size = obj_state.state_table[obj_id][2]
        tag = obj_state.state_table[obj_id][1]
        self.already_storge -= size
        # 将数组中的所有1替换为-1
        self.storge_space[self.storge_space == obj_id] = -1
        # 使用numpy.where找到特定元素的所有下标
        indices = np.where(self.storge_space == obj_id)[0]
        if size in self.discrete_space[tag].keys():
            self.discrete_space[tag][size].append(indices)
        else:
            self.discrete_space[tag][size] = []
       

    def judge(self, size):
        if (self.already_storge + size) >= 0.9*len(self.storge_space):
            return False
        else:
            return True
    #====================用于计算特定对象到磁头的距离========================
    def distance_head(self, obj_id):
        indices = np.where(self.storge_space == obj_id)[0]
        return indices

#===============该类用于在插入时告诉插入位置=========================
class Div_Disk_Space:
    def __init__(self, storge_space, n ,free_data_array,m):
        self.dif_space_point_index = {}#用来存储所有硬盘划分后每一个类的指针位置，从指针位置开始插入
        self.percentage = []
        self.compute_percentage(free_data_array,m,storge_space)
        for i in n:
            self.dif_space_point_index[i] = []#每一个硬盘self.dif_space_point_index[i]有一个list[(ori1,current1),(ori2,current2)]
            p = 0
            for i1 in self.percentage:
                self.dif_space_point_index[i].append(p,p)
                p += i1
        self.discrete_space = {}
        for i in n:
            self.discrete_space[i] = {}
            for i1 in m:
                self.discrete_space[i][i1] = []

    def compute_percentage(self,free_data_array,m,storge_space):
        w_d = free_data_array[m:2*m]-free_data_array[0:m]
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

    def insert(self, obj_class, size, disk_id):
        if self.dif_space_point_index[disk_id][obj_class][1] + size >=  self.dif_space_point_index[disk_id][obj_class+1][0]:
            return False 
        else:
            self.dif_space_point_index[disk_id][obj_class][1] += size


