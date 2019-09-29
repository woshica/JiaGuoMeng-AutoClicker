import json, time

epicBuildings = [2, 5, 6, 7]                        #定义了史诗级建筑的存在情况。在当前情况下，工业区的三个建筑是史诗级的。
buildingsNeedUpgrade = [8]                          #定义了需要升级的建筑（可以有多个）



moveInterval = 150                                  #定义了鼠标移动时各个事件间需要等待的时间（毫秒）
clickInterval = 20                                  #定义了两次鼠标点击事件间需要等待的时间
upgradeInterval = 300                               #定义了升级建筑时点击事件间需要等待的时间
initialTime = 500                                   #定义了脚本在初始时需要等待的时间
allEvents = ["MouseDown", "MouseMove", "MouseUp"]   #定义了各个事件的名称
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
            "upgrade" : (78.18, 89.43)
        }
}

class Mission():
    '''
    Mission类定义了一系列的事件，同时提供了一些便捷的添加事件的方法。
    '''
    def __init__(self, *others):
        self.events = [] #self.events中存储了此Mission的事件系列。
        self.currentTime = 0 #self.currentTime定义了添加新事件时新事件的开始时间。
    
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

    def click(self, pos):
        '''在pos所在的位置增加一个点击事件'''
        self.addEvent(pos, 0)
        self.addEvent(pos, 2)
        self.wait(clickInterval)

    def move(self, pos1, pos2):
        '''添加一个从pos1移动到pos2的移动事件'''
        self.addEvent(pos1, 0)
        self.wait(moveInterval)
        self.addEvent(pos2, 1)
        self.wait(moveInterval)
        self.addEvent(pos2, 2)
        self.wait(moveInterval)

    
    def wait(self, time):
        '''在上一个事件结束之后等待time秒'''
        self.currentTime += time

    def collectCoins(self):
        '''收集所有建筑的金币'''
        for i in pos["buildingPos"]:
            self.click(i)
            self.wait(clickInterval)

    def upgrade(self, building):
        '''给编号为building的建筑升级'''
        bPos = pos["buildingPos"][building]
        self.click(pos["otherPos"]["openUpgrade"])
        self.wait(clickInterval)
        self.click(bPos)
        self.wait(upgradeInterval)
        self.click(pos["otherPos"]["upgrade"])
        self.wait(clickInterval)
        self.click(pos["otherPos"]["openUpgrade"])
        self.wait(upgradeInterval)

    def generateJson(self, name, shortCut):
        '''
        根据已有的events生成json。
        name表示生成的json的文件名。
        shortCut是键盘上的一个按键，生成并导入json后按[ctrl+alt+对应的按键]即可快捷地激活脚本。
        '''
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
        print(j)
        a = open("output\\" + name + ".json", "w")
        a.write(j)

#以下是一些已经实现的json生成流程。

def autoCollect():
    """
    自动收取硬币.
    """
    newMission = Mission()          #新建一个Mission对象
    newMission.wait(500)            #等待500毫秒
    newMission.collectCoins()       #新建一个收集硬币事件集
    j = newMission.generateJson("自动收取硬币", "S")     #生成json文件
    return j

def autoUpgrade(upgradeBuildings = buildingsNeedUpgrade):
    """
    自动收取硬币+自动升级。
    upgradeBuildings中的参数是需要升级的建筑，可以填写多个。
    """
    newMission = Mission()
    for everybuilding in upgradeBuildings:
        newMission.collectCoins()
        for i in range(10):
            newMission.wait(500)
            newMission.collectCoins()
        newMission.upgrade(everybuilding)
    j = newMission.generateJson("自动升级建筑", "U")
    return j

def autoTrain(upgradeBuildings = buildingsNeedUpgrade):
    """
    自动收货+自动收取硬币+自动升级。收集所有火车。
    upgradeBuildings中的参数是需要升级的建筑，可以填写多个。
    """
    newMission = Mission()
    newMission.collectCoins()
    for everybuilding in upgradeBuildings:
        newMission.upgrade(everybuilding)
        timer = 0
        for position in pos["trainPos"]:
            for i in pos["buildingPos"]:
                timer += 1
                newMission.move(position, i)
                newMission.wait(moveInterval)
                if (timer % 2 == 0):
                    newMission.collectCoins()
    j = newMission.generateJson("自动火车发货", "T")
    return j

def autoTrainYellowOnly(upgradeBuildings = buildingsNeedUpgrade):
    """
    自动收货+自动收取硬币+自动升级。只收史诗级建筑的火车。
    upgradeBuildings中的参数是需要升级的建筑，可以填写多个。
    """
    newMission = Mission()                      #新建一个Mission类的对象
    newMission.collectCoins()                   #新建一个收集硬币事件集。
    for everybuilding in upgradeBuildings:      #根据需要升级的建筑循环
        newMission.upgrade(everybuilding)   #新建一个升级对应建筑的事件集
        timer = 0                               #新建一个计时器，用来插入收集硬币事件集
        for position in pos["trainPos"]:        #对每个火车货物的位置进行循环
            for j, i in enumerate(pos["buildingPos"]):  #对每个建筑的位置进行循环
                if (not pos["yellowPos"].count(j)):   #如果对应的位置不是史诗级建筑，跳过
                    continue
                newMission.move(position, i)    #新建一个从货物位置拖拽到建筑位置的事件
                newMission.wait(moveInterval)   #等待

                timer += 1                      #每拖拽两次，增加一个收集硬币事件
                if (timer % 2 == 0):            
                    newMission.collectCoins()

    j = newMission.generateJson("自动火车发货(仅黄色)", "Y")
    return j


if __name__ == '__main__':
    autoTrainYellowOnly()
    autoTrain()
    autoCollect()
    autoUpgrade()
