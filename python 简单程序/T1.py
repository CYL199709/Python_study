f = []
g = []
f.append(0)
g.append(1)

def cal_fun(n):
    for i in range(1,n+1):
        f.append(f[i-1] + 2 * g[i-1])
        g.append(2*g[i - 1] -3 * f[i - 1])
    print("f(",n,")=",f[n] )
    print("g(",n,")=",g[n] )

if __name__ == '__main__':
    print("请输入n:")
    N = int(input())
    cal_fun(N)
    cal_fun(5)
