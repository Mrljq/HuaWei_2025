
from init import *

from delete_action import *

from write_action import *

from read_action import*





# print( , file=sys.stderr)
if __name__ == '__main__':
    #预处理
    T,M,N,V,G=get_init_info()
    



    for item in range(1, N + 1):
        disk_point[item] = 1
    for item in range(1, T + EXTRA_TIME + 1):
        timestamp_action()
        delete_action()
        write_action(N,V)
        read_action(N)
