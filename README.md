# ExBoard
一个基本图形绘制程序，支持选中，移动，缩放等，完全使用插件式设计，为了能够在这基础上扩展  
> qt(c++)
## 环境  
* python3.6(3.5中dxfreader模块 莫名失效)
## 插件式设计
* 只需把插件（python pkg）放入plugins目录即可（当然需要遵守一些规则，可以参考PaintShape插件的设计）
## 功能
### 基本图形绘制
* 圆，直线，圆弧
### 支持修改
* 包括拖动修改 和直接修改参数
### 支持导入cad文件(仅支持dxf格式)
* 还未集成 参考[dxfReader](https://github.com/XUIgit/dxfReader)
### 缩放，移动
### 多个board
### 选择功能
* 你可选择你绘制的图形，然后在插件中进行操作。删除或者进行其他的操作。
### 撤销，前进功能(还未实现)
## 例
![](https://github.com/XUIgit/ExBoard/raw/master/demo/01.png)
![](https://github.com/XUIgit/ExBoard/raw/master/demo/02.png)
![](https://github.com/XUIgit/ExBoard/raw/master/demo/03.png)
![](https://github.com/XUIgit/ExBoard/raw/master/demo/04.png)
