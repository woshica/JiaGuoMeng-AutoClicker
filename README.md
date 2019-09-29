# JiaGuoMeng-AutoClick
用来生成游戏《家国梦》的自动点击脚本的Python代码。生成的.json格式的脚本文件可以用于BlueStacks安卓模拟器中。
生成的脚本可以实现：自动将火车上的史诗级货物拖拽到对应的建筑物上，同时每秒收集一次金币，同时每隔一段时间升级由玩家指定的一个或几个建筑。你也可以通过修改py文件，轻松地实现自定义脚本的功能。
## 用法
1. 下载并安装python3，链接https://www.python.org/getit/，并确保python被添加到了系统的path路径中
2. 在根目录下打开cmd或者其它命令行，先运行
`python JiaGuoMeng.py -h`
阅读帮助信息后根据个人需求进行参数调整。json输出文件在output子目录。
3. 下载并安装蓝叠模拟器国际版，链接https://www.bluestacks.com/
4. 在模拟其中安装《家国梦》，按Ctrl+Shift+7，呼出脚本录制器
5. 点击输入，导入之前生成的json脚本
6. 点击运行，解放双手
## 关于建筑位置编号
命令行中的建筑位置编号为

|左|中|右|
|---|---|---|
|6|7|8| 
|3|4|5| 
|0|1|2|
其中，第一行是工业建筑，
## JiaGuoMeng.py详解
- 此py文件主要提供了一个Mission类，以及其对应的接口。
- Mission类定义了一系列的事件，同时提供了一些便捷的添加事件的方法。
- 通过更改文件最开始的buildingsNeedUpgrade（需要升级的建筑）以及pos["yellowPos"]（史诗级建筑的位置），就可以轻松地根据你的情况生成对应的脚本。所有的建筑按从下到上、从左到右的顺序，按0~8编号。比如，如果想要升级右下角和右上角的建筑，则应将buildingsNeedUpgrade设置为[2, 8]；如果只有中间和上方中间的建筑是史诗级建筑，则应将epicBuildings设置为[4, 7]。
- 程序默认会生成四个json文件，对应了四种情况：
   1. 只收硬币
   2. 收硬币，同时过一段时间升级一次
   3. 在2的基础上收火车的货物
   4. 在3的基础上只收史诗级的火车货物
## 注意事项
- 运行脚本对模拟器的分辨率没有要求，运行脚本时可以随意设置模拟器的分辨率、将模拟器最小化等等。
- 蓝叠模拟器需要使用国际版，国内的版本中好像没有脚本编辑器功能。
