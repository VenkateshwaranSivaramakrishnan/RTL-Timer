# from preprocess import *
import xgboost as xgb
from sklearn.model_selection import KFold

from sklearn.ensemble import RandomForestRegressor

import matplotlib.pyplot as plt
from matplotlib.lines import Line2D

import os, time, json, copy, pickle
import pandas as pd
import numpy as np
from multiprocessing import Pool
from random import shuffle
from stat_ import *
design_json = "/data/wenjifang/AIG_analyzer/LS-benchmark/design_timing_rgb.json"


def testing(test_lst):
    feat_label_dir = "../../feat_label/bit-wise"
    graph_feat_dir = "/home/coguest5/RTL-Timer/modeling/feat_label/graph_feat"
    pred_label_name_list = []
    for design_name in test_lst:
        with open (f"{feat_label_dir}/{design_name}.pkl", "rb") as f:
            feat_label_pair = pickle.load(f)
        
        feat_dict, label_dict = feat_label_pair

        # print(feat_dict)
        # print(label_dict)

        feat_arr = np.array(list(feat_dict.values()))
        print(feat_arr.shape)
        label_arr = np.array(list(label_dict.values()))
        label_arr = label_arr[:,0]
        
    
    
        df_feat = pd.DataFrame(feat_arr)
        df_feat.drop(df_feat.columns[[25]], axis=1, inplace=True)

        save_path = f"../saved_model/bit_ep_model_{design_name}.pkl"
        print('Testing ...')
        with open (save_path, "rb") as f:
            xgbr = pickle.load(f)
        pred = xgbr.predict(df_feat)

        keyPred = dict(zip(feat_dict.keys(), pred))

        with open(f"bitwise_predictions_{design_name}.pkl", "wb") as f:
            pickle.dump(keyPred, f)

        pred_label_name_list.append((pred, label_arr, design_name))

        regression_metrics(pred, label_arr)

        #plot_predictions(pred, label_arr, design_name)

        #plot_all_designs(pred_label_name_list, out_name="bitwise_all_designs.png")

        

def get_design_lst(bench):
    with open(design_json, 'r') as f:
        design_data = json.load(f)
        bench_data = design_data[bench]
    for k, v in bench_data.items():
        design_lst.append(k)

def plot_predictions(pred, label_arr, design_name):
    pred = np.array(pred)
    label_arr = np.array(label_arr)

    r = R_corr(pred, label_arr)
    mape_val = MAPE(pred, label_arr)
    rrse_val = RRSE(pred, label_arr)
    mae = MAE(pred, label_arr)

    fig, ax = plt.subplots(figsize=(6, 4))
    ax.scatter(label_arr, pred, alpha=0.6, edgecolors='k', linewidths=0.5)
    ax.plot([label_arr.min(), label_arr.max()],
            [label_arr.min(), label_arr.max()],
            'r--', linewidth=1.2)

    ax.set_xlabel("Post-Syn Bit AT (ns)", fontsize=10)
    ax.set_ylabel("Pred Bit AT (ns)", fontsize=10)
    ax.set_title(design_name, fontsize=11)

    ax.legend([
        f"r = {r:.3f}",
        f"MAPE = {mape_val:.3f}",
        f"RRSE = {rrse_val:.3f}",
        f"MAE = {mae:.3f}"
    ], fontsize=8, loc='upper left', frameon=True)

    ax.grid(True, linestyle='--', alpha=0.5)
    return fig, ax

def plot_all_designs(pred_label_name_list, out_name="bitwise_all_designs.png", cols=3):
    rows = (len(pred_label_name_list) + cols - 1) // cols
    fig, axs = plt.subplots(rows, cols, figsize=(6 * cols, 4 * rows), squeeze=False)

    axs_flat = axs.flatten()

    for idx, (pred, label_arr, design_name) in enumerate(pred_label_name_list):
        ax = axs_flat[idx]
        pred = np.array(pred)
        label_arr = np.array(label_arr)

        # Compute regression metrics
        r = R_corr(pred, label_arr)
        mape_val = MAPE(pred, label_arr)
        rrse_val = RRSE(pred, label_arr)
        mae = MAE(pred, label_arr)

        # Plot predicted vs actual
        ax.scatter(label_arr, pred, alpha=0.6, edgecolors='k', linewidths=0.5, label=None)

        # Ideal identity line y = x (dotted, with label)
        min_val = min(label_arr.min(), pred.min())
        max_val = max(label_arr.max(), pred.max())
        ax.plot([min_val, max_val],
                [min_val, max_val],
                'r--', linewidth=1.2, label='Ideal (y = x)')

        # Set labels and title
        ax.set_title(f"{design_name}", fontsize=11)
        ax.set_xlabel("Post-Syn Bit AT (ns)", fontsize=10)
        ax.set_ylabel("Pred Bit AT (ns)", fontsize=10)
        ax.grid(True, linestyle='--', alpha=0.5)

        # Dummy plots for metrics (so they appear in legend)
        ax.plot([], [], ' ', label=f"r = {r:.3f}")
        ax.plot([], [], ' ', label=f"MAPE = {mape_val:.3f}")
        ax.plot([], [], ' ', label=f"RRSE = {rrse_val:.3f}")
        ax.plot([], [], ' ', label=f"MAE = {mae:.3f}")

        # Unified legend
        ax.legend(fontsize=8, loc='upper left', frameon=True)

    # Hide any unused subplots
    for i in range(len(pred_label_name_list), len(axs_flat)):
        fig.delaxes(axs_flat[i])

    plt.tight_layout()
    plt.savefig(out_name, dpi=300)
    plt.close()

if __name__ == '__main__':
    bench_list_all = ['iscas','itc','opencores','VexRiscv','chipyard', 'riscvcores','NVDLA']

    design_name = 'TinyRocket'
    # design_name = ""

    global design_lst, phase
    design_lst = []
    phase = 'SYN'

    with open ("./design_js/test_lst.json", "r") as f:
        test_lst = json.load(f)
    
    testing(test_lst)

# def run_xgb_label(x_train, y_train):

#     y_train = y_train.astype(float)
#     xgbr = xgb.XGBRegressor(n_estimators=500, max_depth=100, nthread=25)

#     xgbr.fit(x_train, y_train)

#     # y_pred = xgbr.predict(x_test)
#     # y_pred2 = xgbr.predict(x_train)
#     with open ("../saved_model/ep_model_sog.pkl", "wb") as f:
#         pickle.dump(xgbr, f)




# if __name__ == '__main__':
#     label_data, feat_data = load_data()
#     x = feat_data
#     y = label_data ## seq label

#     # kFold_train(x, y, 'EP Model')
#     run_xgb_label(x, y)

