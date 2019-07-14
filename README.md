# Pyskl
 python automatic work  tool

python编写的自动化工具。可用于手游自动点击、自动工作等。

```Python
titlename = u"天天模拟器 1.3.1044"
#获取句柄
hwnd = win32gui.FindWindow(None, titlename)
#获取窗口左上角和右下角坐标
left, top, right, bottom = win32gui.GetWindowRect(hwnd)
print left,top,right-left,bottom-top
```
