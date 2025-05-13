import os, re, json
from multiprocessing import Pool
from clean_replace_vlg import clean_vlg, clean_map_vlg

def run_one_design(para):
    bench, design, top_name, clk, reset = para
    print(f"Running {design}")
    ys_template = f"./run_ys_template.ys"
    ys_scr = f"./run_{design}.ys"
    with open(ys_template, "r") as f:
        lines = f.readlines()
    
    ### change path here ###
    ## 1. original RTL code path
    ## change the RTL path first
    design_path = f"{config['rtl_base_path']}/{bench}/rtl/{design}/"
    ## 2. BOG output path
    os.makedirs(f"{config['output_base_path']}/{cmd}/generated_netlist_file", exist_ok=True)
    os.makedirs(f"{config['output_base_path']}/{cmd}/mapped_netlist", exist_ok=True)
    os.makedirs(f"{config['output_base_path']}/{cmd}/generated_sdc_file", exist_ok=True)
    save_path = f"{config['output_base_path']}/{cmd}/generated_netlist_file/{top_name}_{design}_TYP.syn.v"
    mapped_save_path = f"{config['output_base_path']}/{cmd}/mapped_netlist/{top_name}_{design}_TYP.syn.v"
    #######################
    if bench in ['itc']:
        read_line = f"read  -verific;\nread -vhdl {design_path}/{design}.vhd\n"
    else:
        read_line = f"read_verilog {design_path}/*.v\n"

    with open(ys_scr, "w") as f_scr:
        f_scr.writelines(read_line)
        for line in lines:
            line = line.replace("design_top", top_name)
            line = line.replace("lib_name", f"nangate45_{cmd}.lib")
            line = line.replace("save_path", save_path)
            f_scr.writelines(line)
    os.system(f"yosys {ys_scr}")
    os.system(f"rm -rf {ys_scr}")

    os.system(f"cp {config['sdc_template']} {config['output_base_path']}/{cmd}/generated_sdc_file/{top_name}_{design}_TYP.sdc")

    dst_path = f"{config['output_base_path']}/{cmd}/generated_sdc_file/{top_name}_{design}_TYP.sdc"
    # Read and modify the file
    with open(dst_path, 'r') as f:
        lines = f.readlines()

    # Apply substitutions line by line
    modified_lines = []
    for line in lines:
        # Replace ' clk ' and ' resetn ' with proper variable values
        line = re.sub(r'\bclk\b', clk, line)
        line = re.sub(r'\bresetn\b', reset, line)
        modified_lines.append(line)

    # Write back to the file
    with open(dst_path, 'w') as f:
        f.writelines(modified_lines)

    clean_map_vlg(save_path, mapped_save_path)



def run_all(bench, design_name=None):
    
    with open(config["design_json"], 'r') as f:
        design_data = json.load(f)
        bench_data = design_data[bench]
    for name, v in bench_data.items():
        top_name = v[0]
        clk = v[1]
        reset = v[2]
        para = (bench, name, top_name, clk, reset)
        if design_name:
            if name == design_name:
                run_one_design(para)
        else:
            run_one_design(para)




def run_all_parallel(bench):
    para_lst = []
    with open(config["design_json"], 'r') as f:
        design_data = json.load(f)
        bench_data = design_data[bench]
    for name, v in bench_data.items():
        top_name = v[0]
        para = (bench, name, top_name, v[1], v[2])
        para_lst.append(para)
    
    with Pool(20) as p:
        p.map(run_one_design, para_lst)
        p.close()
        p.join()



if __name__ == '__main__':
    
    with open("paths.json", "r") as path_file:
        config = json.load(path_file)

    with open(config["properties"], "r") as f:
        properties = json.load(f)

    global cmd
    cmd = properties["cmd"]
    assert cmd in ['SOG', 'AIG', 'AIMG', 'XAG']

    with open(config["design_json"], 'r') as f:
        design_data = json.load(f)
    
    bench_list_all = list(design_data.keys())    
    design_name = ''

    for bench in bench_list_all:
        # run_all(bench, design_name)
        run_all_parallel(bench)
