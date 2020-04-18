# GPA-Calculator
一款基于正方教务系统的GPA计算器，带有图形界面

## 它是什么
该项目是使用Python3语言，在Windows10环境下编写的，一款具有图形界面的GPA（平均学分绩点）计算器。其数据来源依托于正方教务管理系统，适用于绝大多数的使用正方系统的学校。

## 依赖
* 开发语言：Python3（开发环境为Python3.7）
* 操作系统：Windows10（理论上经过少量修改Linux等系统也应该能使用）
* 依赖
  * [numpy](https://github.com/numpy/numpy)
  * [retry](https://github.com/invl/retry)
  * [School_Api](https://github.com/dairoot/school-api)

非常感谢你们伟大的工作！！非常感谢！！

## 如何使用
首先，在确保已经安装Python3的情况下，安装相应的依赖，使用命令
```
pip install -r requirements.txt
```
如果你的默认Python版本不是3的话，你应该使用`pip3`代替`pip`。

然后请配置config.json（配置文件）。其格式如下：
```json
{
  "jwxt_url": "你的教务系统网址",
  "username": "你的用户名（如：学号）",
  "password": "你的教务系统密码",
  "Free_Electives": ["任选课1", "任选课2", "任选课3"]
}
```
按照上面的格式填写即可。其中，"Free_Electives"项代表“任选课”。任选课一般是不算GPA的。将任选课的课程名称**准确地**填写在"Free_Electives"项里（不要更改格式！），即可在后续的GPA计算中略过所列的任选课。

**要说明的是**，GPA的计算方法这里采用的是5绩满绩制。即：5.0为满绩，对应100分。1.0对应60分。60分以上，每提高一分绩点对应增加0.1。**有些学校并没有采用这种计算方法，因此请自行修改实现Main.py中的calculate方法。**

之后，只需要运行Main.py即可
```
python Main.py
```
类似地，使用`python3`代替`python`如果你的默认Python版本不是3的话。

之后，尽情享受吧。

![GPA Calculator Demo](https://gitee.com/pragmatism/GPA-Calculator/raw/master/demo.png)

* 双击表格中的项会弹出修改输入框
* 红色斜体字代表任选课（不算绩点）
* 点击“添加课程”可以新添加课程，双击修改表格项的值
* 单机表格表头栏可以使得表格按该列排序（支持双向排序）

如果你想写一个批处理脚本，你可以像下面这样轻易实现：
```bat
@echo off
python somedir/Main.py
pause
```
（类似地，使用`python3`代替`python`如果你的默认Python版本不是3的话。）之后，将其保存为“GPA计算器.bat”。这样，当你下次想要运行项目时，只需双击这个批处理脚本即可。

## 它是如何工作的
GUI是使用Python自带的tkinter实现的。我尽可能地使用Python的原生库，而少引用其他的依赖。项目通过[School-Api](https://github.com/dairoot/school-api)获取正方系统的成绩，然后调用calculate方法计算GPA，最后展示在GUI上。

很明显，这里最困难的部分是GUI的实现。从灰白相间的背景色，到字体的不同展示（如任选课的字体为红色斜体），再到双击修改、排序的实现、弹窗的合理实现等，我查阅了大量的资料，这一过程真的使我收获良多。最终的GUI效果我还是很满意的，很具有用户友好性。

而相比较的，GPA的计算算法反而是最简单的部分了。

## 作者
一个学生，一个宅男。

一个Kizuner，一个[春日望(twitter@kasuga_nozomi)](https://twitter.com/kasuga_nozomi)的死忠粉。

* **联系方式**
  * 电子邮件: pragmatism0220@gmail.com
  * 微博: [@保護者_Pragmatism0220](https://weibo.com/u/7341561133)
  * 推特: [@Pragmatism_0220](https://twitter.com/Pragmatism_0220)

## 开源许可证
[Mozilla Public License 2.0](https://github.com/Pragmatism0220/GPA-Calculator/blob/master/LICENSE)
