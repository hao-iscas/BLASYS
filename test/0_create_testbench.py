import os
import sys
import subprocess

def generate_commands_list(base_path, all=False):
    '''
        all : Boolean => indicate the disable or not for testbenchs already created.
    '''
    assert os.path.isdir(base_path)

    if all:
        files_verilog = [f for f in os.listdir(base_path) if os.path.isfile(os.path.join(base_path,f)) and f.endswith('.v') and not f.endswith('_tb.v')]
    else:
        files_verilog = [f for f in os.listdir(base_path) if os.path.isfile(os.path.join(base_path,f)) and f.endswith('.v')]

    commands_list = []
    for f in files_verilog:
        bench_name = f.split('.')[0]
        commands_list.append('python3 testbench.py -i ' + os.path.join(base_path, f) + ' -o ' + os.path.join(base_path, bench_name) + '_tb.v')
    
    return commands_list

if __name__ == '__main__':
    assert len(sys.argv) == 2

    commands_list = generate_commands_list(sys.argv[-1], all=True)
    
    for command in commands_list:
        print(command)
        subprocess.run(command, shell=True)
    


