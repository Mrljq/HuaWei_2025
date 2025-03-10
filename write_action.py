'''
写操作
'''
from init import *


def print_next(message):
    print(f"{message}", end="")

def do_object_write(object_unit, disk_unit, size, object_id,V):
    current_write_point = 0
    for i in range(1, V + 1):
        if disk_unit[i] == 0:
            disk_unit[i] = object_id
            current_write_point += 1
            object_unit[current_write_point] = i
            if current_write_point == size:
                break
    assert (current_write_point == size)


def write_action(N,V):
    n_write = int(input())
    for i in range(1, n_write + 1):
        write_input = input().split()
        write_id = int(write_input[0])
        size = int(write_input[1])
        objects[write_id].lastRequestPoint = 0
        for j in range(1, REP_NUM + 1):
            objects[write_id].replica[j] = (write_id + j) % N + 1
            objects[write_id].unit[j] = [0 for _ in range(size + 1)]
            objects[write_id].size = size
            objects[write_id].isDelete = False
            do_object_write(objects[write_id].unit[j], disk[objects[write_id].replica[j]], size, write_id,V)
        print(f"{write_id}")
        for j in range(1, REP_NUM + 1):
            print_next(f"{objects[write_id].replica[j]}")
            for k in range(1, size + 1):
                print_next(f" {objects[write_id].unit[j][k]}")
            print()
    sys.stdout.flush()