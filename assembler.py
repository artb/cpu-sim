import fileinput
import collections

line_number = 0
instructions = [] 
labels = {}
opcodes = {
    "ADD": "0000",
    "INP": "0100",
    "PRINT": "0101",
    "STOP": "0110",
    "LW": "1100",
    "SW": "1101",
    "BZ":"1001",
    ".word": ""
}
registers = {
    "$t0": "0",
    "$t1": "1"
}

post_address_set = collections.defaultdict(list)

getBin = lambda x: x >= 0 and str(bin(x))[2:] or "-" + str(bin(x))[3:]  # Converte decimal (inteiro) para binario string


for line in fileinput.input():
    bfer = line.strip()
    # first check if the line has a label
    lblarg = bfer.split(":")
    if ( len(lblarg) == 2):
        labels[lblarg[0]] = line_number
        if lblarg[0] in post_address_set.keys():
            address = getBin(labels[lblarg[0]])
            add_zeros = 8 - len(address)
            address = "0"*add_zeros + address
            for ins in post_address_set[lblarg[0]]:
                instructions[ins] = address 
        bfer = lblarg[1].strip()
    # now we only want to look at the instruction
    # instruction is a opcode followed by a space and its arguments
    opcodeandarg = bfer.split(" ")
    opc = opcodeandarg[0].upper()
    try:
        args = opcodeandarg[1].split(",")
        args = map(lambda x:x.strip(), args)
    except:
        args = []

    if opc == "STOP":
        instructions.append(opcodes[opc] + "0000")
    elif opc == "ADD":
        tmp = opcodes[opc]
        tmp += reduce(lambda x,y: x+y, map(lambda x: registers[x], args))
        tmp += "00"
        instructions.append(tmp)
    elif opc == "INP" or  opc == "PRINT":
        instructions.append(opcodes[opc]+ registers[args[0]] + "000")
    elif opc == "LW" or opc == "SW":
        instructions.append( opcodes[opc] + registers[args[0]] + "000")
        line_number = line_number + 1
        try:
            address = getBin(labels[args[1]])
            add_zeros = 8 - len(address)
            address = "0"*add_zeros + address
        except:
            address = "not set yet"
            post_address_set[args[1]].append(line_number )
        instructions.append(address)
    elif opc == "BZ":
        instructions.append(opcodes[opc] + \
                reduce(lambda x,y: x+y, map(lambda x: registers[x], args[:-1]))+\
                 "00")
        line_number = line_number + 1
        try:
            address = getBin(labels[args[2]])
            add_zeros = 8 - len(address)
            address = "0"*add_zeros + address
        except:
            address = "not set yet"
            post_address_set[args[2]].append(line_number)
        instructions.append(address)
    elif opc == ".WORD":
        immediate = getBin(int(args[0]))
        add_zeros = 8 - len(immediate)
        immediate = "0"*add_zeros + immediate
 
        instructions.append(immediate)
    elif opc == ".DATA":
        line_number -= 1
    line_number = line_number + 1

count = 0

print "v2.0 raw"
for ins in instructions:
    ins = str(hex(int(ins, 2))).replace("0x","")
    print ins,
    count +=1
    if count == 4:
        count = 0
        print '\n',


