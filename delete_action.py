'''
删除操作
'''
from init import *
# from init import _id ,objects,req_is_dones,req_prev_ids
from global_ import *

def delete_action():
    n_delete = int(input())
    abortNum = 0
    del_read = []
    for i in range(1, n_delete + 1):
        de_id = int(input())
        delete_function(de_id)
        if de_id in read_queue.keys():
            for r_id in read_queue[de_id]:
                del_read.append(r_id)
            abortNum += len(read_queue[de_id])

    # for i in range(1, n_delete + 1):
    #     delete_id = _id[i]
    #     currentId = objects[delete_id].lastRequestPoint
    #     while currentId != 0:
    #         if not req_is_dones[currentId]:
    #             abortNum += 1
    #         currentId = req_prev_ids[currentId]

    print(f"{abortNum}")
    for d_id in del_read:
        print(f"{d_id}")
    # for i in range(n_delete + 1):
    #     delete_id = _id[i]
    #     currentId = objects[delete_id].lastRequestPoint
    #     while currentId != 0:
    #         if not req_is_dones[currentId]:
    #             print(f"{currentId}")
    #         currentId = req_prev_ids[currentId]
    #     for j in range(1, REP_NUM + 1):
    #         do_object_delete(objects[delete_id].unit[j], disk[objects[delete_id].replica[j]], objects[delete_id].size)
    #     objects[delete_id].isDelete = True
    sys.stdout.flush()



def do_object_delete(object_unit, disk_unit, size):
    for i in range(1, size + 1):
        disk_unit[object_unit[i]] = 0

def delete_function(obj_id):
    # 计算数组中1的个数
    size = obj_state.state_table[obj_id][2]
    tag = obj_state.state_table[obj_id][1]
    disks_id = obj_state.state_table[obj_id][3]
    for disk_id in disks_id:
        disks_state[id].del_obj(obj_id, size, tag)