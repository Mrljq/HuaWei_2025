'''
删除操作
'''
from init import *
# from init import _id ,objects,req_is_dones,req_prev_ids
from global_ import *

def delete_action(timestamp,read_queue_ght):
    n_delete = int(input())
    # if int(timestamp)==2313:
    #     print('ssss',n_delete,file=sys.stderr)
    
    
    abortNum = 0
    del_read = []
    for i in range(1, n_delete + 1):
        de_id = int(input())
        # if int(timestamp)==2313:
        #     print(read_queue_ght.hash_map[100200],file=sys.stderr)
        #     print('ssss',de_id,read_queue_ght.exists(4),file=sys.stderr)
        # delete_function(de_id)
        if read_queue_ght.exists(de_id):
            for item in read_queue_ght.hash_map[de_id]:
                del_read.append(item.id)
            abortNum += len(del_read)
            read_queue_ght.clear(disks_state,de_id)
        delete_function(de_id)    
                
        # if de_id in read_queue.keys():
        #     for r_id in read_queue[de_id]:
        #         del_read.append(r_id)
        #     abortNum += len(read_queue[de_id])

    # for i in range(1, n_delete + 1):
    #     delete_id = _id[i]
    #     currentId = objects[delete_id].lastRequestPoint
    #     while currentId != 0:
    #         if not req_is_dones[currentId]:
    #             abortNum += 1
    #         currentId = req_prev_ids[currentId]
    
    # if int(timestamp)==2313:
    #     print(del_read,file=sys.stderr)
    #     print(1)
    #     print(1628)
        # print(f"{abortNum}")

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
    size = obj_state.state_table[obj_id][1]
    tag = obj_state.state_table[obj_id][0]
    disks_id = obj_state.state_table[obj_id][2]
    for disk_id in disks_id:
        index_obj = disks_state[disk_id].del_obj(obj_id)
        obj_state.del_obj(disk_id, size, tag-1, index_obj)