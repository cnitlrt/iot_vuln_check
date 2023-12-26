# 环境搭建

## Windows

BinaryNinja的安装包

下载地址：https://www.yunzhongzhuan.com/#sharefile=eYWM4QpQ_63294

解压密码：`www.ddosi.org`

在`\BinaryNinja\scripts`，运行

```
python3 install_api.py
```

建议虚拟环境

```
python3 install_api.py -v
```





官方API文档：https://api.binary.ninja/

示例：打开一个二进制文件并显示所有函数

```python
from binaryninja import *

if __name__ == "__main__":
    bv = BinaryViewType.get_view_of_file("./command_inject")
    bv.update_analysis()
    for func in bv.functions:
        print(func.symbol.name)
```



# 参考

https://docs.binary.ninja/getting-started.html#linux

https://www.ddosi.org/binary-ninja/#Binary_Ninja%E7%A0%B4%E8%A7%A3%E7%89%88%E4%B8%8B%E8%BD%BD%E5%9C%B0%E5%9D%80winlinuxLicense




test123
