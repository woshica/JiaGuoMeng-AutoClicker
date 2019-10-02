import json, time
from os import makedirs
import sys, argparse





####################################################################################################
#
#   定义了各种鼠标事件的间隔时间、屏幕位置等信息。
#   如果运行脚本时出现错误或性能问题，可以尝试更改间隔时间或更改坐标。
#
####################################################################################################

moveInterval = 150                                  #定义了鼠标移动时各个事件间需要等待的时间（单位是毫秒）
clickInterval = 20                                  #定义了两次鼠标点击事件间需要等待的时间
upgradeInterval = 300                               #定义了升级建筑时点击事件间需要等待的时间
initialTime = 500                                   #定义了脚本在初始时需要等待的时间

collectRateWhileTrain = 2                           #定义了火车来的时候，每进行几次拖拽收集一次金币（单位是次数）
UpdateRateWhileCollect = 10                         #定义了升级建筑时，每收集几次金币升级

allEvents = ["MouseDown", "MouseMove", "MouseUp"]   #定义了各个事件的名称

#屏幕坐标是蓝叠内使用的坐标，定义的是坐标点在手机屏幕的x、y轴上所占的百分比。比如(50, 50)就是屏幕的正中间，(0, 0)是左上角，(0, 100)是左下角，etc。
pos = {
    "buildingPos" : #定义了建筑的位置
        [
            (26.76, 61.07), (51.46, 55.58), (72.26, 48.25),
            (30.9, 51.81), (53.77, 44.35), (73.84, 35.92),
            (26.52, 35.06), (51.09, 27.69), (74.14, 21.25)
        ],
    "trainPos" : #定义了火车上的三个货物的位置
        [(61.44, 85.01), (77.13, 81.52), (89.78, 76.87)],
    "otherPos" : #定义了开启建筑编辑界面按钮以及升级按钮的位置
        {
            "openUpgrade" : (90.88, 60.22),
            "upgrade" : (78.18, 89.43),
            "openExchange" : (50.00, 89.43),
            "lightPos" : (50.00, 80.00),
            "exchange" : (50.00, 43.40),
            "moveDistence" : (0.00, 19.43),
            "exchangeoffset": (0.00, 21.00)
        }
}

#定义了导出成json时各个事件系列的函数名对应的文件名和快捷键。其中每一项的key值必须对应Mission中的一个函数。
exportConfiguration = {
    "autoCollect" : {
       "name" : "自动收取硬币",
       "shortCut" :  "s"
    },
    "autoUpgrade" : {
        "name" : "自动升级建筑",
        "shortCut" : "u"
    },
    "autoTrain" : {
        "name" : "自动火车发货",
        "shortCut" : ""
    },
    "autoTrainYellowOnly" : {
        "name" : "自动火车发货(仅黄色)",
        "shortCut" : "y"
    }
}



####################################################################################################
#
#   定义了Mission类。一个Mission是由一个或一系列需要重复执行的事件组成的。
#   一个Mission中的事件系列可以很简单，比如重复点击屏幕上的某个坐标；也可以比较复杂，比如自动收取火车上的货物，同时保证每秒收取一次金币。
#   不同的事件系列的创建是通过在Mission中定义不同的函数实现的，这些任务可以通过互相调用的方式相互组合、叠加，从而创建出更复杂而不失可读性的事件系列。
#   同时，Mission类还提供了自动生成json文件的接口。
#
####################################################################################################

class Mission():
    '''
    Mission类定义了一个需要重复执行的任务，同时提供了一些便捷的添加事件的方法。
    '''
    def __init__(self, buildingsNeedUpgrade, epicBuildings, exchangeBuildings):
        self.buildingsNeedUpgrade = buildingsNeedUpgrade #self.buildingsNeedUpgrade中存储了需要升级的建筑的编号
        self.epicBuildings = epicBuildings #self.epicBuildings中存储了需要接受火车货物的建筑的编号
        self.exchangeBuildings = exchangeBuildings

        self.initialize()
    
    def addEvent(self, pos, eventType, Delta = 0):
        """
        在Mission的事件系列的结尾处增加新事件。新事件的开始时间由self.currentTime定义。
        pos定义了事件发生的位置；eventType定义了事件的类型，0、1、2分别表示"MouseDown", "MouseMove", "MouseUp"。
        """
        self.events.append(
            {
                "Timestamp": self.currentTime,
                "X": pos[0],
                "Y": pos[1],
                "Delta": 0,
                "EventType": allEvents[eventType]
            }
        )
    def initialize(self):
        """
        初始化Mission
        """
        self.events = [] #self.events中存储了此Mission的事件系列。
        self.currentTime = 0 #self.currentTime定义了添加新事件时新事件的开始时间。

    def generateJson(self, name, shortCut):
        """
        根据已有的events生成json。
        name表示生成的json的文件名。
        shortCut是键盘上的一个按键，生成并导入json后按[ctrl+alt+对应的按键]即可快捷地激活脚本。
        """
        js = {
            "TimeCreated": time.strftime("%Y%m%dT%H%M%S", time.localtime()),
            "Name": name,
            "Events": self.events,
            "LoopType": "UntilStopped",
            "LoopNumber": 1,
            "LoopTime": 0,
            "LoopInterval": 0,
            "Acceleration": 1.0,
            "PlayOnStart": False,
            "RestartPlayer": False,
            "RestartPlayerAfterMinutes": 60,
            "ShortCut": shortCut
        }
        j = json.dumps(js, indent=4, separators=(',', ': '))
        try:
            a = open("output\\" + name + ".json", "w")
        except FileNotFoundError:
            makedirs("output")
            a = open("output\\" + name + ".json", "w")
        a.write(j)
        return j

    def export(self, funcName, *args, **kwargs):
        """
        可以从外部调用的快捷生成json的接口。
        funcName是定义了需要导出的事件系列的函数的函数名；*args和**kwargs是需要传到这个函数中的参数。
        """
        func = getattr(self, funcName)
        func(*args, **kwargs)
        retValue = self.generateJson(exportConfiguration[funcName]["name"], exportConfiguration[funcName]["shortCut"])
        self.initialize()
        return retValue






####################################################################################################
#
#   以下是Mission类中定义的事件系列。你也可以在此处自定义你的事件系列，然后添加到exportConfiguration中，
#   并加上对应的名字和快捷键（可选），以生成你自定义的json文件
#
####################################################################################################
    def click(self, pos):
        """
        在pos所在的位置增加一个点击事件
        """
        self.addEvent(pos, 0)
        self.addEvent(pos, 2)
        self.wait(clickInterval)

    def move(self, pos1, pos2):
        """
        添加一个从pos1移动到pos2的移动事件
        """
        self.addEvent(pos1, 0)
        self.wait(moveInterval)
        self.addEvent(pos2, 1)
        self.wait(moveInterval)
        self.addEvent(pos2, 2)
        self.wait(moveInterval)

    def exchangeMove(self, pos1, pos2):
        """
        添加一个从pos1移动到pos2的移动事件
        """
        self.addEvent(pos1, 0)
        self.wait(clickInterval)
        for t in range(moveInterval//5):
            pos = tuple([(i-j)*float(t)/(moveInterval//5)+j for i,j in zip(pos2, pos1)])
            self.addEvent(pos, 1)
            self.wait(5)
        self.addEvent(pos2, 2)
        self.wait(clickInterval)

    
    def wait(self, time):
        """
        在上一个事件结束之后等待time秒
        """
        self.currentTime += time

    def collectCoins(self):
        """
        关闭家国之光弹窗并收集所有建筑的金币
        """
        self.click(pos["otherPos"]["lightPos"])
        self.wait(clickInterval)
        for i in pos["buildingPos"]:
            self.click(i)
            self.wait(clickInterval)

    def autoCollect(self):
        """
        自动收取硬币.
        """
        self.wait(500)            #等待500毫秒
        self.collectCoins()       #新建一个收集硬币事件集

    def upgrade(self, building):
        """
        给编号为building的建筑升级
        """
        bPos = pos["buildingPos"][building]
        self.click(pos["otherPos"]["openUpgrade"])
        self.wait(clickInterval * 3)
        self.click(bPos)
        self.wait(upgradeInterval)
        self.click(pos["otherPos"]["upgrade"])
        self.wait(clickInterval)
        self.click(pos["otherPos"]["openUpgrade"])
        self.wait(upgradeInterval)

    def exchange(self, building, n):
        '''将'编号为building的建筑交换成序列中第n个'''
        bPos = pos["buildingPos"][building]
        self.click(bPos)
        self.wait(upgradeInterval)
        self.click(pos["otherPos"]["openExchange"])
        self.wait(upgradeInterval)
        buildingPos = pos["otherPos"]['exchange']
        if n < 3:
            buildingPos = tuple([i+n*j for i,j in zip(buildingPos, pos["otherPos"]['moveDistence'])])
        else:
            movePos = tuple([i+j for i,j in zip(buildingPos, pos["otherPos"]['exchangeoffset'])])
            for i in range(n-2):
                self.exchangeMove(movePos, buildingPos)
                self.wait(clickInterval)
            buildingPos = tuple([i+2*j for i,j in zip(buildingPos, pos["otherPos"]['moveDistence'])])
        self.click(buildingPos)
        self.wait(upgradeInterval*4)
        self.click(pos["otherPos"]["lightPos"])
        self.wait(clickInterval)

    def collectTrain(self):
        """
        将三个位置的火车货物分别向每个建筑物拖拽一次。
        """
        timer = 0
        for position in pos["trainPos"]:
            for i in pos["buildingPos"]:
                timer += 1
                self.move(position, i)
                self.wait(moveInterval)
                if (timer % collectRateWhileTrain == 0):
                    self.collectCoins()

    def collectTrainYellowOnly(self):
        """
        将三个位置的火车货物分别向epicBudings里编号的每个建筑拖拽一次。
        """
        timer = 0                                       #新建一个计时器，用来插入收集硬币事件集
        for position in pos["trainPos"]:                #对每个火车货物的位置进行循环
            for j, i in enumerate(pos["buildingPos"]):  #对每个建筑的位置进行循环
                if (not self.epicBuildings.count(j)):   #如果对应的位置不是史诗级建筑，跳过
                    continue
                self.move(position, i)    #新建一个从货物位置拖拽到建筑位置的事件
                self.wait(moveInterval)   #等待
                self.move(position, i)    #新建一个从货物位置拖拽到建筑位置的事件
                self.wait(moveInterval)   #等待
    
    def autoUpgrade(self):
        """
        自动收取硬币+自动升级。
        """
        for everybuilding in self.buildingsNeedUpgrade:
            self.collectCoins()
            for i in range(UpdateRateWhileCollect):
                self.wait(500)
                self.collectCoins()
            self.upgrade(everybuilding)

    def autoTrain(self):
        """
        自动收货+自动收取硬币+自动升级。收集所有火车。
        """
        self.collectCoins()
        if (self.buildingsNeedUpgrade == []):
            self.collectTrain()
        else:
            for everybuilding in self.buildingsNeedUpgrade:
                self.upgrade(everybuilding)
                self.collectTrain()

    def autoTrainYellowOnly(self):    
        """
        自动收货+自动收取硬币+自动升级。只收史诗级建筑的火车。
        """
        self.collectCoins()
        if (not self.buildingsNeedUpgrade):
            self.collectTrainYellowOnly()
        else:
            for everybuilding in self.buildingsNeedUpgrade:
                self.upgrade(everybuilding)
                self.collectTrainYellowOnly()
        if (self.exchangeBuildings):
            buildings = [0,1,2,3,4,5,6,7,8]
            exchangedBuildings = [i for i in buildings if not self.epicBuildings.count(i)]
            self.click(pos["otherPos"]["openUpgrade"])
            self.wait(clickInterval)
            for i in range(len(exchangedBuildings)):
                self.exchange(exchangedBuildings[i], 0)
                self.wait(upgradeInterval)
                self.exchange(exchangedBuildings[i], self.exchangeBuildings[i])
                self.wait(upgradeInterval)
            self.click(pos["otherPos"]["openUpgrade"])
            self.wait(clickInterval)




####################################################################################################
#
#   以下是main函数。
#
####################################################################################################

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='输入史诗建筑位置和需要升级的建筑。输出文件在output子目录。\n例："python JiaGuoMeng.py -epicId 0 1 2 3 -lvup 0 1 -all"')
    parser.add_argument('-epicId', metavar='编号', type=int, nargs='+',
                        help='在这个flag后加上你想要接受火车货物的建筑的编号')
    parser.add_argument('-lvup', metavar='编号', type=int, nargs='+',
                        help='在这个flag后加上你要升级建筑的编号')
    parser.add_argument('-list',action='store_true',
                        help="列出所有可以生成的json以及对应的指令")
    parser.add_argument('-all',action='store_true',
                        help="一键生成所有可以生成的json。如果使用此flag，则不需要使用下面的flag。")
    parser.add_argument('-generate',metavar='指令', type=str, nargs='+',
                        help="根据flag后的指令，生成对应的json文件。例：-generate autoCollect autoUpgrade"),
    parser.add_argument('-exchange', metavar='编号', type=int, nargs='+',
                        help='在这个flag后按顺序加上你要交换的各个建筑在交换列表里的编号')
    
    args = parser.parse_args()
    nm = Mission(args.lvup, args.epicId, args.exchange)

    if args.list:
        for i in exportConfiguration:
            print("可输出json文件名：" + exportConfiguration[i]["name"])
            print("介绍：" + ''.join(getattr(Mission, i).__doc__.split()))
            print("对应指令：" + i)
            print()
    elif args.all:
        for i in exportConfiguration:
            nm.export(i)
    elif args.generate:
        for i in args.generate:
            nm.export(i)
    else:
        print("请输入“python JiaGuoMeng.py -h”查看用法。")
        exit()
