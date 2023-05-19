import sys
#Defining all other various error that can be encountered:
def Def_Error(code_org):
    Flag=[]

    #Making List Label which contains all labels name:
    list_label=[]
    list_label_num=[]
    for list_line in code_org:
        if list_line!=[]:
            if list_line[0]=="jmp" or list_line[0]=="jlt" or list_line[0]=="jgt" or list_line[0]=="je":
                list_label.append(list_line[1]+":")
                list_label_num.append((list_line[1]+":",code_org.index(list_line)+1))
            elif list_line[0]=="add" or list_line[0]=="sub" or list_line[0]=="mul" or list_line[0]=="xor" or list_line[0]=="or" or list_line[0]=="and" or list_line[0]=="mov" or list_line[0]=="rs" or list_line[0]=="ls" or list_line[0]=="mov" or list_line[0]=="div" or list_line[0]=="not" or list_line[0]=="cmp" or list_line[0]=="ld" or list_line[0]=="st" or list_line[0]=="jmp" or list_line[0]=="jlt" or list_line[0]=="jgt" or list_line[0]=="je" or list_line[0]=="hlt" or list_line[0]=="var":
                pass
            elif list_line[0] not in list_label and len(list_line)>1:
                if list_line[1]=="jmp" or list_line[1]=="jlt" or list_line[1]=="jgt" or list_line[1]=="je":
                    list_label.append(list_line[2]+":")
                    list_label_num.append((list_line[1]+":",code_org.index(list_line)+1))
    
    #Label should have a instruction next to it:
    for label_name in list_label:
        for list_line in code_org:
            if list_line!=[]:
                if list_line[0]==label_name:
                    if len(list_line)>1:
                        if list_line[1]=="add" or list_line[1]=="sub" or list_line[1]=="mul" or list_line[1]=="xor" or list_line[1]=="or" or list_line[1]=="and" or list_line[1]=="mov" or list_line[1]=="rs" or list_line[1]=="ls" or list_line[1]=="mov" or list_line[1]=="div" or list_line[1]=="not" or list_line[1]=="cmp" or list_line[1]=="ld" or list_line[1]=="st" or list_line[1]=="jmp" or list_line[1]=="jlt" or list_line[1]=="jgt" or list_line[1]=="je" or list_line[1]=="hlt" or list_line[1]=="var":
                            continue
                        else:
                            line_num=code_org.index(list_line)+1
                            Flag.append(["No instruction after label at",line_num])
                    else:
                        line_num=code_org.index(list_line)+1
                        Flag.append(["No instruction after label at",line_num])

    #Illegal Use of FLAGS register:
    for list_line in code_org:
        if "FLAGS" in list_line:
            if len(list_line)>2:
                if (list_line[0]=="mov" and list_line[2][0]!="$") or (list_line[1]=="mov"and list_line[3][0]!="$"):
                    continue
                else:
                    for j in list_line:
                        if j=="FLAGS":
                            line_num=code_org.index(list_line)+1
                            Flag.append(["Illegal use of FLAGS register at",line_num])
            else:
                line_num=code_org.index(list_line)+1
                Flag.append(["Illegal use of FLAGS register at",line_num])

    #No spaces between the label and the colon (":"):
    for list_line in code_org:
        if list_line!=[]:
            if list_line[0]=="add" or list_line[0]=="sub" or list_line[0]=="mul" or list_line[0]=="xor" or list_line[0]=="or" or list_line[0]=="and" or list_line[0]=="mov" or list_line[0]=="rs" or list_line[0]=="ls" or list_line[0]=="mov" or list_line[0]=="div" or list_line[0]=="not" or list_line[0]=="cmp" or list_line[0]=="ld" or list_line[0]=="st" or list_line[0]=="jmp" or list_line[0]=="jlt" or list_line[0]=="jgt" or list_line[0]=="je" or list_line[0]=="hlt" or list_line[0]=="var":
                continue
            else:
                if len(list_line)>1:
                    if list_line[1]==":":
                        line_num=code_org.index(list_line)+1
                        Flag.append(["Space between label and colon at",line_num])

    #Use of undefined variable and not defining all variables in the starting:
    var_flag=0
    list_var=[]
    for list_line in code_org:
        if list_line!=[]:
            if list_line[0]=="var":
                list_var.append(list_line[1])
                if var_flag==1:
                    line_num=code_org.index(list_line)+1
                    Flag.append(["Not defining all variables in the starting at",line_num])
            else:
                var_flag=1

    for list_line in code_org:
        var_flag2=0
        if list_line!=[] and list_line!=["hlt"]:
            if list_line[0]=="ld" or list_line[0]=="st":
                for i in list_var:
                    if list_line[2]==i:
                        var_flag2=1
            if list_line[0]=="ld" or list_line[0]=="st":
                if var_flag2==0:
                    line_num=code_org.index(list_line)+1
                    Flag.append(["Use of undefined variables at",line_num])
            if len(list_line)>1:
                if list_line[1]=="ld" or list_line[1]=="st":
                    for i in list_var:
                        if list_line[3]==i:
                            var_flag2=1
                if list_line[1]=="ld" or list_line[1]=="st":
                    if var_flag2==0:
                        line_num=code_org.index(list_line)+1
                        Flag.append(["Use of undefined variables at",line_num])

    #Typos in instructions name and registers names:
    list_inst=["add","sub","mul","xor","or","and","mov","rs","ld","ls","div","not","cmp","Id","st","jmp","jlt","jgt","je","hlt","var"]
    list_regist=["R0","R1","R2","R3","R4","R5","R6"]+list_var
    for list_line in code_org:
        Flag_inst=0
        if list_line!=[]:
            for i in list_inst:
                if list_line[0]==i:
                    count_reg=0
                    Flag_inst=1
                    if i =="add" or i=="sub" or i=="mul" or i=="xor" or i=="or" or i=="and":
                        count_reg=0
                        if len(list_line)==4:
                            for reg in list_regist:
                                if reg==list_line[1]:
                                    count_reg+=1
                                if reg==list_line[2]:
                                    count_reg+=1
                                if reg==list_line[3]:
                                    count_reg+=1
                        if count_reg<3:
                            line_num=code_org.index(list_line)+1
                            Flag.append(["Typos error in register at",line_num])
                            break
                    pass_status=""
                    if i=="mov" or i=="div" or i=="not" or i=="cmp":
                        count_reg=0
                        pass_status=""
                        if len(list_line)==3:
                            if (i=="mov" and list_line[2][0]=="$"):
                                pass_status="OK"
                            if pass_status!="OK":
                                for reg in list_regist:
                                    if reg==list_line[1]:
                                        count_reg+=1
                                    if reg==list_line[2]:
                                        count_reg+=1
                                    if (i=="mov" and (list_line[2]=="FLAGS")):
                                        count_reg+=1
                        if count_reg<2 and pass_status!="OK":
                            line_num=code_org.index(list_line)+1
                            Flag.append(["Typos error in register at",line_num])
                            break
                    status=""
                    if i=="mov" or i=="rs" or i=="ls" or i=="ld" or i=="st":
                        count_reg=0
                        status="Yes"
                        if len(list_line)==3:
                            if (i=="mov" and list_line[2][0]!="$"):
                                status="No pass"
                            if status!="No pass":
                                for reg in list_regist:
                                    if reg==list_line[1]:
                                        count_reg+=1
                            if count_reg<1 and status!="No pass":
                                line_num=code_org.index(list_line)+1
                                Flag.append(["Typos error in register at",line_num])
                                break
            if Flag_inst==0:
                if len(list_line)>1 and len(list_line[0])>1:
                    if (list_line[0] in list_label or list_line[0][-1]==":"):
                        for i in list_inst:
                            if list_line[1]==i:
                                Flag_inst=1
                                count_reg=0
                                if i =="add" or i=="sub" or i=="mul" or i=="xor" or i=="or" or i=="and":
                                    count_reg=0
                                    if len(list_line)==5:
                                        for reg in list_regist:
                                            if reg==list_line[2]:
                                                count_reg+=1
                                            if reg==list_line[3]:
                                                count_reg+=1
                                            if reg==list_line[4]:
                                                count_reg+=1
                                    if count_reg<3:
                                        line_num=code_org.index(list_line)+1
                                        Flag.append(["Typos error in register at",line_num])
                                        break
                                pass_status=""
                                if i=="mov" or i=="div" or i=="not" or i=="cmp":
                                    count_reg=0
                                    pass_status=""
                                    if len(list_line)==4:
                                        if (i=="mov" and list_line[3][0]=="$"):
                                            pass_status="OK"
                                        if pass_status!="OK":
                                            for reg in list_regist:
                                                if reg==list_line[2]:
                                                    count_reg+=1
                                                if reg==list_line[3]:
                                                    count+=1
                                                if (i=="mov" and (list_line[3]=="FLAGS")):
                                                    count_reg+=1
                                    if count_reg<2 and pass_status!="OK":
                                        line_num=code_org.index(list_line)+1
                                        Flag.append(["Typos error in register at",line_num])
                                        break
                                status=""
                                if i=="mov" or i=="rs" or i=="ls" or i=="ld" or i=="st":
                                    count_reg=0
                                    if len(list_line)==4:
                                        if (i=="mov" and list_line[3][0]!="$"):
                                            status="No pass"
                                        if status!="No pass":
                                            for reg in list_regist:
                                                if reg==list_line[2]:
                                                    count_reg+=1
                                    if count_reg<1 and status!="No pass":
                                        line_num=code_org.index(list_line)+1
                                        Flag.append(["Typos error in register at",line_num])
                                        break
                elif (len(list_label)>1):
                    line_num=code_org.index(list_line)+1
                    Flag.append(["Typos error in instruction at",line_num])
            if Flag_inst!=1:
                line_num=code_org.index(list_line)+1
                Flag.append(["Typos error in instruction at",line_num])
    #Use of undefined labels:
    list_label_call=[]
    for list_line in code_org:
        if list_line!=[]:
            if list_line[0]=="var" or list_line[0]=="add" or list_line[0]=="sub" or list_line[0]=="mul" or list_line[0]=="xor" or list_line[0]=="or" or list_line[0]=="and" or list_line[0]=="mov" or list_line[0]=="rs" or list_line[0]=="ls" or list_line[0]=="mov" or list_line[0]=="div" or list_line[0]=="not" or list_line[0]=="cmp" or list_line[0]=="ld" or list_line[0]=="st" or list_line[0]=="jmp" or list_line[0]=="jlt" or list_line[0]=="jgt" or list_line[0]=="je" or list_line[0]=="hlt":
                continue
            else:
                if len(list_line)>=1:
                    if list_line[0][-1]==":":
                        list_label_call.append(list_line[0])
                if len(list_line)>2:
                    if list_line[0][-1]==":" or list_line[1]==":":
                        list_label_call.append(list_line[0])
    for label,line_num in list_label_num:
        label_flag=0
        if label in list_label_call:
            label_flag=1
        if label_flag==0:
            Flag.append(["Use of undefined Labels at",line_num])

    #Illegal use of Immediate value [0,217]:
    for list_line in code_org:
        if list_line!=[] and list_line!=["hlt"]:
            if (list_line[0]=="rs" or list_line[0]=="ls" or list_line[0]=="mov"):
                if list_line[2][0]=="$":
                    num=int(list_line[2][1:])
                    if num>=218 or num<0:
                        line_num=code_org.index(list_line)+1
                        Flag.append(["Illegal use of immediate value at",line_num])
            if len(list_line)>1:
                if (list_line[1]=="rs" or list_line[1]=="ls" or list_line[1]=="mov"):
                    if list_line[3][0]=="$":
                        num=int(list_line[3][1:])
                        if num>=218 or num<0:
                            line_num=code_org.index(list_line)+1
                            Flag.append(["Illegal use of immediate value at",line_num])

    #Using one label at multiple times in a code:
    count=0
    for label_name in list_label:
        count=0
        for list_line in code_org:
            if list_line!=[]:
                if list_line[0]==label_name:
                    count+=1
                    if count>1:
                        line_num=code_org.index(list_line)+1
                        Flag.append(["Label used at multiple times at",line_num])
    
    #Misuse of label as variable or vice-versa:
    for list_line in code_org:
        flag1=0
        if list_line!=[]:
            if list_line[0]=="var" or list_line[0]=="add" or list_line[0]=="sub" or list_line[0]=="mul" or list_line[0]=="xor" or list_line[0]=="or" or list_line[0]=="and" or list_line[0]=="mov" or list_line[0]=="rs" or list_line[0]=="ls" or list_line[0]=="mov" or list_line[0]=="div" or list_line[0]=="not" or list_line[0]=="cmp" or list_line[0]=="ld" or list_line[0]=="st" or list_line[0]=="jmp" or list_line[0]=="jlt" or list_line[0]=="jgt" or list_line[0]=="je" or list_line[0]=="hlt":
                continue
            else:
                for j in list_var:
                    if list_line[0] == j+":":
                        flag1=1
                if flag1==1:
                    line_num=code_org.index(list_line)+1
                    Flag.append(["Misuse of variable as label at",line_num])

    for list_line in code_org:
        flag2=0
        if list_line!=[] and list_line!=["hlt"]:
            if list_line[0]=="ld" or list_line[0]=="st":
                for i in list_label:
                    if list_line[2]==i[:len(i)-1]:
                        flag2=1
                if flag2==1:
                    line_num=code_org.index(list_line)+1
                    Flag.append(["Misuse of label as variable at",line_num])
                    
            if len(list_line)>1:
                if list_line[1]=="ld" or list_line[1]=="st":
                    for i in list_label:
                        if list_line[3]==i[:len(i)-1]:
                            flag2=1
                if list_line[1]=="ld" or list_line[1]=="st":
                    if flag2==1:
                        line_num=code_org.index(list_line)+1
                        Flag.append(["Misuse of label as variable at",line_num])
    #Missing hlt instruction and hlt not being used as the last instruction:
    halt_flag=0
    count=0
    for list_line in code_org:
        for j in list_line:
            if halt_flag==1:
                if count==1:
                    break
                line_num=code_org.index(list_line)
                Flag.append(["hlt not being used as the last instruction at",line_num])
                count+=1
                break
            if j=="hlt":
                halt_flag+=1
    if halt_flag==0:
        line_num=code_org.index(list_line)+1
        Flag.append(["Missing hlt instructions after",line_num])
    
    return Flag


#Generate 7 bit binary code from the decimal number:          
def BinaryGen(num,decimal_flag):    
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
        integer_part = int(num)
        binary_code = ""

        # Convert integer part to binary
        while integer_part > 0:
            remainder = integer_part % 2
            binary_code = str(remainder) + binary_code
            integer_part = integer_part // 2

        # If there is a fractional part, convert it to binary
        if num != integer_part:
            binary_code += "."
            fractional_part = num - int(num)
            for i in range(4):  # 4 digits of precision
                fractional_part *= 2
                if fractional_part >= 1:
                    binary_code += "1"
                    fractional_part -= 1
                else:
                    binary_code += "0"

        list_num=binary_code.split(".")
        exponent=len(list_num[0])+2
        mantissa=(list_num[0][1:]+list_num[1]+"00000")[:5]
        binary_str_7bit=BinaryGen(exponent,"n")[-3:]+mantissa
    
    return binary_str_7bit

#Machine Code for all the 7 registers named R1,R2,R3...,R6,FLAGS
def register_binary(list_line,num,label):
    if label=="y":
        if list_line[num]=="R0":
            print("000",end="")
        elif list_line[num]=="R1":
            print("001",end="")
        elif list_line[num]=="R2":
            print("010",end="")
        elif list_line[num]=="R3":
            print("011",end="")
        elif list_line[num]=="R4":
            print("100",end="")
        elif list_line[num]=="R5":
            print("101",end="")
        elif list_line[num]=="R6":
            print("110",end="")
        elif list_line[num]=="FLAGS":
            print("111",end="")
    elif label=="n":
        if list_line[num]=="R0":
            print("000",end="")
        elif list_line[num]=="R1":
            print("001",end="")
        elif list_line[num]=="R2":
            print("010",end="")
        elif list_line[num]=="R3":
            print("011",end="")
        elif list_line[num]=="R4":
            print("100",end="")
        elif list_line[num]=="R5":
            print("101",end="")
        elif list_line[num]=="R6":
            print("110",end="")

#Finding the label machine code:
def label_code(list_org):
    list_label_add=[]
    count_line=0
    for list_line in list_org:
        count_line+=1
        if list_line!=[]:
            if list_line[0]=="var" or list_line[0]=="add" or list_line[0]=="sub" or list_line[0]=="mul" or list_line[0]=="xor" or list_line[0]=="or" or list_line[0]=="and" or list_line[0]=="mov" or list_line[0]=="rs" or list_line[0]=="ls" or list_line[0]=="mov" or list_line[0]=="div" or list_line[0]=="not" or list_line[0]=="cmp" or list_line[0]=="ld" or list_line[0]=="st" or list_line[0]=="jmp" or list_line[0]=="jlt" or list_line[0]=="jgt" or list_line[0]=="je" or list_line[0]=="hlt":
                if list_line[0]=="var":
                    count_line-=1
                continue
            else:
                if list_line[0][-1]==":" or list_line[1]==":":
                    list_label_add.append([list_line[0],BinaryGen(count_line-1,"n")])
    return list_label_add

#Creating suitable assembly code list
def create_assem_code(list_org,list_label_add):
    assembly_code=[]
    #Removing Variable declaring Brackets, Empty lines and label.
    for word_list in list_org:
        flag=0
        if word_list!=[]:
            if word_list[0]!="var":
                for label_name in list_label_add:
                    if word_list[0]==label_name[0]:
                        flag=1
                        word_list.remove(label_name[0])
                        assembly_code.append(word_list)
                        break
                if flag!=1:
                    assembly_code.append(word_list)
    return assembly_code

#Finding the variable machine code:
def var_code(list_org,count):
    count_var=0
    list_var_add=[]
    for word_list in list_org:
        if word_list!=[]:
            if word_list[0]=="var":
                count_var+=1
                list_var_add.append([word_list[1]])
    add=count-count_var

    for i in range(count_var):
        list_var_add[i].append(BinaryGen(add+i,"n"))

    return list_var_add

#To print the binary code:
def printing_machinecode(assembly_code,list_var_add,list_label_add):
    for list_line in assembly_code:
        #Type A Instructions:
        if list_line[0]=="add" or list_line[0]=="sub" or list_line[0]=="mul" or list_line[0]=="xor" or list_line[0]=="or" or list_line[0]=="and":
            
            if list_line[0]=="add":
                print("00000",end="")
                #unused bits in Type-A format:
                print("00",end="")
                for j in range(1,4):
                    register_binary(list_line,j,"n")

            elif list_line[0]=="sub":
                print("00001",end="")
                #unused bits in Type-A format:
                print("00",end="")
                for j in range(1,4):
                    register_binary(list_line,j,"n")
            
            elif list_line[0]=="mul":
                print("00110",end="")
                #unused bits in Type-A format:
                print("00",end="")
                for j in range(1,4):
                    register_binary(list_line,j,"n")
            
            elif list_line[0]=="xor":
                print("01010",end="")
                #unused bits in Type-A format:
                print("00",end="")
                for j in range(1,4):
                    register_binary(list_line,j,"n")

            elif list_line[0]=="and":
                print("01100",end="")
                #unused bits in Type-A format:
                print("00",end="")
                for j in range(1,4):
                    register_binary(list_line,j,"n")
            print("")
        
        #Type B Instructions:
        if list_line[0]=="mov" or list_line[0]=="rs" or list_line[0]=="ls":

            #Additional condition with "mov case" as mov instruction is same as in "Type C" Instructions.
            if list_line[0]=="mov" and list_line[2]!="R1"and list_line[2]!="R2" and list_line[2]!="R3" and list_line[2]!="R4" and list_line[2]!="R5" and list_line[2]!="R6" and list_line[2]!="FLAGS":
                print("00010",end="")
                dot_flag=0
                for char_dot in list_line[2]:
                    if char_dot==".":
                        dot_flag=1
                #Printing Unused bit
                if dot_flag==0:
                    print("0",end="")
                    register_binary(list_line,1,"n")
                    print(BinaryGen(list_line[2].replace("$",""),"n"))
                else:
                    register_binary(list_line,1,"n")
                    print(BinaryGen(list_line[2].replace("$",""),"y"))
                
            elif list_line[0]=="rs":
                print("01000",end="")
                dot_flag=0
                for char_dot in list_line[2]:
                    if char_dot==".":
                        dot_flag=1
                #Printing Unused bit
                if dot_flag==0:
                    print("0",end="")
                    register_binary(list_line,1,"n")
                    print(BinaryGen(list_line[2].replace("$",""),"n"))
                else:
                    register_binary(list_line,1,"n")
                    print(BinaryGen(list_line[2].replace("$",""),"y"))
            
            elif list_line[0]=="ls":
                dot_flag=0
                list_line[2].replace("$","")
                for char_dot in list_line[2]:
                    if char_dot==".":
                        dot_flag=1
                #Printing Unused bit
                if dot_flag==0:
                    print("0",end="")
                    register_binary(list_line,1,"n")
                    print(BinaryGen(list_line[2].replace("$",""),"n"))
                else:
                    register_binary(list_line,1,"n")
                    print(BinaryGen(list_line[2].replace("$",""),"y"))

        #Type C Instructions:
        if list_line[0]=="mov" or list_line[0]=="div" or list_line[0]=="not" or list_line[0]=="cmp":
            
            if list_line[0]=="mov" and (list_line[2]=="R1" or list_line[2]=="R2" or list_line[2]=="R3" or list_line[2]=="R4" or list_line[2]=="R5" or list_line[2]=="R6" or list_line[2]=="FLAGS"):
                print("00011",end="")
                #Printing Unused Bits
                print("00000",end="")
                #Printing for Registers
                for j in range(1,3):
                    register_binary(list_line,j,"y")
                print("")

            elif list_line[0]=="div":
                print("00111",end="")
                #Printing Unused Bits
                print("00000",end="")
                #Printing for register
                for j in range(1,3):
                    register_binary(list_line,j,"n")
                print("")

            elif list_line[0]=="not":
                print("01101",end="")
                #Printing Unused Bits
                print("00000",end="")
                #Printing for register
                for j in range(1,3):
                    register_binary(list_line,j,"n")
                print("")

            elif list_line[0]=="cmp":
                print("01110",end="")
                #Printing Uned Bits
                print("00000",end="")
                #Printing for register
                for j in range(1,3):
                    register_binary(list_line,j,"n")
                print("")

        #Type D Instructions:
        if list_line[0]=="ld" or list_line[0]=="st":
            if list_line[0]=="ld":
                print("00100",end="")
                #Printing Unused bits
                print("0",end="")
                register_binary(list_line,1,"n")
                for j in list_var_add:
                    if j[0]==list_line[2]:
                        print(j[1])

            elif list_line[0]=="st":
                print("00101",end="")
                #Printing Unused bits
                print("0",end="")
                register_binary(list_line,1,"n")
                for j in list_var_add:
                    if j[0]==list_line[2]:
                        print(j[1])
            
        #Type E instructions:
        if list_line[0]=="jmp" or list_line[0]=="jlt" or list_line[0]=="jgt" or list_line[0]=="je":
            if list_line[0]=="jmp":
                print("01111",end="")
                #Printing Unused Bit:
                print("0000",end="")
                for j in list_label_add:
                    if j[0]==list_line[1]+":":
                        print(j[1])

            elif list_line[0]=="jlt":
                print("11100",end="")
                #Printing Unused Bit:
                print("0000",end="")
                for j in list_label_add:
                    if j[0]==list_line[1]+":":
                        print(j[1])
            
            elif list_line[0]=="jgt":
                print("11101",end="")
                #Printing Unused Bit:
                print("0000",end="")
                for j in list_label_add:
                    if j[0]==list_line[1]+":":
                        print(j[1])
            
            elif list_line[0]=="je":
                print("11111",end="")
                #Printing Unused Bit:
                print("0000",end="")
                for j in (list_label_add):
                    if j[0]==list_line[1]+":":
                        print(j[1])

        #Type F instructions:
        if list_line[0]=="hlt":
            print("1101000000000000")
            return
#Taking Input and counting number of lines.
count_line=0
list_line=[]
list_org=[]
for i in sys.stdin:
    list_line.append(i)
for i in list_line:
    i=i.strip()
    count_line+=1

for line in list_line:
    a=line.split()
    list_org.append(a)

flag_error="No"
for i in Def_Error(list_org):
    if i[0]=="Space between label and colon at":
        flag_error="Yes"
        for j in i:
            print(str(j),end=" ")
        print("")
    if i[0]=="Not defining all variables in the starting at":
        flag_error="Yes"
        for j in i:
            print(str(j),end=" ")
        print("")
    if i[0]=="Use of undefined variables at":
        flag_error="Yes"
        for j in i:
            print(str(j),end=" ")
        print("")
    if i[0]=="Label used at multiple times at":
        flag_error="Yes"
        for j in i:
            print(str(j),end=" ")
        print("")
    if i[0]=="No instruction after label at":
        flag_error="Yes"
        for j in i:
            print(str(j),end=" ")
        print("")
    if i[0]=="Use of undefined Labels at":
        flag_error="Yes"
        for j in i:
            print(str(j),end=" ")
        print("")
    if i[0]=="Illegal use of FLAGS register at":
        flag_error="Yes"
        for j in i:
            print(str(j),end=" ")
        print("")
    if i[0]=="Illegal use of immediate value at":
        flag_error="Yes"
        for j in i:
            print(str(j),end=" ")
        print("")
    if i[0]=="Missing hlt instructions after":
        flag_error="Yes"
        for j in i:
            print(str(j),end=" ")
        print("")
    if i[0]=="hlt not being used as the last instruction at":
        flag_error="Yes"
        for j in i:
            print(str(j),end=" ")
        print("")
    if i[0]=="Misuse of variable as label at":
        flag_error="Yes"
        for j in i:
            print(str(j),end=" ")
        print("")
    if i[0]=="Misuse of label as variable at":
        flag_error="Yes"
        for j in i:
            print(str(j),end=" ")
        print("")
    if i[0]=="Typos error in register at":
        flag_error="Yes"
        for j in i:
            print(str(j),end=" ")
        print("")
    if i[0]=="Typos error in instruction at":
        flag_error="Yes"
        for j in i:
            print(str(j),end=" ")
        print("")
if (flag_error=="No"):
    list_var_add=var_code(list_org,count_line)
    list_label_add=label_code(list_org)
    assembly_code=create_assem_code(list_org,list_label_add)
    printing_machinecode(assembly_code,list_var_add,list_label_add)