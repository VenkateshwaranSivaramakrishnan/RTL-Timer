import pickle, json 

import numpy as np

if __name__ == '__main__':
    with open('FPU.pkl', "rb") as f:
        test_lst = pickle.load(f)

    #for a in test_lst:
        #print(a)

    feat_dict, label_dict = test_lst

    temp = list(feat_dict.values())
    label_arr = list(label_dict.values())
    print(test_lst)
    with open("output.txt", "w") as f:
        print(test_lst, file=f)

