import Command
import Branch
import Function
import Memory


class VMT:
    brnch_cmnds = ['if-goto', 'goto', 'label']
    func_cmnds = ['function', 'call']
    mem_cmnds = ['push', 'pop']
    op_cmnds = ['add', 'sub', 'neg', 'eq', 'gt', 'lt', 'and', 'or', 'not', 'return']
    SP_mem = '@256\nD=A\n@R0\nM=D\n'
    LCL_mem = '@11256\nD=A\n@R1\nM=D\n'
    ARG_mem = '@12256\nD=A\n@R2\nM=D\n'
    THIS_mem = '@13256\nD=A\n@R3\nM=D\n'
    THAT_mem = '@14256\nD=A\n@R4\nM=D\n'
    sys_file_code = SP_mem + LCL_mem + ARG_mem + THIS_mem + THAT_mem
    func_call_num_dict = {}
    current_func = ''

    def __init__(self, vm_code, sys_file_present, vm_file_name):
        self.vm_code = vm_code
        self.sys_file_present = sys_file_present
        self.vm_file_name = vm_file_name
        self.temp = None
        self.asm_code = None
        self.comp_op_num = 0

    def report_line_data(self):
        data = []
        for pair in self.temp:
            for p in pair:
                data.append(p.report_data())
        return data

    def parse(self):
        def clean_code(code):
            clean_code = []
            for line in code:
                comment_ind = line.find('//')
                newline_ind = line.find('\n')
                if comment_ind != -1:
                    if comment_ind != 0:
                        clean_code.append(line[:comment_ind])
                elif line[:newline_ind]:
                    clean_code.append(line[:newline_ind])
            return clean_code

        def parse_code(self, code):
            parsed_code = []
            for line in code:
                new_line = []
                line_l = line.split()
                cmnd = line_l[0]
                new_line.append(Command.Command(cmnd))
                if cmnd in self.mem_cmnds:
                    mem_type = line_l[1]
                    if mem_type == 'static':
                        new_line.append(Memory.Memory(self.vm_file_name, line_l[2]))
                    else:
                        new_line.append(Memory.Memory(mem_type, line_l[2]))
                elif cmnd in self.brnch_cmnds:
                    new_line.append(Branch.Branch(line_l[1]))
                elif cmnd in self.func_cmnds:
                    new_line.append(Function.Function(line_l[1], line_l[2]))
                parsed_code.append(new_line)
            return parsed_code

        self.temp = self.vm_code
        self.temp = clean_code(self.temp)
        self.temp = parse_code(self, self.temp)

    def output_asm(self):
        def translate_mem_push(memory, location):
            if memory == 'constant':
                return '@' + location + '\nD=A'
            elif memory == 'local':
                return '@' + location + '\nD=A\n@LCL\nA=M+D\nD=M'
            elif memory == 'argument':
                return '@' + location + '\nD=A\n@ARG\nA=M+D\nD=M'
            elif memory == 'this':
                return '@' + location + '\nD=A\n@THIS\nA=M+D\nD=M'
            elif memory == 'that':
                return '@' + location + '\nD=A\n@THAT\nA=M+D\nD=M'
            elif memory == 'pointer':
                pointer_loc = str(3 + int(location))
                return '@' + pointer_loc + '\nD=M'
            elif memory == 'temp':
                temp_loc = str(5 + int(location))
                return '@' + temp_loc + '\nD=M'
            else:
                return '@' + memory + '.' + location + '\nD=M'

        def translate_mem_pop(memory, location):
            if memory == 'constant':
                return 'YOU CANT POP CONSTANT MEMORY'
            elif memory == 'local':
                return '@' + location + '\nD=A\n@LCL\nD=M+D\n@R13\nM=D'
            elif memory == 'argument':
                return '@' + location + '\nD=A\n@ARG\nD=M+D\n@R13\nM=D'
            elif memory == 'this':
                return '@' + location + '\nD=A\n@THIS\nD=M+D\n@R13\nM=D'
            elif memory == 'that':
                return '@' + location + '\nD=A\n@THAT\nD=M+D\n@R13\nM=D'
            elif memory == 'pointer':
                pointer_loc = str(3 + int(location))
                return '@' + pointer_loc + '\nD=A\n@R13\nM=D'
            elif memory == 'pointer':
                pointer_loc = str(3 + int(location))
                return '@' + pointer_loc + '\nD=A\n@R13\nM=D'
            elif memory == 'temp':
                temp_loc = str(5 + int(location))
                return '@' + temp_loc + '\nD=A\n@R13\nM=D'
            else:
                return '@' + memory + '.' + location + '\nD=A\n@R13\nM=D'


        def translate_double_op(self, command):
            comp_op = '.' + str(self.comp_op_num)

            if command == 'add':
                return 'M=M+D\n'
            elif command == 'sub':
                return 'M=M-D\n'
            elif command == 'and':
                return 'M=M&D\n'
            elif command == 'or':
                return 'M=M|D\n'
            elif command == 'eq':  # JEQ

                self.comp_op_num += 1
                return ('D=M-D\n@TRUE' + comp_op
                        + '\nD;JEQ\n@SP\nA=M-1\nM=0\n@LEAVE' + comp_op + '\n0;JMP\n(TRUE' + comp_op
                        + ')\n@SP\nA=M-1\nM=-1\n@LEAVE' + comp_op + '\n0;JMP\n(LEAVE' + comp_op + ')\n')
            elif command == 'gt':  # JGT
                self.comp_op_num += 1
                return ('D=M-D\n@TRUE' + comp_op
                        + '\nD;JGT\n@SP\nA=M-1\nM=0\n@LEAVE' + comp_op + '\n0;JMP\n(TRUE' + comp_op
                        + ')\n@SP\nA=M-1\nM=-1\n@LEAVE' + comp_op + '\n0;JMP\n(LEAVE' + comp_op + ')\n')
            elif command == 'lt':  # JLT
                self.comp_op_num += 1
                return ('D=M-D\n@TRUE' + comp_op
                        + '\nD;JLT\n@SP\nA=M-1\nM=0\n@LEAVE' + comp_op + '\n0;JMP\n(TRUE' + comp_op
                        + ')\n@SP\nA=M-1\nM=-1\n@LEAVE' + comp_op + '\n0;JMP\n(LEAVE' + comp_op + ')\n')

        def translate_single_op(command):
            if command == 'neg':
                return 'M=-M\n'
            elif command == 'not':
                return 'M=!M\n'

        def translate_mem(command, memory, location):
            translation = None
            comment = '//' + command + ' ' + memory + ' ' + location + '\n'
            if command == 'push':
                translation = comment + translate_mem_push(memory, location) + '\n@SP\nA=M\nM=D\n@SP\nM=M+1\n'
            elif command == 'pop' and memory != 'constant':
                translation = comment + translate_mem_pop(memory, location) + \
                              '\n@SP\nA=M-1\nD=M\n@R13\nA=M\nM=D\n@SP\nM=M-1\n'
            else:
                translation = 'NO CONDITION MET'
            return translation

        def translate_op(command):
            translation = None
            comment = '//' + command + '\n'
            if command != 'neg' and command != 'not' and command != 'return':
                translation = comment + '@SP\nM=M-1\nA=M\nD=M\n@SP\nA=M-1\n' + translate_double_op(self, command)
            elif command == 'neg' or command == 'not':
                translation = comment + '@SP\nA=M-1\n' + translate_single_op(command)
            elif command == 'return':  # R14 = ENDFRAME R15 = retaddr
                move_efp = '@R14\nAM=M-1\nD=M\n'
                translation = (comment + '@LCL\nD=M\n@R14\nM=D\n@5\nD=A\n@R14\nA=M-D\nD=M\n@R15\nM=D\n@SP\n' +
                               'A=M-1\nD=M\n@ARG\nA=M\nM=D\n@ARG\nD=M+1\n@SP\nM=D\n' + move_efp + '@THAT\nM=D\n' +
                               move_efp + '@THIS\nM=D\n' + move_efp + '@ARG\nM=D\n' + move_efp + '@LCL\nM=D\n' +
                               '@R15\nA=M\n0;JMP\n')
            else:
                translation = 'NO CONDITION MET'
            return translation

        def translate_brnch(command, label):
            translation = ''
            comment = '//' + command + ' ' + label + '\n'
            translation += comment
            if command == 'label':
                translation += '(' + label + ')\n'
            elif command == 'goto':
                translation += '@' + label + '\n0;JMP\n'
            elif command == 'if-goto':
                translation += '@SP\nAM=M-1\nD=M\n@' + label + '\nD;JNE\n'
            return translation

        def translate_func(self, command, name, n_vars):
            translation = ''
            comment = '//' + command + ' ' + name + ' ' + n_vars + '\n'
            translation += comment
            if command == 'function':
                translation += ('(' + name + ')\n@' + n_vars + '\nD=A\n@R13\nM=D\n@' + name + '.nopush\nD;JEQ\n' +
                                '(' + name + '.push.' + n_vars +
                                ')\n@SP\nA=M\nM=0\n@SP\nM=M+1\n@R13\nMD=M-1\n@' + name + '.push.' + n_vars +
                                '\nD;JGT\n(' + name + '.nopush)\n')
            elif command == 'call':
                n_args = n_vars
                mem_push = 'D=M\n@SP\nAM=M+1\nM=D\n'
                func_call_num = 0

                if name in self.func_call_num_dict:
                    func_call_num = str(self.func_call_num_dict[name])
                    self.func_call_num_dict[name] = self.func_call_num_dict[name] + 1
                else:
                    self.func_call_num_dict[name] = 1
                    func_call_num = str(self.func_call_num_dict[name])
                    self.func_call_num_dict[name] = self.func_call_num_dict[name] + 1

                return_label = name + '$ret.' + func_call_num
                translation += ('@' + return_label + '\nD=A\n@SP\nA=M\nM=D\n@LCL\n' + mem_push + '@ARG\n' +
                                mem_push + '@THIS\n' + mem_push + '@THAT\n' + mem_push + '@SP\nM=M+1\n' +
                                '@5\nD=A\n@' + n_args + '\nD=D+A\n@SP\nD=M-D\n@ARG\nM=D\n@SP\nD=M\n@LCL\n' +
                                'M=D\n@' + name + '\n0;JMP\n(' + return_label + ')\n')
            else:
                translation += 'NOT IMPLEMENTED YET'
            return translation

        asm = []
        if self.sys_file_present:
            asm.append(self.sys_file_code)

        for line in self.temp:
            cmnd = line[0].report_data()['cmnd']
            if cmnd in self.mem_cmnds:
                mem = line[1].report_data()['mem']
                loc = line[1].report_data()['loc']
                asm.append(translate_mem(cmnd, mem, loc))
            elif cmnd in self.op_cmnds:
                asm.append(translate_op(cmnd))
            elif cmnd in self.brnch_cmnds:
                lbl = line[1].report_data()['label']
                asm.append(translate_brnch(cmnd, lbl))
            elif cmnd in self.func_cmnds:
                name = line[1].report_data()['name']
                n_vars = line[1].report_data()['n_vars']
                asm.append(translate_func(self, cmnd, name, n_vars))

        self.asm_code = asm
        return asm
