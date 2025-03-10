'''
读操作
'''
from init import *


def read_action(N):
    request_id = 0
    nRead = int(input())
    for i in range(1, nRead + 1):
        read_input = input().split()
        request_id = int(read_input[0])
        objectId = int(read_input[1])
        req_object_ids[request_id] = objectId
        req_prev_ids[request_id] = objects[objectId].lastRequestPoint
        objects[objectId].lastRequestPoint = request_id
        req_is_dones[request_id] = False
    global current_request
    global current_phase
    if current_request == 0 and nRead > 0:
        current_request = request_id
    if current_request == 0:
        for i in range(1, N + 1):
            print("#")
        print("0")
    else:
        current_phase += 1
        objectId = req_object_ids[current_request]
        for i in range(1, N + 1):
            if i == objects[objectId].replica[1]:
                if current_phase % 2 == 1:
                    print(f"j {objects[objectId].unit[1][int(current_phase / 2 + 1)]}")
                else:
                    print("r#")
            else:
                print("#")
        if current_phase == objects[objectId].size * 2:
            if objects[objectId].isDelete:
                print("0")
            else:
                print(f"1\n{current_request}")
                req_is_dones[current_request] = True
            current_request = 0
            current_phase = 0
        else:
            print("0")
    sys.stdout.flush()
