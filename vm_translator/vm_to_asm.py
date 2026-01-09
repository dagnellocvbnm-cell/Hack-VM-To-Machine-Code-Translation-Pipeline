import sys, os, glob

dictionaryB = {
    "label": lambda name: [
        f"({name})"
    ],

    "goto": lambda name: [
        f"@{name}",
        "0;JMP"
    ],

    "if-goto": lambda name: [
        "@SP",
        "AM=M-1",     # SP--, A = SP
        "D=M",        # D = stack[top]
        f"@{name}",
        "D;JNE"       # jump if D != 0
    ]
}

dictionaryPop = {
    "local": [
        "@i",
        "D=A",
        "@LCL",
        "D=D+M",
        "@R13",
        "M=D",
        "@SP",
        "M=M-1",
        "A=M",
        "D=M",
        "@R13",
        "A=M",
        "M=D"
    ],
    "argument": [
        "@i",
        "D=A",
        "@ARG",
        "D=D+M",
        "@R13",
        "M=D",
        "@SP",
        "M=M-1",
        "A=M",
        "D=M",
        "@R13",
        "A=M",
        "M=D"
    ],
    "this": [
        "@i",
        "D=A",
        "@THIS",
        "D=D+M",
        "@R13",
        "M=D",
        "@SP",
        "M=M-1",
        "A=M",
        "D=M",
        "@R13",
        "A=M",
        "M=D"
    ],
    "that": [
        "@i",
        "D=A",
        "@THAT",
        "D=D+M",
        "@R13",
        "M=D",
        "@SP",
        "M=M-1",
        "A=M",
        "D=M",
        "@R13",
        "A=M",
        "M=D"
    ],
    "temp": [
        "@i",
        "D=A",
        "@5",
        "D=D+A",
        "@R13",
        "M=D",
        "@SP",
        "M=M-1",
        "A=M",
        "D=M",
        "@R13",
        "A=M",
        "M=D"
    ],
    "pointer_0": [
        "@SP",
        "M=M-1",
        "A=M",
        "D=M",
        "@THIS",
        "M=D"
    ],
    "pointer_1": [
        "@SP",
        "M=M-1",
        "A=M",
        "D=M",
        "@THAT",
        "M=D"
    ],
    "static": [
        "@SP",
        "M=M-1",
        "A=M",
        "D=M",
        "@FileName.i",
        "M=D"
    ]
}

dictionaryPush = {

    "constant": [
        "@i",
        "D=A",
        "@SP",
        "A=M",
        "M=D",
        "@SP",
        "M=M+1"
    ],
    "local": [
        "@i",
        "D=A",
        "@LCL",
        "A=D+M",
        "D=M",
        "@SP",
        "A=M",
        "M=D",
        "@SP",
        "M=M+1"
    ],
    "argument": [
        "@i",
        "D=A",
        "@ARG",
        "A=D+M",
        "D=M",
        "@SP",
        "A=M",
        "M=D",
        "@SP",
        "M=M+1"
    ],
    "this": [
        "@i",
        "D=A",
        "@THIS",
        "A=D+M",
        "D=M",
        "@SP",
        "A=M",
        "M=D",
        "@SP",
        "M=M+1"
    ],
    "that": [
        "@i",
        "D=A",
        "@THAT",
        "A=D+M",
        "D=M",
        "@SP",
        "A=M",
        "M=D",
        "@SP",
        "M=M+1"
    ],
    "temp": [
        "@i",
        "D=A",
        "@5",
        "A=D+A",
        "D=M",
        "@SP",
        "A=M",
        "M=D",
        "@SP",
        "M=M+1"
    ],
    "pointer_0": [
        "@THIS",
        "D=M",
        "@SP",
        "A=M",
        "M=D",
        "@SP",
        "M=M+1"
    ],
    "pointer_1": [
        "@THAT",
        "D=M",
        "@SP",
        "A=M",
        "M=D",
        "@SP",
        "M=M+1"
    ],
    "static": [
        "@FileName.i",
        "D=M",
        "@SP",
        "A=M",
        "M=D",
        "@SP",
        "M=M+1"
    ],
}

dictionaryA = {

    "add": [
        "@SP", "AM=M-1", "D=M",
        "A=A-1", "M=D+M"
    ],
    "sub": [
        "@SP", "AM=M-1", "D=M",
        "A=A-1", "M=M-D"
    ],
    "and": [
        "@SP", "AM=M-1", "D=M",
        "A=A-1", "M=D&M"
    ],
    "or": [
        "@SP", "AM=M-1", "D=M",
        "A=A-1", "M=D|M"
    ],

    "neg": [
        "@SP", "A=M-1", "M=-M"
    ],
    "not": [
        "@SP", "A=M-1", "M=!M"
    ],

    "eq" : [
        "@SP",
        "M=M-1",
        "A=M",
        "D=M",
        "@SP",
        "M=M-1",
        "A=M",
        "D=M-D",
        "@EQ_TRUEvalue",
        "D;JEQ",
        "@SP",
        "A=M",
        "M=0",
        "@EQ_ENDvalue",
        "0;JMP",
        "(EQ_TRUEvalue)",
        "@SP",
        "A=M",
        "M=-1",
        "(EQ_ENDvalue)",
        "@SP",
        "M=M+1"
        ],

    "gt": [
        "@SP",
        "M=M-1",
        "A=M",
        "D=M",
        "@SP",
        "M=M-1",
        "A=M",
        "D=M-D",
        "@GT_TRUEvalue",
        "D;JGT",
        "@SP",
        "A=M",
        "M=0",
        "@GT_ENDvalue",
        "0;JMP",
        "(GT_TRUEvalue)",
        "@SP",
        "A=M",
        "M=-1",
        "(GT_ENDvalue)",
        "@SP",
        "M=M+1"
    ],

    "lt" : [
        "@SP",
        "M=M-1",
        "A=M",
        "D=M",
        "@SP",
        "M=M-1",
        "A=M",
        "D=M-D",
        "@LT_TRUEvalue",
        "D;JLT",
        "@SP",
        "A=M",
        "M=0",
        "@LT_ENDvalue",
        "0;JMP",
        "(LT_TRUEvalue)",
        "@SP",
        "A=M",
        "M=-1",
        "(LT_ENDvalue)",
        "@SP",
        "M=M+1"
    ]

}

def function_translate(name, num_lcls):
    num_lcls = int(num_lcls)
    lines = [f"({name})"]
    for i in range(num_lcls):
        lines.extend([
            "@0",
            "D=A",
            "@SP",
            "A=M",
            "M=D",
            "@SP",
            "M=M+1"
        ])
    return lines

def call_translate(function_name, suffix, num_lcls, counter):
    num_lcls = int(num_lcls)
    ret_label = f"{suffix}.{function_name}${counter}"
    return [
        # push return-address
        f"@{ret_label}", "D=A",
        "@SP", "A=M", "M=D",
        "@SP", "M=M+1",

        # push LCL
        "@LCL", "D=M",
        "@SP", "A=M", "M=D",
        "@SP", "M=M+1",

        # push ARG
        "@ARG", "D=M",
        "@SP", "A=M", "M=D",
        "@SP", "M=M+1",

        # push THIS
        "@THIS", "D=M",
        "@SP", "A=M", "M=D",
        "@SP", "M=M+1",

        # push THAT
        "@THAT", "D=M",
        "@SP", "A=M", "M=D",
        "@SP", "M=M+1",

        # ARG = SP - 5 - n_args
        "@SP", "D=M",
        "@5", "D=D-A",
        f"@{num_lcls}", "D=D-A",
        "@ARG", "M=D",

        # LCL = SP
        "@SP", "D=M",
        "@LCL", "M=D",

        # goto function
        f"@{function_name}", "0;JMP",

        # return-address label
        f"({ret_label})"
    ]

def return_translate():
    return [
        # FRAME = LCL
        "@LCL", "D=M",
        "@R13", "M=D",

        # RET = *(FRAME - 5)
        "@5", "A=D-A", "D=M",
        "@R14", "M=D",

        # *ARG = pop()
        "@SP", "AM=M-1", "D=M",
        "@ARG", "A=M", "M=D",

        # SP = ARG + 1
        "@ARG", "D=M+1",
        "@SP", "M=D",

        # THAT = *(FRAME - 1)
        "@R13", "AM=M-1", "D=M",
        "@THAT", "M=D",

        # THIS = *(FRAME - 2)
        "@R13", "AM=M-1", "D=M",
        "@THIS", "M=D",

        # ARG = *(FRAME - 3)
        "@R13", "AM=M-1", "D=M",
        "@ARG", "M=D",

        # LCL = *(FRAME - 4)
        "@R13", "AM=M-1", "D=M",
        "@LCL", "M=D",

        # goto RET
        "@R14", "A=M", "0;JMP"
    ]

def parser(file_name):

    lines= []

    with open(file_name, "r") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("//"):
                continue
            if "//" in line:
                line = line.split("//")[0].strip()
            if line:
                lines.append(line)

    parsed_lines = []
    operator_list = []

    for i in range(0, len(lines)):

        if lines[i] == "return":
            parsed_lines.append(lines[i])
            operator_list.append(2)
        else:
            parts = lines[i].split()
            if len(parts) == 1:
                parsed_lines.append(parts[0])
                operator_list.append(1)
            else:
                parsed_lines.append(parts)
                operator_list.append(0)

    # print(parsed_lines)
    # print(operator_list)

    print("PARSED", repr(parsed_lines))

    return parsed_lines, operator_list

def translate(parsed_lines, operator_list, suffix):

    asm_list = []
    counter1 = 0
    counter2 = 0

    for i in range(0, len(operator_list)):

        # return
        if operator_list[i] == 2:
            value = return_translate()

        # dictionaryA

        elif operator_list[i] == 1:
            value = dictionaryA[parsed_lines[i]].copy()
            if parsed_lines[i] in ("eq", "lt", "gt"):
                value = [line.replace("value", str(counter1)) for line in value]
                counter1 += 1

        # dictionaryPush

        elif parsed_lines[i][0] == 'push':
            if parsed_lines[i][1] in ("constant", "local", "this", "that", "argument","temp"):
                value = dictionaryPush[parsed_lines[i][1]].copy()
                value[0] = '@' + parsed_lines[i][2]
            elif parsed_lines[i][1] == "static":
                value = dictionaryPush[parsed_lines[i][1]].copy()
                value[0] = '@' + suffix + '.' + parsed_lines[i][2]
            elif parsed_lines[i][2] == '0':
                value = dictionaryPush['pointer_0'].copy()
            else:
                value = dictionaryPush['pointer_1'].copy()

        # dictionaryPop

        elif parsed_lines[i][0] == 'pop':
            if parsed_lines[i][1] in ("local", "this", "that", "argument","temp"):
                value = dictionaryPop[parsed_lines[i][1]].copy()
                value[0] = '@' + parsed_lines[i][2]
            elif parsed_lines[i][1] == "static":
                value = dictionaryPop[parsed_lines[i][1]].copy()
                value[4] = '@' + suffix + '.' + parsed_lines[i][2]
            elif parsed_lines[i][2] == '0':
                value = dictionaryPop['pointer_0'].copy()
            else:
                value = dictionaryPop['pointer_1'].copy()

        # dictionaryB

        elif parsed_lines[i][0] in ('goto', 'if-goto', 'label'):
            value = dictionaryB[parsed_lines[i][0]](parsed_lines[i][1])

        # function

        elif parsed_lines[i][0] == 'function':
            value = function_translate(parsed_lines[i][1], parsed_lines[i][2])

        # call
        elif parsed_lines[i][0] == 'call':
            value = call_translate(parsed_lines[i][1], suffix, parsed_lines[i][2], counter2)
            counter2 += 1

        #append value to asm list
        for line in value:
            asm_list.append(line)


    print(asm_list)

    return asm_list

def write(asm_list, file_name):
    with open(file_name, "w") as f:
        for i in range (0, len(asm_list)):
            if i == len(asm_list) - 1:
                f.write(asm_list[i])
            else:
                f.write(asm_list[i] + "\n")

def get_asm_list(vm_file):
    file_name = os.path.basename(vm_file)
    suffix = file_name.split(".")[0]
    parsed_lines, operator_list = parser(vm_file)
    asm_list = translate(parsed_lines, operator_list, suffix)
    return asm_list

def bootstrap():
    SP_eq_256 = ['@256',
                'D=A',
                '@SP',
                 'M=D']
    call_SysInit = call_translate("Sys.init", "Bootstrap",0,0)
    SP_eq_256.extend(call_SysInit)
    return SP_eq_256

def get_vm_files(path):
    return glob.glob(os.path.join(path, "*.vm"))

def dir_contains_dirVM(dir_path):
    dir = os.path.basename(os.path.normpath(dir_path))
    vm = os.path.join(dir_path, dir + ".vm")

    return os.path.isfile(vm)

def test():
    asm_list = get_asm_list(r"C:\Users\dagne\PyCharmProject1\NAND2TETRIS\NAND2TETRIS_Part2\Project7\FibonacciElement\Main.vm")
    write(asm_list, "test")

def main():
    vm_path = sys.argv[1]

    if os.path.isdir(vm_path):
        asm_file = os.path.join(vm_path, os.path.basename(vm_path) + ".asm")
        if not dir_contains_dirVM(vm_path):
            asm_list = bootstrap()
            vm_list = get_vm_files(vm_path)
            for vm in vm_list:
                translated_asm = get_asm_list(vm)
                asm_list.extend(translated_asm)
        else:
            vm_file = os.path.join(vm_path, os.path.basename(vm_path) + ".vm")
            asm_list = get_asm_list(vm_file)


    else:
        asm_file = os.path.splitext(vm_path)[0] + ".asm"
        vm_file = os.path.splitext(vm_path)[0] + ".vm"
        asm_list = get_asm_list(vm_file)

    write(asm_list, asm_file)


if __name__ == "__main__":
    main()
#test()


