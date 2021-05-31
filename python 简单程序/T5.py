
def cal_fun(str_in):
    count = 0
    instr = []
    if len(str_in) < 8 or len(str_in) > 15:
        print("Invalid Passward")
        return 0
    for i in range(0, len(str_in)):
        instr.append(str_in[i])
    for i in range(0,len(str_in)):
        for j in range(i, len(str_in)):
            if instr[i] > instr[j]:
                temp = instr[i]
                instr[i] = instr[j]
                instr[j] = temp
    if instr[0] >= "0" and instr[0] <= "9" and instr[len(str_in)-1] >= "A" and instr[len(str_in)-1] <= "z":
        for i in range(1, len(str_in)-1):
            if str_in[i] == str_in[i-1] and  str_in[i] == str_in[i+1]:
                print("Weak Password")
                return 0
        print("Strong Passward")
    else:
        print("Weak Password")





if __name__ == '__main__':
    print("请输入Input:")
    str_in = input()
    result = cal_fun(str_in)



