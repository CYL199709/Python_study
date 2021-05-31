
def cal_fun(str_num,res):
    num = []
    for i in range(0,len(str_num)):
        num.append(int(str_num[i]))
    for i in range(0, len(str_num)):
        for j in range(i, len(str_num)):
            if num[i] +num[j] == res:
                print("{",i,":",num[i],",",j,":",num[j],"}")
                return 0
    print("No solution")
    return 0


if __name__ == '__main__':
    print("请输入num_poool:")
    str_num = (input().split())
    print("请输入result:")
    res = int(input())
    cal_fun(str_num, res)



