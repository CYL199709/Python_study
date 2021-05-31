
def cal_fun(str_num):
    num = []
    count = 0
    for i in range(0,len(str_num)):
        num.append(int(str_num[i]))
    for i in range(0,len(str_num)):
        for j in range(i, len(str_num)):
            if num[i] >num[j]:
                temp = num[i]
                num[i] = num[j]
                num[j] = temp
    for i in range(1, len(str_num)):
        if num[i-1] == num[i]:
            count = count + 1

    if count == 1:
        print("True")
    else :
        print("False")

if __name__ == '__main__':
    print("请输入Input:")
    str_num = (input().split())
    cal_fun(str_num)



