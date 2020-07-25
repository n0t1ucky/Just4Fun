import random
import pandas
import numpy as np
import time
from progress.bar import Bar
class record:
    def __init__(self):
        self.totTimes=0
        self.ssrGuarantee=0
        self.srGuarantee=True
        self.ssrGot=0
        self.srGot=0
        self.rGot=0
        self.nGot=0
        self.timesBeforeSSR=[]
    def refresh(self):
        self.__init__()
    def showRcd(self):
        print('#{:>10} {:<10}#'.format('SSR',self.ssrGot))
        print('#{:>10} {:<10}#'.format('SR',self.srGot))
        print('#{:>10} {:<10}#'.format('R',self.rGot))
        print('#{:>10} {:<10}#'.format('N',self.nGot))
        print('#{:>10} {:<10}#'.format('TOTAL',self.totTimes))
        print('#{:>10} {:<10}#'.format('GUARNTEE',self.ssrGuarantee))
    def showAvg4SSR(self):
        avg=sum(self.timesBeforeSSR)/len(self.timesBeforeSSR)
        print('avg={},max={},min={}'.format(avg,max(self.timesBeforeSSR),min(self.timesBeforeSSR)))
def getGurantee(probList,rcd):
    # SSR保底机制:
    # 提高SSR的获取几率
    # 等比例降低其他三种稀有度的获取几率
    pList=probList.copy()
    ssrRate=rcd.ssrGuarantee-50
    if ssrRate>0:
        pList[0]+=0.02*ssrRate
        for i in range(1,4):
            pList[i]-=(0.02*ssrRate)*pList[i]/0.98
    # SR保底机制:
    # 将R和N的获取几率降低为0
    if rcd.srGuarantee==True and rcd.totTimes==9:
        pList[1]+=pList[2]+pList[3]
        pList[2],pList[3]=0.0,0.0
        rcd.srGuarantee=False
    return pList
def gacha(probList,rcd):
    # 获取保底情况并抽卡
    pList=getGurantee(probList,rcd)
    randomCode=random.random()
    Code=0
    if randomCode<=pList[0]:
        rcd.ssrGot+=1
        Code=6
    elif pList[0]<randomCode<=pList[0]+pList[1]:
        rcd.srGot+=1
        Code=5
    elif pList[0]+pList[1]<randomCode<=pList[0]+pList[1]+pList[2]:
        rcd.rGot+=1
        Code=4
    else:
        rcd.nGot+=1
        Code=3
    # 抽卡后统计
    rcd.totTimes+=1
    if Code!=6:
        rcd.ssrGuarantee+=1
    else:
        rcd.timesBeforeSSR.append(rcd.ssrGuarantee)
        rcd.ssrGuarantee=0
    if rcd.srGuarantee==True and Code>=5:
        rcd.srGuarantee=False
    return Code

def printStar(stars,toPrint=True):
    starStr=''
    if stars>4:
            starStr='['+'★ '*stars+']'
    else:
            starStr='['+'☆ '*stars+']'
    if toPrint:
        print(starStr)
    return starStr

simpleRecord=record()
probabilityList=[0.02,0.08,0.5,0.4]
random.seed()
inputCode=input()
gachaCode=0
resultList=[]

while inputCode!='0':
    tmpStr=''
    if inputCode in [str(i) for i in range(10)]:
        for i in range(int(inputCode)):
            gachaCode=gacha(probabilityList,simpleRecord)
            tmpStr=printStar(gachaCode)
            resultList.append(tmpStr)
    elif inputCode=='10':
        tmpList=[]
        for j in range(10):
            gachaCode=gacha(probabilityList,simpleRecord)
            tmpStr=printStar(gachaCode,False)
            print(tmpStr,end=',')
            tmpList.append(tmpStr)
        resultList+=tmpList
    elif inputCode[:2]=='10':
        bar=Bar('Progress:',max=int(inputCode[3:]))
        for i in range(int(inputCode[3:])):
            tmpList=[]
            for j in range(10):
                gachaCode=gacha(probabilityList,simpleRecord)
                tmpStr=printStar(gachaCode,False)
                #print(tmpStr,end=',')
                tmpList.append(tmpStr)
            resultList+=tmpList
            bar.next()
        bar.finish()
        print(inputCode+'...Done!')
    elif inputCode=='count':
        simpleRecord.showRcd()
    elif inputCode=='list':
        print(resultList)
    elif inputCode=='prob':
        tmpList=getGurantee(probabilityList,simpleRecord)
        print('#{:>4} {:<6.2}#'.format('SSR',tmpList[0]))
        print('#{:>4} {:<6.2}#'.format('SR',tmpList[1]))
        print('#{:>4} {:<6.2}#'.format('R',tmpList[2]))
        print('#{:>4} {:<6.2}#'.format('N',tmpList[3]))
    elif inputCode=='reset':
        simpleRecord.refresh()
    elif inputCode=='avg':
        simpleRecord.showAvg4SSR()
    inputCode=input()

