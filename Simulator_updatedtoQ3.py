import sys
def Registers_code(code):
    if code == "000":
        return "R0"
    elif code == "001":
        return "R1"
    elif code == "010":
        return "R2"
    elif code == "011":
        return "R3"
    elif code == "100":
        return "R4"
    elif code == "101":
        return "R5"
    elif code == "110":
        return "R6"
    else:
        return "FLAGS"

def BinarytoDecimal(binary_code):
    index=0
    for digit in binary_code:
        if digit!="0":
            break
        else:
            index+=1
    if binary_code[index:]=="":
        return 0
    else:
        binary_code=(int)(binary_code[index:])
    decimal = 0
    power = 0

    while binary_code != 0:
        digit = binary_code % 10
        decimal += digit * (2 ** power)
        binary_code //= 10
        power += 1

    return decimal

def DecimaltoBinary(decimal_value, length):
    if type(decimal_value) == str:
        decimal_value = int(decimal_value)
    if decimal_value == 0:
        return '0' * length
    binary_num = ''
    while decimal_value > 0:
        binary_num = str(decimal_value % 2) + binary_num
        decimal_value //= 2
    bits = len(binary_num)
    binary_str_len_bit = ("0" * (length - bits)) + binary_num

    return binary_str_len_bit

#All three inputs are in string.
def Bit_operator(operation,num1,num2):
    result=""
    if operation=="XOR":
        for bit_a, bit_b in zip(num1, num2):
            # Perform XOR operation on each pair of bits
            result += str(int(bit_a) ^ int(bit_b))

        return result
    
    elif operation=="OR":
        for bit_a, bit_b in zip(num1, num2):
            # Perform OR operation on each pair of bits
            result += str(int(bit_a) | int(bit_b))

        return result
    
    elif operation=="AND":
        for bit_a, bit_b in zip(num1, num2):
            result += str(int(bit_a) & int(bit_b))

        return result

    elif operation=="NOT":
        # Perform the bitwise NOT operation
        result = ''.join('1' if bit == '0' else '0' for bit in num1)

        return result
    
    elif operation=="Right Shift":
        shift_amt=BinarytoDecimal(num2)
        result="0"*shift_amt+num1[:-(shift_amt)]

        return result

    elif operation=="Left Shift":
        shift_amt=BinarytoDecimal(num2)
        result=num1[shift_amt:]+"0"*shift_amt

        return result

def BinaryGen(num,decimal_flag):    
    decimal_flag="y"
    if decimal_flag=="n":
        if type(num)==str:
            num=int(num)
        if num == 0:
            return '0000000'
        binary_num = ''
        while num > 0:
            binary_num = str(num % 2) + binary_num
            num //= 2
        #To return 7 bits binary number
        bits=len(str(binary_num))
        binary_str_7bit=("0"*(7-bits))+str(binary_num)
    else:
        num=float(num)
        exponent=0
        mantissa = ""

        while(num>2.0 or num<1.0):
            exponent+=1
            num+=1
            num=num/2

        num=num-1
        if num>=0.5:
            num-=0.5
            mantissa+="1"
        else:
            mantissa+="0"

        if num>=0.25:
            num-=0.25
            mantissa+="1"
        else:
            mantissa+="0"

        if num>=0.125:
            num-=0.125
            mantissa+="1"
        else:
            mantissa+="0"

        if num>=0.0625:
            num-=0.0625
            mantissa+="1"
        else:
            mantissa+="0"

        if num>=0.03125:
            num-=0.03125
            mantissa+="1"
        else:
            mantissa+="0"
        binary_str_7bit=BinaryGen(exponent+3,"n")[-3:]+mantissa
    
    return binary_str_7bit

def instruct_exe(list_input,PC,dict_register,dict_var,line_num,Flag_jump):
    count=-1
    list_input2=list_input[line_num:]
    for list_line in list_input2:
        #Program Counter Update:
        if Flag_jump==True:
            count=list_input.index(list_line)
            PC=DecimaltoBinary(list_input.index(list_line),7)
            Flag_jump=False
        else:
            count+=1
            PC=DecimaltoBinary(count,7)
        opcode=list_line[:5]

        #Type A Instructions:
        if opcode=="00000" or opcode=="00001" or opcode=="00110" or opcode=="01010" or opcode=="01011" or opcode=="01100":
            reg1=Registers_code(list_line[7:10])
            reg2=Registers_code(list_line[10:13])
            reg3=Registers_code(list_line[13:])
            if opcode=="00000":
                #Addition
                new_val=BinarytoDecimal(dict_register[reg2])+BinarytoDecimal(dict_register[reg3])
                if new_val>65535:
                    dict_register[reg1]=DecimaltoBinary(0,16)
                    dict_register["FLAGS"]=dict_register["FLAGS"][0:12]+"1"+dict_register["FLAGS"][13:]
                else:
                    dict_register[reg1]=DecimaltoBinary(new_val,16)
            elif opcode=="00001":
                #Subtraction
                new_val=BinarytoDecimal(dict_register[reg2])-BinarytoDecimal(dict_register[reg3])
                if new_val<0:
                    dict_register[reg1]=DecimaltoBinary(0,16)
                    dict_register["FLAGS"]=dict_register["FLAGS"][0:12]+"1"+dict_register["FLAGS"][13:]
                else:
                    dict_register[reg1]=DecimaltoBinary(new_val,16)
            elif opcode=="00110":
                #Multiplication
                new_val=BinarytoDecimal(dict_register[reg2])*BinarytoDecimal(dict_register[reg3])
                if new_val>65535:
                    dict_register[reg1]=DecimaltoBinary(0,16)
                    dict_register["FLAGS"]=dict_register["FLAGS"][0:12]+"1"+dict_register["FLAGS"][13:]
                else:
                    dict_register[reg1]=DecimaltoBinary(new_val,16)
            elif opcode=="01010":
                #XOR
                new_val=Bit_operator("XOR",dict_register[reg2],dict_register[reg3])
                dict_register[reg1]=new_val
            elif opcode=="01011":
                #OR
                new_val=Bit_operator("OR",dict_register[reg2],dict_register[reg3])
                dict_register[reg1]=new_val
            elif opcode=="01100":
                #AND
                new_val=Bit_operator("AND",dict_register[reg2],dict_register[reg3])
                dict_register[reg1]=new_val
        
        #Type B Instructions:
        elif opcode=="00010" or opcode=="01000" or opcode=="01001":
            reg1=Registers_code(list_line[6:9])
            Imm=list_line[9:]
            if opcode=="00010":
                #Mov Immediate
                dict_register[reg1]="000000000"+Imm
            elif opcode=="01000":
                #Right Shift
                dict_register[reg1]=Bit_operator("Right Shift",dict_register[reg1],Imm)
            elif opcode=="01001":
                #Left Shift
                dict_register[reg1]=Bit_operator("Left Shift",dict_register[reg1],Imm)

        #Type C Instructions:
        elif opcode=="00011" or opcode=="00111" or opcode=="01101" or opcode=="01110":
            reg3=Registers_code(list_line[10:13])
            reg4=Registers_code(list_line[13:])
            if opcode=="00011":
                #mov Register
                dict_register[reg3]=dict_register[reg4]
                if reg4=="FLAGS":
                    dict_register["FLAGS"]="0000000000000000"
            elif opcode=="00111":
                #divide
                if dict_register[reg4]!="0000000000000000":
                    dict_register["R0"]=DecimaltoBinary(BinarytoDecimal(dict_register[reg3])//BinarytoDecimal(dict_register[reg4]),16)
                    dict_register["R1"]=DecimaltoBinary(BinarytoDecimal(dict_register[reg3])%BinarytoDecimal(dict_register[reg4]),16)
                else:
                    dict_register["R0"]=DecimaltoBinary(0,16)
                    dict_register["R0"]=DecimaltoBinary(0,16)
                    dict_register["FLAGS"]=dict_register["FLAGS"][0:12]+"1"+dict_register["FLAGS"][13:]
            elif opcode=="01101":
                #Invert
                dict_register[reg3]= Bit_operator("NOT",dict_register[reg4],"")
            elif opcode=="01110":
                #Compare
                if BinarytoDecimal(dict_register[reg3])==BinarytoDecimal(dict_register[reg4]):
                    dict_register["FLAGS"]=dict_register["FLAGS"][0:15]+"1"
                elif BinarytoDecimal(dict_register[reg3])>BinarytoDecimal(dict_register[reg4]):
                    dict_register["FLAGS"]=dict_register["FLAGS"][0:14]+"1"+dict_register["FLAGS"][-1]
                elif BinarytoDecimal(dict_register[reg3])<BinarytoDecimal(dict_register[reg4]):
                    dict_register["FLAGS"]=dict_register["FLAGS"][0:13]+"1"+dict_register["FLAGS"][-2:]

        #Type D Instructions:
        elif opcode=="00100" or opcode=="00101":
            reg1=Registers_code(list_line[6:9])
            mem=list_line[9:]
            if mem not in dict_var.keys():
                dict_var.update({mem:"0000000000000000"})
            if opcode=="00100":
                #Load
                dict_register[reg1]=dict_var[mem]
            elif opcode=="00101":
                #Store
                dict_var[mem]=dict_register[reg1]

        #Type E Instructions:
        elif opcode=="01111" or opcode=="11100" or opcode=="11101" or opcode=="11111":
            mem=BinarytoDecimal(list_line[9:])
            if opcode=="01111":
                #Reset of FLAGS Register
                dict_register["FLAGS"]="0000000000000000"
                #Unconditional Jump
                print(PC+"        "+dict_register["R0"]+" "+dict_register["R1"]+" "+dict_register["R2"]+" "+dict_register["R3"]+" "+dict_register["R4"]+" "+dict_register["R5"]+" "+dict_register["R6"]+" "+dict_register["FLAGS"])
                Flag_jump=True
                instruct_exe(list_input,PC,dict_register,dict_var,mem,Flag_jump)
                return
            elif opcode=="11100":
                #Jump if less than
                if dict_register["FLAGS"][13]=="1":
                    #dict_register["FLAGS"]=dict_register["FLAGS"][0:13]+"0"+dict_register["FLAGS"][-2:]
                    dict_register["FLAGS"]="0000000000000000"
                    print(PC+"        "+dict_register["R0"]+" "+dict_register["R1"]+" "+dict_register["R2"]+" "+dict_register["R3"]+" "+dict_register["R4"]+" "+dict_register["R5"]+" "+dict_register["R6"]+" "+dict_register["FLAGS"])
                    Flag_jump=True
                    instruct_exe(list_input,PC,dict_register,dict_var,mem,Flag_jump)
                    return
                else:
                    dict_register["FLAGS"]="0000000000000000"
            elif opcode=="11101":
                #Jump if greater than
                if dict_register["FLAGS"][14]=="1":
                    #dict_register["FLAGS"]=dict_register["FLAGS"][0:14]+"0"+dict_register["FLAGS"][-1]
                    dict_register["FLAGS"]="0000000000000000"
                    print(PC+"        "+dict_register["R0"]+" "+dict_register["R1"]+" "+dict_register["R2"]+" "+dict_register["R3"]+" "+dict_register["R4"]+" "+dict_register["R5"]+" "+dict_register["R6"]+" "+dict_register["FLAGS"])
                    Flag_jump=True
                    instruct_exe(list_input,PC,dict_register,dict_var,mem,Flag_jump)
                    return
                else:
                    dict_register["FLAGS"]="0000000000000000"
            elif opcode=="11111":
                #Jump if equal
                if dict_register["FLAGS"][15]=="1":
                    #dict_register["FLAGS"]=dict_register["FLAGS"][0:15]+"0"
                    dict_register["FLAGS"]="0000000000000000"
                    print(PC+"        "+dict_register["R0"]+" "+dict_register["R1"]+" "+dict_register["R2"]+" "+dict_register["R3"]+" "+dict_register["R4"]+" "+dict_register["R5"]+" "+dict_register["R6"]+" "+dict_register["FLAGS"])
                    Flag_jump=True
                    instruct_exe(list_input,PC,dict_register,dict_var,mem,Flag_jump)
                    return
                else:
                    dict_register["FLAGS"]="0000000000000000"
                
        #Type F Instructions:
        elif opcode=="11010":
            #Halt
            print(PC+"        "+dict_register["R0"]+" "+dict_register["R1"]+" "+dict_register["R2"]+" "+dict_register["R3"]+" "+dict_register["R4"]+" "+dict_register["R5"]+" "+dict_register["R6"]+" "+dict_register["FLAGS"])
            return
        
        print(PC+"        "+dict_register["R0"]+" "+dict_register["R1"]+" "+dict_register["R2"]+" "+dict_register["R3"]+" "+dict_register["R4"]+" "+dict_register["R5"]+" "+dict_register["R6"]+" "+dict_register["FLAGS"])

#Taking Input:
list_input=[]
file1 = open("Simulator_input.txt", "r")
for i in file1:
    list_input.append(i.strip())
file1.close()

""" for i in sys.stdin:
    list_input.append(i.strip()) """

#Initializing all registers and program counter
dict_register={"R0":"0000000000000000","R1":"0000000000000000","R2":"0000000000000000","R3":"0000000000000000","R4":"0000000000000000","R5":"0000000000000000","R6":"0000000000000000","FLAGS":"0000000000000000"}
dict_var={}
PC="0000000" #7 zeros
Flag_jump=False
instruct_exe(list_input,PC,dict_register,dict_var,0,Flag_jump)

#Printing DumpMemory
count2=0
for list_line in list_input:
    count2+=1
    print(list_line)

for i in range(128-count2):
    print("0000000000000000")