# JiaGuoMeng-AutoClick
用来生成游戏《家国梦》的自动点击脚本的Python代码。生成的.json格式的脚本文件可以用于BlueStacks安卓模拟器中。
生成的脚本可以实现：自动将火车上的史诗级货物拖拽到对应的建筑物上，同时每秒收集一次金币，同时每隔一段时间升级由玩家指定的一个或几个建筑。你也可以通过修改py文件，轻松地实现自定义脚本的功能。
## 用法
0. 点击页面右上方的绿色“Clone or download”按钮，选择Download Zip，下载zip包并解压。
1. 下载并安装python3，链接https://www.python.org/getit/
，并确保python被添加到了系统的path路径中
2. 在根目录下（打开解压zip后生成的文件夹）打开cmd或者其它命令行，先运行
`python JiaGuoMeng.py -h`
阅读帮助信息后根据个人需求进行参数调整。json输出文件在output子目录。
3. 下载并安装蓝叠模拟器国际版，仓库根目录下的BlueStacksInstaller.exe是从官网上下载的蓝叠国际版安装器，官网链接为https://www.bluestacks.com/
4. 在模拟其中安装《家国梦》，按Ctrl+Shift+7，呼出脚本录制器
5. 点击输入，导入之前生成的json脚本
6. 点击运行，解放双手
## 关于建筑位置编号
命令行中的建筑位置编号对应的游戏中的建筑位置为

|左|中|右|
|---|---|---|
|6|7|8| 
|3|4|5| 
|0|1|2|

其中，第一行是工业建筑，第二行是商业建筑，第三行是住宅。
## 关于只收橙色时自动切换建筑
该项为可选项（不推荐）
目的为将非橙色建筑泳列表里的第一个替换后再替换回来，可以起到刷新火车的作用，可以提高效率(?)
列表里的编号也从0开始
使用此方法多次刷新后可能会造成不在发车的问题
## 注意事项
- 运行脚本对模拟器的分辨率没有要求，运行脚本时可以随意设置模拟器的分辨率、将模拟器最小化等等。
- 蓝叠模拟器需要使用国际版，国内的版本中好像没有脚本编辑器功能。
- 如果在运行脚本时发现无法正常升级建筑、建筑坐标不正确等问题，可以修改python文件中最开始定义的一系列参数，如upgradeInterval（定义了升级建筑时点击事件间需要等待的时间），buildingPos（定义了建筑坐标）等。
