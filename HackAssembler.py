import re

comp_table = {
    # a = 0
    "0":   "0101010",
    "1":   "0111111",
    "-1":  "0111010",
    "D":   "0001100",
    "A":   "0110000",
    "!D":  "0001101",
    "!A":  "0110001",
    "-D":  "0001111",
    "-A":  "0110011",
    "D+1": "0011111",
    "A+1": "0110111",
    "D-1": "0001110",
    "A-1": "0110010",
    "D+A": "0000010",
    "D-A": "0010011",
    "A-D": "0000111",
    "D&A": "0000000",
    "D|A": "0010101",

    # a = 1
    "M":   "1110000",
    "!M":  "1110001",
    "-M":  "1110011",
    "M+1": "1110111",
    "M-1": "1110010",
    "D+M": "1000010",
    "D-M": "1010011",
    "M-D": "1000111",
    "D&M": "1000000",
    "D|M": "1010101" }

predefined_symbols = {
    # registers
    **{f"R{i}": i for i in range(16)},  # R0..R15 -> 0..15
    # pointer / segments
    "SP": 0,
    "LCL": 1,
    "ARG": 2,
    "THIS": 3,
    "THAT": 4,
    # I/O
    "SCREEN": 16384,
    "KBD": 24576
}






def jump(str):
    if(str == '0'):
        return '000'
    if (str == 'JGT'):
        return '001'
    if (str == 'JEQ'):
        return '010'
    if (str == 'JGE'):
        return '011'
    if (str == 'JLT'):
        return '100'
    if (str == 'JNE'):
        return '101'
    if (str == 'JLE'):
        return '110'
    if (str == 'JMP'):
        return '111'

def dest(str):
    if (str == '0'):
        return '000'
    if (str == 'M'):
        return '001'
    if (str == 'D'):
        return '010'
    if (str == 'MD'):
        return '011'
    if (str == 'A'):
        return '100'
    if (str == 'AM'):
        return '101'
    if (str == 'AD'):
        return '110'
    if (str == 'AMD'):
        return '111'

def parser(file_name):
    asmLines = []

    with open(file_name, "r") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("//"):
                continue
            asmLines.append(line)

    print(asmLines)

    commandLines = []
    newAsmLines = []
    pc = 0
    symbols = {}
    symbols = predefined_symbols
    for line in asmLines:
        if line.startswith('@'):
            commandLines.append("a")
            newAsmLines.append(line)
            pc += 1
        elif line.startswith('('):
            key = line[1:-1]
            value = pc
            symbols[key] = value
        else:
            commandLines.append("c")
            newAsmLines.append(line)
            pc += 1

    print(commandLines)
    print(newAsmLines)

    parsedList = []


    for i in range (0, len(commandLines)):
        if commandLines[i] == "a":
            a = newAsmLines[i].replace("@", "")
            parsedList.append(a)
        if commandLines[i] == "c":
            c = re.split("[=;]", newAsmLines[i])
            if ';' not in newAsmLines[i]:
                c += ["0"] * (3 - len(c))
            if '=' not in newAsmLines[i]:
                c.insert(0, "0")
            parsedList.append(c)

    print(parsedList)
    print(symbols)

    return parsedList, symbols

def code(parsed_list, symbols):
    binary_list = []
    variable_counter = 16
    for element in parsed_list:
        if type(element) == str:
            try:
                int(element)
                integer = True
            except ValueError:
                integer = False
            if integer == False:
                if element in symbols:
                    str_num = symbols[element]
                else:
                    str_num = str(variable_counter)
                    symbols[element] = str_num
                    variable_counter += 1
            else:
                str_num = element
            num = int(str_num)
            bin_num = format(num & 0xFFFF, '016b')
            binary_list.append(bin_num)

        if type(element) == list:
            c = comp_table[element[1]]
            d = dest(element[0])
            j = jump(element[2])
            c_num = "111" + c + d + j
            binary_list.append(c_num)

    print(binary_list)
    return binary_list



def main():
    parsedList, symbols = parser('Pong.asm')
    binary_list = code(parsedList, symbols)

    with open("Pong.hack", "w") as f:
        for i in range (0, len(binary_list)):
            if i == len(binary_list) - 1:
                f.write(binary_list[i])
            else:
                f.write(binary_list[i] + "\n")



main()
























