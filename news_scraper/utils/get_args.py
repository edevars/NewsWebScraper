import sys

def get_args():
    arg_dic = dict()
    for i in range(1,len(sys.argv)):
        opt_arr = sys.argv[i].split('=')
        arg_dic[opt_arr[0]] = opt_arr[1]
    return arg_dic