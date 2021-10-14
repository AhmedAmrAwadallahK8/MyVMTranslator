import VMT
import sys
import os


def extract(file_name):
    file_contents = []
    with open(file_name, 'r') as f:
        file_contents = f.readlines()
    return file_contents


def load_asm(file_content, vm_file_name):
    extension_ind = vm_file_name.find('.')
    if extension_ind != -1:
        asm_file_name = vm_file_name[:extension_ind] + '.asm'
    else:
        asm_file_name = vm_file_name + '.asm'
    with open(asm_file_name, 'w') as f:
        for line in file_content:
            f.write(line)


def find_vm_files(file_list):
    sys_file = []
    vm_files = []
    sys_file_present = False
    for file in file_list:
        vm_extension_ind = file.find('.vm')
        if vm_extension_ind != -1:
            if file[:vm_extension_ind] == 'Sys':
                sys_file.append(file)
                sys_file_present = True
            else:
                vm_files.append(file)
    return sys_file + vm_files, sys_file_present


def main(vm_files, sys_file_present, direc_name):
    final_asm_code = []
    for vm_file_name in vm_files:
        vm_code = []
        if vm_file_name.find('Sys') != -1:
            vm_code.append('call Sys.init 0\n')
        vm_code += extract(vm_file_name)
        code = VMT.VMT(vm_code, sys_file_present, vm_file_name[:vm_file_name.find('.vm')])
        code.parse()
        final_asm_code += code.output_asm()
    load_asm(final_asm_code, direc_name)


input = sys.argv[1]
py_or_direc = input.find('.vm')
if py_or_direc == -1:
    input_direc = input
    orig_path = os.getcwd()
    new_path = orig_path + '/' + input_direc
    os.chdir(new_path)
    vm_file_list, sys_file_present = find_vm_files(os.listdir())
    main(vm_file_list, sys_file_present, input_direc)
else:
    input_single_file = input
    main([input_single_file], False, input_single_file)



