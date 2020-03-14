import math

class cal:
#2.球壳计算
    #球壳各带的计算压力
    def f2_1(self,a,b,c,d):
        return a+b*c*d*1e-9

    #球壳各带的厚度
    def f2_2(self,a,b,c,d,e):
        return (a*b)/(4*c*d-a)+e

    #外压校核
    def f2_3(self,a,b,c):
        p = a/(b/c)
        with open('instruction.txt','a',encoding='utf-8')as f:
            if p >0.1:
                f.write('外压校核通过')
            else:
                f.write('外压校核不通过')
        return p

#3.球罐质量计算

    #球壳质量计算
    def f3_1(self,a,b,c):
        return math.pi*a**2*b*c*1e-9

    #介质质量计算
    def f3_2(self,a,b,c):
        return math.pi/6*a**3*b*c*1e-9

    #耐压试验时液体的质量计算
    def f3_3(self,a,b):
        return math.pi/6*a**3*b*1e-9
    
    #积雪质量计算
    def f3_4(self,a,b,c,d):
        return math.pi/(4*a)*b**2*c*d*1e-6

    #保温层质量计算
    def f3_5(self):
        return 0

    #支柱和拉杆的质量
    def f3_6(self):
        return 24509

    #附件质量
    def f3_7(self):
        return 33962

    #操作状态下球罐的质量计算
    def f3_8(self,a,b,c,d,e,f,):
        return sum((a,b,c,d,e,f))

    #耐压试验状态下的球罐质量
    def f3_9(self,a,b,c,d):
        return sum((a,b,c,d))

    #球罐的最小质量
    def f3_10(self,a,b,c):
        return sum((a,b,c))

#4.地震载荷计算

    #支柱横截面的惯性矩
    def f4_1_1(self,a,b):
        return math.pi/64*(a**4-b**4)

    #拉杆影响系数
    def f4_1_2(self,a,b):
        return 1-(a/b)**2*(3-(2*a)/b)

    #球罐的基本自振周期   
    def f4_1_3(self,a,b,c,d,e,f):
        return math.pi*((a*b**3*c*1e-3)/(3*d*e*f))**(1/2)

    #曲线下降段的衰减指数
    def f4_2_1(self,a):
        return 0.9+(0.05-a)/(0.3+6*a)

    #阻尼调整系数
    def f4_2_2(self,a):
        return 1+(0.05-a)/(0.08+1.6*a)

    #对应于自振周期T的地震影响系数
    def f4_2_3(self,a,b,c,d,e):
        return (a/b)**c*d*e

    #球罐的水平地震载荷
    def f4_2_4(self,a,b):
        return a*b*9.81

#5.风载荷计算

    #风振系数
    def f5_1(self,a):
        return 1+0.35*a

    #球罐的水平风力
    def f5_2(self,a,b,c,d,e,f):
        return math.pi/4*a**2*b*c*d*e*f*1e-6

#6.弯矩计算

    #(Fe+0.25Fw)与Fw的较大值，Fmax
    def f6_1(self,a,b):
        c = a + 0.25*b
        return c if c > b else b

    #力臂L
    def f6_2(self,a,b):
        return a-b
    
    #由水平地震载荷和水平风力引起的最大弯矩
    def f6_3(self,a,b):
        return a*b

#7.支柱计算

    #操作状态下的重力载荷
    def f7_1_1_1(self,a,b):
        return a*9.81/b

    #耐压实验状态下的重力载荷
    def f7_1_1_2(self,a,b):
        return a*9.81/b

    #最大弯矩对支柱产生的垂直载荷的最大值（查GB 12337 表22)
    def f7_1_2_1(self,a,b):
        return 0.2*a/b

    #拉杆作用在支柱上的垂直载荷的最大值
    def f7_1_2_2(self,a,b,c):
        return 0.3236*a*b/c

    #以上两力之和的最大值
    def f7_1_2_3(self,a,b,c,d):
        return 0.1176*a/b+0.3078*c*d/b

    #操作状态下支柱的最大垂直载荷
    def f7_2_1(self,a,b):
        return a+b

    #耐压实验状态下支柱的最大垂直载荷
    def f7_2_2(self,a,b,c,d):
        return a+0.3*b*c/d

    #操作状态下介质在赤道线额液柱静压力
    def f7_3_1_1(self,a,b):
        return a*b*9.81*1e-9

    #耐压试验状态下液体在赤道的液柱静压力
    def f7_3_1_2(self,a,b):
        return a*b*9.81*1e-9

    #操作状态下球壳赤道线的薄膜应力
    def f7_3_1_3(self,a,b,c,d):
        return (a+b)*(c+d)/(4*d)

    #耐压试验状态下球壳赤道线的薄膜应力
    def f7_3_1_4(self,a,b,c,d):
        return (a+b)*(c+d)/(4*d)

    #操作状态下支柱的偏心弯矩球
    def f7_3_1_5(self,a,b,c,d,e):
        return a*b*c/d*(1-e)

    #耐压试验状态下支柱的偏心弯矩
    def f7_3_1_6(self,a,b,c,d,e):
        return a*b*c/d*(1-e)

    #操作状态下支柱的附加弯矩
    def f7_3_2_1(self,a,b,c,d,e,f,g):
        return 6*a*b*c*d/(e**2*f)*(1-g)

    

    #耐压试验状态下支柱的附加弯矩
    def f7_3_2_2(self,a,b,c,d,e,f,g):
        return 6*a*b*c*d/(e**2*f)*(1-g)

    #单个支柱的横截面积
    def f7_4_1(self,a,b):
        return math.pi/4*(a**2-b**2)

    #支柱的惯性半径

    #支柱长细比
    def f7_4_2(self,a,b,c):
        return a*b/c

    #支柱换算长细比
    def f7_4_3(self,a,b,c):
        return a/math.pi*(b/c)**0.5

    #弯矩作用平面内的轴心受压支柱稳定系数
    def f7_4_4(self,a,b,c):
        return 1/(2*a**2)*((b+c*a+a**2)-((b+c*a+a**2)**2-4*a**2)**0.5)

    #单个支柱的截面系数
    def f7_4_5(self,a,b):
        return math.pi*(a**4-b**4)/(32*a)

    #欧拉临界力
    def f7_4_6(self,a,b,c):
        return (math.pi)**2*a*b/c**2

    #支柱材料的许用应力
    

    #操作状态下支柱的稳定性校核
    def f7_4_7(self,a,b,c,d,e,f,g,h,i):
        return a/(b*c)+d*e/(f*g*(1-0.8*h/i))

    #耐压试验状态下支柱的稳定性校核
    def f7_4_7(self,a,b,c,d,e,f,g,h,i):
            return a/(b*c)+d*e/(f*g*(1-0.8*h/i))

#8.地脚螺栓计算

    #拉杆值支柱间的夹角
    def f8_1_1(self,a,b,c):
        return math.atan(2*a*math.sin(math.pi/b)/c)

    #拉杆作用在支柱上的水平力
    def f8_1_2(self,a,b):
        return a*math.tan(b)
 
    #支柱底板与基础的摩擦力
    def f8_2_1(self,a,b,c):
        return a*b*9.81/c

    #地脚螺栓材料的许用剪应力
    def f8_3_1(self,a):
        return 0.4*a

    #地脚螺栓的螺纹小径
    def f8_3_2(self,a,b,c,d,e):
        return 1.13*((a-b)/(c*d))**0.5+e

#9.底板厚度
    #支柱底板直径

    def f9_1_1(self,a,b):
        return 1.13*(a/b)**0.5

    def f9_1_2(self,a,b):
        return 10*a+b

    #底板厚度
    def f9_2_1(self,a,b):
        return 4*a/(math.pi*b**2)

    def f9_2_2(self,a,b,c,d):
        ans = (3*a*b**2/c)**0.5+d
        return math.ceil(ans)+2

#10.拉杆计算

    #拉杆的最大应力
    def f10_1_1(self,a,b):
        return a/math.cos(b)

    #拉杆材料的许用应力

    #拉杆螺纹小径
    def f10_1_2(self,a,b,c):
        return 1.13*(a/b)**0.5+c

    #销子材料的许用剪切力

    #销子直径
    def f10_2_1_1(self,a,b):
        return 0.8*(a/b)**0.5

    #耳板厚度
    def f10_2_2_1(self,a,b,c):
        return a/(b*c)
    
    #翼板厚度
    def f10_2_3_1(self,a,b,c):
        thk = a/2*b/c
        return math.ceil(thk)+2

    #耳板与支柱连接焊缝A的剪切应力校核
    def f10_2_4_1(self,a,b,c,d):
        ans = a/(1.41*b*c)
        with open('instruction.txt','a',encoding='utf-8')as f:
            if ans < d :
                f.write('校核合格\n')
            else:
                f.write('校核不合格\n')

    #拉杆与翼板的焊缝B的剪切应力校核
    def f10_2_4_2(self,a,b,c,d):
        ans = a/(2.82*b*c)
        with open('instruction.txt','a',encoding='utf-8')as f:
            if ans < d :
                f.write('校核合格\n')
            else:
                f.write('校核不合格\n')

#11.支柱与球壳连接最低点a的应力校核

    #操作状态下a点的剪切应力
    def f11_1_1(self,a,b,c,d):
        return (a+b)/(2*c*d)

    #耐压试验状态下a点的剪切应力
    def f11_1_2(self,a,b,c,d,e,f):
        return (a+0.3*b*c/d)/(2*e*f)

    #操作状态下介质在a点的液柱静压力
    def f11_2_1(self,a,b):
        return a*b*9.81*1e-9

    #耐压试验状态下液体在a点的液柱静压力
    def f11_2_2(self,a,b):
        return a*b*9.81*1e-9

    #操作状态下a点的纬向应力
    def f11_2_3(self,a,b,c,d):
        return (a+b)*(c+d)/(4*d)

    #耐压试验状态下a点的纬向应力
    def f11_2_4(self,a,b,c,d):
        return (a+b)*(c+d)/(4*d)

    #操作状态下a点的应力组合

    #耐压试验状态下a点的组合应力

    #操作状态下应力校核
    def f11_3_1(self,a,b,c):
        ans = a*b
        with open('instruction.txt','a',encoding='utf-8')as f:
            if c < ans:
                f.write('校验合格\n')
            else:
                f.write('校验不合格\n')

    #耐压状态下应力校核
    def f11_3_2(self,a,b,c):
        ans = 0.9*a*b
        with open('instruction.txt','a',encoding='utf-8')as f:
            if c < ans:
                f.write('校验合格\n')
            else:
                f.write('校验不合格\n')

#12.支柱与球壳连接焊缝的强度校核

    #W的取值
    def f12_1(self,a,b,c,d,e):
        ans1 = a+c
        ans2 = b+0.3*c*d/e
        return max(ans1,ans2)

    #支柱与与球壳连接焊缝所承受的剪切应力
    def f12_2(self,a,b,c):
        return a/(1.41*b*c)








