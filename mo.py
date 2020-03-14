import json
import math
import re
from func import *


#打开一个txt文件(没有则新建),然后清除上次的内容
with open('instruction.txt','w')as f:
    f.seek(0)
    f.truncate()
#定义一个写入文件的函数
def wri():
    with open('instruction.txt','a',encoding='utf-8')as f:
        for k,v in tmp.items():
            f.write(str(k)+' : '+str(v))
            f.write('\n') 


#打开数据存储的json文件并读入
with open('data.json', 'r',encoding='utf-8') as f:
    json_data = json.load(f)

if __name__ == '__main__':
    #申明一个计算的类
    x = cal()
#1.设计条件
    
    tmp = json_data['设计条件']
    with open('instruction.txt','a',encoding='utf-8')as f:
        f.write('1.设计条件\n')

    #写入设计条件   
    wri()

    del tmp

#2.球壳计算
    with open('instruction.txt','a',encoding='utf-8')as f:   
        f.write('-------------------------------------------------------------\n')
        f.write('-------------------------------------------------------------\n')




        f.write('2 球壳计算\n')
        f.write('2.1计算压力\n')

    #申请一个临时字典存放数据
    tmp = json_data['球壳计算']['计算压力']

    wri()

    #计算压力
    pc1 = x.f2_1(tmp['设计压力'],tmp['液柱高度h1'],tmp['介质密度'],tmp['重力加速度'])
    pc2 = x.f2_1(tmp['设计压力'],tmp['液柱高度h2'],tmp['介质密度'],tmp['重力加速度'])
    pc3 = x.f2_1(tmp['设计压力'],tmp['液柱高度h3'],tmp['介质密度'],tmp['重力加速度'])
    with open('instruction.txt','a',encoding='utf-8')as f: 
        f.write('pc1=')
        f.write(str(pc1)+' MPa\n')
        f.write('pc2=')
        f.write(str(pc2)+' MPa\n')
        f.write('pc3=')
        f.write(str(pc3)+' MPa\n')


    #删除临时字典
    del tmp

    with open('instruction.txt','a',encoding='utf-8')as f: 
        f.write('***************************************************************\n')
        f.write('2.2球壳各带的厚度\n')
    tmp = json_data['球壳计算']['球壳各带的厚度']

    wri()

    
    thk1 = x.f2_2(pc1,tmp['球壳内直径'],tmp['许用应力'],tmp['焊接接头系数'],tmp['厚度附加量'])
    thk2 = x.f2_2(pc2,tmp['球壳内直径'],tmp['许用应力'],tmp['焊接接头系数'],tmp['厚度附加量'])
    thk3 = x.f2_2(pc3,tmp['球壳内直径'],tmp['许用应力'],tmp['焊接接头系数'],tmp['厚度附加量'])

    with open('instruction.txt','a',encoding='utf-8')as f:
        f.write('球壳各带名义厚度\n')
        f.write('δn1=')
        f.write(str(thk1)+' mm\n')
        f.write('δn2=')
        f.write(str(thk2)+' mm\n')
        f.write('δn3=')
        f.write(str(thk3)+' mm\n')
        #球壳各带名义厚度
        nthk = math.ceil(max(thk1,thk2,thk3)+2)
        f.write('取球壳的名义厚度: '+str(nthk)+' mm\n')

    del tmp
    with open('instruction.txt','a',encoding='utf-8')as f:
        f.write('*****************************************************************\n')
        f.write('2.3外压校核\n')
    tmp =json_data['球壳计算']['外压校核']
    wri()
    #球壳的有效厚度
    ethk = nthk - tmp['厚度附加量']
    
    #许用外应力
    p = x.f2_3(tmp['系数B'],tmp['球壳的外半径'],ethk)

    #打印内容
    with open('instruction.txt','a',encoding='utf-8')as f:
        f.write('球壳的有效厚度: '+str(ethk)+' mm\n')
        f.write('许用外应力[p]: '+str(p)+' MPa\n')
        if p>0.1:
            f.write('外压校核通过\n')
        else:
            f.write('外压校核不通过\n')

    del tmp

#3.球罐质量计算
    with open('instruction.txt','a',encoding='utf-8')as f:
        f.write('-------------------------------------------------------------------\n')
        f.write('-------------------------------------------------------------------\n')
        f.write('3 球罐质量计算\n')
    tmp =json_data['球罐质量计算']
    #打印条件
    wri()
    #球壳质量
    m1 = x.f3_1(tmp['球壳平均直径'],nthk,tmp['球壳材料密度'])
   
    #介质质量
    m2 = x.f3_2(tmp['球壳内直径'],tmp['介质密度'],tmp['装量系数'])
    
    #耐压试验时液体的质量
    m3 = x.f3_3(tmp['球壳内直径'],tmp['水的密度'])
    
    #积雪质量
    m4 = x.f3_4(tmp['重力加速度'],tmp['球壳外直径'],tmp['基本雪压值'],tmp['球面的积雪系数'])
    
    #保温层质量
    m5 = x.f3_5()
    
    #支柱和拉杆质量
    m6 = x.f3_6()
    
    #附件质量
    m7 = x.f3_7()
    
    #操作状态下的球罐质量
    mO = x.f3_8(m1,m2,m4,m5,m6,m7)

    #耐压试验状态下的球罐质量
    mT = x.f3_9(m1,m3,m6,m7)
    
    #球罐最小质量
    mmin = x.f3_10(m1,m6,m7)

    with open('instruction.txt','a',encoding='utf-8')as f:
        f.write('球壳质量: '+str(m1)+' kg\n')
        f.write('介质质量: '+str(m2)+' kg\n')
        f.write('耐压试验时液体的质量: '+str(m3)+' kg\n')
        f.write('积雪质量: '+str(m4)+' kg\n')
        f.write('保温层质量: '+str(m5)+' (无保温)\n')
        f.write('支柱和拉杆的质量: '+str(m6)+' kg\n')
        f.write('附件质量: '+str(m7)+' kg\n')
        f.write('操作状态下的球罐质量: '+str(mO)+' kg\n')
        f.write('耐压试验状态下的球罐质量: '+str(mT)+' kg\n')
        f.write('球罐的最小质量: '+str(mmin)+' kg\n')

#4.地震载荷计算


    with open('instruction.txt','a',encoding='utf-8')as f:

        f.write('----------------------------------------------------------\n')
        f.write('----------------------------------------------------------\n')
        f.write('4 地震载荷计算\n')
        f.write('4.1自振周期\n')
    tmp = json_data['地震载荷计算']['自振周期']


    #设计条件
    wri()

    #支柱横截面的惯性矩
    I = x.f4_1_1(tmp['支柱外直径'],tmp['支柱内直径'])

    #拉杆影响系数
    eIndx = x.f4_1_2(tmp['支柱底板底面至上支耳销子中心的距离'],tmp['支柱底板底面至球壳中心的距离'])

    #球罐的基本自振周期
    T = x.f4_1_3(mO,tmp['支柱底板底面至球壳中心的距离'],eIndx,tmp['支柱数目'],tmp['支柱材料Q345R的室温弹性模量'],I)

    
    #打印条件

    with open('instruction.txt','a',encoding='utf-8')as f:
        f.write('支柱横截面的惯性矩I: '+str(I)+' mm^4\n')
        f.write('拉杆影响系数ξ ：'+str(eIndx)+' \n')
        f.write('球罐的基本自振周期T :'+str(T)+' s\n')

    del tmp

    with open('instruction.txt','a',encoding='utf-8')as f:

        f.write('***********************************************************\n')
        f.write('4.2地震载荷\n')
    tmp = json_data['地震载荷计算']['地震载荷']

    #打印条件
    wri()
    #曲线下降段的衰减指数
    dIndx = x.f4_2_1(tmp['阻尼比'])

    #阻尼调整系数
    aIndx = x.f4_2_2(tmp['阻尼比'])

    #对应于自振周期T的地震影响系数
    a = x.f4_2_3(tmp['特征周期'],T,dIndx,aIndx,tmp['地震影响系数的最大值'])

    #球罐的水平地震载荷
    Fe = x.f4_2_4(a,mO)

    #打印条件
    with open('instruction.txt','a',encoding='utf-8')as f:
        f.write('曲线下降段的衰减指数γ: ' +str(dIndx)+' \n')
        f.write('阻尼调整系数η2: '+str(aIndx)+' \n')
        f.write('对应与自振周期T的地震影响系数a: '+str(a)+' \n')
        f.write('球罐的水平地震载荷Fe: '+str(Fe)+' N\n')
    del tmp

#5.风载荷计算
    with open('instruction.txt','a',encoding='utf-8')as f:

        f.write('------------------------------------------------------------\n')
        f.write('------------------------------------------------------------\n')


        f.write('5 风载荷计算\n')
    tmp = json_data['风载荷计算']

    #打印条件
    wri()

    #风振系数
    k2 = x.f5_1(tmp['系数'])

    #球罐的水平风力
    Fw = x.f5_2(tmp['球壳外直径'],tmp['风载荷体型系数'],k2,tmp['基本风压值'],tmp['风压高度变化系数'],tmp['球罐附件增大系数'])

    with open('instruction.txt','a',encoding='utf-8')as f:
        f.write('风振系数k2: '+str(k2)+' \n')
        f.write('球罐的水平风力Fw: '+str(Fw)+' N\n')

    del tmp

#6.弯矩计算
    with open('instruction.txt','a',encoding='utf-8')as f:
        f.write('---------------------------------------------------------------\n')
        f.write('---------------------------------------------------------------\n')

        f.write('6.弯矩计算\n')
    tmp = json_data['弯矩计算']

    #打印条件
    wri()

    #(Fe+0.25Fw)与Fw的较大值，Fmax
    Fmax = x.f6_1(Fe,Fw)

    #力臂L
    L = x.f6_2(tmp['支柱底板底面至球壳赤道平面的距离'],tmp['支柱底板底面至上支耳销子中心的距离'])

    #由水平地震载荷和水平风力引起的最大弯矩
    Mmax = x.f6_3(Fmax,L)
    
    with open('instruction.txt','a',encoding='utf-8')as f:
        f.write('(Fe+0.25Fw)与Fw的较大值，Fmax: '+str(Fmax)+' N\n')
        f.write('力臂L:'+str(L)+' mm\n')
        f.write('由水平地震载荷和水平风力引起的最大弯矩'+str(Mmax)+' N*mm\n')
    del tmp

#7.支柱计算
    with open('instruction.txt','a',encoding='utf-8')as f:
        f.write('---------------------------------------------------------------\n')
        f.write('---------------------------------------------------------------\n')
        f.write('7 支柱计算\n')
        f.write('7.1单个支柱的垂直载荷\n')
        f.write('7.1.1重力载荷\n')
    tmp = json_data['支柱计算']['单个支柱的垂直载荷']['重力载荷']

    #打印条件
    wri()
    #操作状态下的重力载荷
    GO = x.f7_1_1_1(mO,tmp['支柱数目'])
    

    #耐压实验状态下的重力载荷
    GT = x.f7_1_1_2(mT,tmp['支柱数目'])
    

    with open('instruction.txt','a',encoding='utf-8')as f:
        f.write('操作状态下的重力载荷:'+str(GO)+' N\n')
        f.write('耐压试验状态下的重力载荷: '+str(GT)+' N\n')
    del tmp
    with open('instruction.txt','a',encoding='utf-8')as f:
        f.write('***************************************************************\n')
        f.write('7.1.2支柱的最大垂直载荷\n')
    tmp = json_data['支柱计算']['单个支柱的垂直载荷']['支柱的最大垂直载荷']

    #打印条件
    wri()
    #最大弯矩对支柱产生的垂直载荷的最大值
    Fimax = x.f7_1_2_1(Mmax,tmp['支柱中心圆半径'])

    #拉杆作用在支柱上的垂直载荷的最大值
    Pijmax = x.f7_1_2_2(tmp['支柱底板底面至上支耳销子中心的距离'],Fmax,tmp['支柱中心圆半径'])

    #以上两力之和的最大值
    Ftotmax = x.f7_1_2_3(Mmax,tmp['支柱中心圆半径'],tmp['支柱底板底面至上支耳销子中心的距离'],Fmax)

    with open('instruction.txt','a',encoding='utf-8')as f:
        f.write('最大弯矩对支柱产生的垂直载荷的最大值: '+str(Fimax)+' N\n')
        f.write('拉杆作用在支柱上的垂直载荷的最大值: '+str(Pijmax)+' N\n')
        f.write('以上两力之和的最大值'+str(Ftotmax)+' N\n')
    del tmp

    with open('instruction.txt','a',encoding='utf-8')as f:
        f.write('****************************************************************\n')
        f.write('7.2组合载荷\n')
    tmp = json_data['支柱计算']['组合载荷']

    #打印条件
    wri()
    #操作状态下支柱的最大垂直载荷
    WO = x.f7_2_1(GO,Ftotmax)

    #耐压实验状态下支柱的最大垂直载荷
    WT = x.f7_2_2(GT,Ftotmax,Fw,Fmax)

    with open('instruction.txt','a',encoding='utf-8')as f:
        f.write('操作状态下支柱的最大垂直载荷: '+str(WO)+' N\n')
        f.write('耐压试验状态下支柱的最大垂直载荷: '+str(WT)+' N\n')
    
    del tmp

    with open('instruction.txt','a',encoding='utf-8')as f:
        f.write('*****************************************************************\n')
        f.write('7.3单个支柱弯矩\n')
        f.write('7.3.1偏心弯矩\n')
    tmp = json_data['支柱计算']['单个支柱弯矩']

    #打印条件
    wri()
    #操作状态下介质在赤道线的液柱静压力
    pOe = x.f7_3_1_1(tmp['操作状态下赤道线的液柱高度'],tmp['介质密度'])
    
    #耐压试验状态下液体在赤道的液柱静压力
    pTe = x.f7_3_1_2(tmp['耐压试验状态下赤道线的液柱高度'],tmp['水的密度'])
    
    #操作状态下球壳赤道线的薄膜应力
    deltaOe = x.f7_3_1_3(tmp['设计压力'],pOe,tmp['球壳内直径'],ethk)
    
    #耐压试验状态下球壳赤道线的薄膜应力
    deltaTe = x.f7_3_1_4(tmp['试验压力'],pTe,tmp['球壳内直径'],ethk)
    
    #操作状态下支柱的偏心弯矩
    MO1 = x.f7_3_1_5(deltaOe,tmp['球壳内半径'],WO,tmp['球壳材料Q370R的室温弹性模量'],tmp['球壳材料的泊松比'])
    
    #耐压试验状态下支柱的偏心弯矩
    MT1 = x.f7_3_1_6(deltaTe,tmp['球壳内半径'],WT,tmp['球壳材料Q370R的室温弹性模量'],tmp['球壳材料的泊松比'])
    
    #打印条件
    with open('instruction.txt','a',encoding='utf-8')as f:
        f.write('操作状态下介质在赤道线的液柱静压力: '+str(pOe)+' MPa\n')
        f.write('耐压试验状态下液体在赤道的液柱静压力: '+str(pTe)+' MPa\n')
        f.write('操作状态下球壳赤道线的薄膜应力: '+str(deltaOe)+' MPa\n')
        f.write('耐压试验状态下球壳赤道线的薄膜应力: '+str(deltaTe)+' MPa\n')
        f.write('操作状态下支柱的偏心弯矩: '+str(MO1)+' N*mm\n')
        f.write('耐压试验状态下支柱的偏心弯矩: '+str(MT1)+' N*mm\n')


    with open('instruction.txt','a',encoding='utf-8')as f:
        f.write('******************************************************************\n')
        f.write('7.3.2 附加弯矩\n')

    #操作状态下支柱的附加弯矩
    MO2 = x.f7_3_2_1(tmp['支柱材料Q345R的室温弹性模量'],I,deltaOe,tmp['球壳内半径'],tmp['支柱底板底面至球壳中心的距离'],tmp['球壳材料Q370R的室温弹性模量'],tmp['球壳材料的泊松比'])
    
    #耐压试验状态下支柱的附加弯矩
    MT2 = x.f7_3_2_2(tmp['支柱材料Q345R的室温弹性模量'],I,deltaTe,tmp['球壳内半径'],tmp['支柱底板底面至球壳中心的距离'],tmp['球壳材料Q370R的室温弹性模量'],tmp['球壳材料的泊松比'])
    
    #打印条件
    with open('instruction.txt','a',encoding='utf-8')as f:
        f.write('操作状态下支柱的附加弯矩: '+str(MO2)+' N*mm\n')
        f.write('耐压试验状态下支柱的附加弯矩： '+str(MT2)+' N*mm\n')
                
    with open('instruction.txt','a',encoding='utf-8')as f:
        f.write('********************************************************************\n')
        f.write('7.3.3总弯矩\n')
    #操作状态下支柱的总弯矩
    MO = MO1 + MO2

    #耐压试验状态下支柱的总弯矩
    MT = MT1 + MT2
    
    with open('instruction.txt','a',encoding='utf-8')as f:
        f.write('操作状态下支柱的总弯矩: '+str(MO)+' N*mm\n')
        f.write('耐压试验状态下的支柱的总弯矩： '+str(MT)+' N*mm\n')

    del tmp

    with open('instruction.txt','a',encoding='utf-8')as f:
        f.write('********************************************************************\n')
        f.write('7.4支柱稳定性校核\n')
    tmp = json_data['支柱计算']['支柱稳定性校核']

    #打印条件
    wri()

    with open('instruction.txt','a',encoding='utf-8')as f:

        #单个支柱的横截面积
        A = x.f7_4_1(tmp['支柱外直径'],tmp['支柱内直径'])
        f.write('单个支柱的横截面积'+str(A)+' mm^2\n')

        #支柱的惯性半径
        ri = (I/A)**0.5
        f.write('支柱的惯性半径: '+str(ri)+' mm\n')

        #支柱长细比
        lrratio = x.f7_4_2(tmp['计算长度系数'],tmp['支柱底板底面至球壳中心的距离'],ri)
        f.write('支柱长细比: '+str(lrratio)+' \n')

        #支柱换算长细比
        clrratio = x.f7_4_3(lrratio,tmp['支柱材料Q345R的室温屈服强度'],tmp['支柱材料Q345R的室温弹性模量'])
        f.write('支柱换算长细比: '+str(clrratio)+' \n')

        #弯矩作用平面内的轴心受压支柱稳定系数
        sIndx = x.f7_4_4(clrratio,tmp['系数α2'],tmp['系数α3'])
        f.write('弯矩作用平面内的周鑫受压支柱稳定系数: '+str(sIndx)+' \n')

        #单个支柱的截面系数
        Z = x.f7_4_5(tmp['支柱外直径'],tmp['支柱内直径'])
        f.write('单个支柱的截面系数: '+str(Z)+' \n')

        #欧拉临界力
        WEX = x.f7_4_6(tmp['支柱材料Q345R的室温弹性模量'],A,lrratio)
        f.write('欧拉临界力: '+str(WEX)+' N\n')

        #支柱材料的许用应力
        deltaC = tmp['支柱材料Q345R的室温屈服强度']/1.5
        f.write('支柱材料的许用应力: '+str(deltaC)+' MPa\n')

        #操作状态下支柱的稳定性校核
        PcheckO = x.f7_4_7(WO,sIndx,A,tmp['等效弯矩系数'],MO,tmp['截面塑性发展系数'],Z,WO,WEX)
        f.write('操作状态下支柱的稳定性校核: '+str(PcheckO)+' MPa\n')

        if PcheckO < deltaC:
            f.write('校核合格\n')
        else:
            f.write('校核不合格\n')
        #耐压试验状态下支柱的稳定性校核
        PcheckT = x.f7_4_7(WT,sIndx,A,tmp['等效弯矩系数'],MT,tmp['截面塑性发展系数'],Z,WO,WEX)
        f.write('耐压试验状态下支柱的稳定性校核: '+str(PcheckT)+' MPa\n')
        if PcheckO < deltaC:
            f.write('校核合格\n')
        else:
            f.write('校核不合格\n')
    
    del tmp

#8.地脚螺栓计算

    with open('instruction.txt','a',encoding='utf-8')as f:
        
        f.write('-----------------------------------------------------------------------\n')
        f.write('-----------------------------------------------------------------------\n')
        f.write('8.地脚螺栓计算\n')
        f.write('8.1拉杆作用在支柱上的水平力\n')
    tmp = json_data['地脚螺栓计算']

    #设计条件
    wri()
    with open('instruction.txt','a',encoding='utf-8')as f:
        #拉杆与支柱间的夹角
        beta = x.f8_1_1(tmp['支柱中心圆半径'],tmp['支柱数目'],tmp['支柱底板底面至上支耳销子中心的距离'])
        f.write('拉杆与支柱间的夹角: '+str(beta)+' rad\n')
        #拉杆作用在支柱上的水平力
        Fc = x.f8_1_2(Pijmax,beta)
        f.write('拉杆作用在支柱上的水平力: '+str(Fc)+' N\n')

        f.write('8.2支柱底板与基础的摩擦力')
        #支柱底板与基础的摩擦力
        Fs = x.f8_2_1(tmp['支柱底板与基础的摩擦系数'],mmin,tmp['支柱数目'])
        f.write('支柱底板与基础的摩擦力'+str(Fs)+' N\n')

        if Fs < Fc:

            f.write('8.3地脚螺栓\n')
            #地脚螺栓材料的许用剪应力
            deltaB = x.f8_3_1(tmp['地脚螺栓材料Q235B室温屈服强度'])
            f.write('地脚螺栓材料的许用剪应力: '+str(deltaB)+' MPa\n')
            #地脚螺栓的螺纹小径
            dB = x.f8_3_2(Fc,Fs,tmp['每个支柱上的地脚螺栓个数'],deltaB,tmp['地脚螺栓的腐蚀裕量'])
            f.write('地脚螺栓的螺纹小径: '+str(dB)+' mm\n')
        else:
            f.write('不需要添加地脚螺栓\n')
    
    del tmp

#9.底板厚度
    with open('instruction.txt','a',encoding='utf-8')as f:
        f.write('------------------------------------------------------------------\n')
        f.write('------------------------------------------------------------------\n')
        f.write('9.支柱底板\n')
        f.write('9.1支柱底板直径\n')
    tmp = json_data['支柱底板']
    #打印条件
    wri()

    with open('instruction.txt','a',encoding='utf-8')as f:
        #支柱底板直径
        Db1 = x.f9_1_1(WT,tmp['钢筋混凝土许用压应力'])
        Db2 = x.f9_1_2(tmp['地脚螺栓直径'],tmp['支柱外直径'])
        Db =int((max(Db1,Db2)/50)+1)*50
        f.write('支柱底板直径: '+str(Db)+' mm\n')

        #底板的压应力
        sigmabc = x.f9_2_1(WT,Db)
        f.write('底板的压应力: '+str(sigmabc)+' MPa\n')

        #底板外边缘至支柱外表面的距离
        lb = (Db-tmp['支柱外直径'])/2
        f.write('底板外边缘至支柱外表面的距离: '+ str(lb)+' mm\n')

        #底板材料的许用弯曲应力
        sigmab = tmp['底板材料Q345R室温屈服强度']/1.5
        f.write('底板材料的许用弯曲应力： '+str(sigmab)+' MPa\n')

        #底板厚度
        deltab = x.f9_2_2(sigmabc,lb,sigmab,tmp['底板的腐蚀裕量'])
        f.write('底板厚度: '+str(deltab)+' mm\n')

    del tmp

#10.拉杆计算
    with open('instruction.txt','a',encoding='utf-8')as f:
        f.write('---------------------------------------------\n')
        f.write('---------------------------------------------\n')
        f.write('10.拉杆计算')
    tmp = json_data['拉杆计算']
    #打印条件
    wri()
    with open('instruction.txt','a',encoding='utf-8')as f:

        #拉杆的最大应力
        FT = x.f10_1_1(Pijmax,beta)
        f.write('拉杆的最大应力: '+str(FT)+' MPa\n')

        #拉杆材料的许用应力
        sigmaT = tmp['拉杆材料Q235B室温屈服强度']/1.5
        f.write('拉杆材料的许用应力: '+str(sigmaT)+' MPa\n')
        #拉杆螺纹小径

        dT = x.f10_1_2(FT,sigmaT,tmp['拉杆的腐蚀裕量'])
        f.write('拉杆螺纹小径： '+str(dT)+' mm\n')

        f.write('************************************************\n')
        f.write('10.2销子连接部位的计算\n')
        f.write('10.2.1销子直径\n')
        #销子材料的许用剪切力
        taoP = 0.4*tmp['销子材料35室温屈服强度']
        f.write('销子材料的许用剪切力: '+str(taoP)+' MPa\n')

        #销子直径
        dP = x.f10_2_1_1(FT,taoP)
        f.write('销子直径: '+str(dP)+' mm\n')

        f.write('**************************************************\n')
        f.write('10.2.2耳板厚度\n')
        #耳板材料的许用压应力
        sigmac = tmp['耳板材料Q235B室温屈服强度']/1.1
        f.write('耳板材料的许用压应力: '+str(sigmac)+' MPa\n')

        #耳板厚度
        deltac = x.f10_2_2_1(FT,dP,sigmac)
        f.write('耳板厚度： '+str(deltac)+' mm\n')

        f.write('**************************************************\n')
        f.write('10.2.3翼板厚度\n')
        #翼板厚度
        deltaa = x.f10_2_3_1(deltac,tmp['耳板材料Q235B室温屈服强度'],tmp['翼板材料Q235B室温屈服强度'])
        f.write('翼板厚度: '+str(deltaa)+' mm\n')

        f.write('**************************************************\n')
        f.write('10.2.4连接焊缝强度验算\n')

        #A焊缝的许用剪切应力
        taoWA = 0.4*tmp['支柱或耳板材料屈服强度的较小值']*tmp['角焊缝系数']
        f.write('A焊缝的许用剪切应力: '+str(taoWA)+' MPa\n')

        #耳板与支柱连接焊缝A的剪切应力校核
        x.f10_2_4_1(FT,tmp['A焊缝单边长度'],tmp['A焊缝焊脚尺寸'],taoWA)

        #B焊缝的许用剪切应力
        taoWB = 0.4*tmp['拉杆或翼板材料屈服强度的较小值']*tmp['角焊缝系数']
        f.write('B焊缝的许用剪切应力： '+str(taoWB)+' MPa\n')
        #拉杆与翼板的焊缝B的剪切应力校核
        x.f10_2_4_2(FT,tmp['B焊缝单边长度'],tmp['B焊缝焊脚尺寸'],taoWB)

    del tmp

#11.支柱与球壳连接最低点a的应力校核

    with open('instruction.txt','a',encoding='utf-8')as f:
        f.write('---------------------------------------------------------------\n')
        f.write('---------------------------------------------------------------\n')
        f.write('11.支柱与球壳连接最低点a的应力校核\n')
        tmp = json_data['支柱与球壳连接最低点a的应力校核']
        #打印调价
        wri()
        f.write('11.1.a点的剪切应力\n')

        #操作状态下a点的剪切应力
        taoO = x.f11_1_1(GO,Fimax,tmp['支柱与球壳连接焊缝单边的弧长'],tmp['球壳a点处的有效厚度'])
        f.write('操作状态下a点的剪切应力: '+str(taoO)+' MPa\n')
        #耐压试验状态下a点的剪切应力
        taoT = x.f11_1_2(GT,Fimax,Fw,Fmax,tmp['支柱与球壳连接焊缝单边的弧长'],tmp['球壳a点处的有效厚度'])
        f.write('耐压试验状态下a点的剪切应力: '+str(taoT)+' MPa\n')
        f.write('*************************************************\n')
        f.write('11.2.a点的纬向应力\n')

        #操作状态下介质在a点的液柱静压力
        pOa = x.f11_2_1(tmp['操作状态下a点的液柱高度'],tmp['介质密度'])
        f.write('操作状态下介质在a点的液柱静压力: '+str(pOa)+' MPa\n')
        #耐压试验状态下液体在a点的液柱静压力
        pTa = x.f11_2_2(tmp['耐压实验状态下a点的液柱高度'],tmp['水的密度'])
        f.write('耐压试验状态下液体在a点的液柱静压力: '+str(pTa)+' MPa\n')
        #操作状态下a点的纬向应力
        sigmaO1 =x.f11_2_3(tmp['设计压力'],pOa,tmp['球壳内直径'],tmp['球壳a点处的有效厚度'])
        f.write('操作状态下a点的纬向应力: '+str(sigmaO1)+' MPa\n')

        #耐压试验状态下a点的纬向应力
        sigmaT1 = x.f11_2_4(tmp['试验压力'],pTa,tmp['球壳内直径'],tmp['球壳a点处的有效厚度'])
        f.write('耐压试验状态下a点的纬向应力: '+str(sigmaT1)+' MPa\n')

        f.write('*******************************************\n')
        f.write('11.3.a点的应力校核\n')
            
        #操作状态下a点的组合应力
        sigmaOa = sigmaO1 + taoO
        f.write('操作状态下a点的组合应力: '+str(sigmaOa)+' MPa\n')

        #耐压试验状态下a点的组合应力
        sigmaTa = sigmaT1 + taoT
        f.write('耐压试验状态下a的组合应力： '+str(sigmaTa)+' MPa\n')

        #操作状态下应力校核
        x.f11_3_1(tmp['许用应力'],tmp['焊接接头系数'],sigmaOa)

        #耐压状态下应力校核
        x.f11_3_2(tmp['支柱或球壳材料屈服强度的较小值'],tmp['焊接接头系数'],sigmaTa)

    del tmp

#12.支柱与球壳连接焊缝的强度校核
    with open('instruction.txt','a',encoding='utf-8')as f:
        f.write('---------------------------------------------\n')
        f.write('---------------------------------------------\n')
        f.write('12.支柱与球壳连接焊缝的强度校核\n')
    tmp = json_data['支柱与球壳连接焊缝的强度校核']
    #打印条件
    wri()
    with open('instruction.txt','a',encoding='utf-8')as f:
        #W的取值
        W = x.f12_1(GO,GT,Fimax,Fw,Fmax)
        f.write('W的取值: '+str(W)+' N\n')

        #支柱与球壳连接焊缝所承受的剪切应力
        taow = x.f12_2(W,tmp['支柱与球壳连接焊缝单边的弧长'],tmp['支柱与球壳连接焊缝焊脚尺寸'])
        f.write('支柱与球壳连接焊缝所承受的剪切应力: '+str(taow)+'  MPa\n')
        #焊缝许用剪切应力
        taoW = 0.4*tmp['支柱或球壳材料屈服强度的较小值']*tmp['角焊缝系数']
        f.write('焊缝许用剪切应力: '+str(taoW)+' MPa\n')

        #应力校核
        f.write('应力校核：')
        if taow < taoW:
            f.write('校核合格\n')
        else:
            f.write('校核不合格\n')
    del tmp

    print('已生成说明书\n')