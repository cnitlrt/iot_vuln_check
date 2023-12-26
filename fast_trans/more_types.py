#状态枚举
from enum import Enum, auto


#漏洞类型
class SuccessType(Enum):
    FORMAT_UNCONSTANT   = auto()
    FORMAT_OVERFLOW     = auto()
    STACKOVERFLOW       = auto()
    COMMANDINJECT       = auto()
    COMMANDUNCONSTANT   = auto()
    BUFOVERFLOW         = auto()

# class Error(Enum):
#     FORMAT_UNCONSTANT = auto()
#     FORMAT_OVERFLOW = auto()
#     STACKOVERFLOW = auto()
#     COMMANDINJECT = auto()

#传参类型
class ArgPassType(Enum):
    cdecl       = auto()
        # 参数从右到左依次入栈
        # 由调用者负责清理堆栈
        # 函数返回值通常通过寄存器传递，如EAX
    
    stdcall     = auto()
        # 参数从右到左依次入栈
        # 由被调用者负责清理堆栈
        # 通常用于WinAPI函数
    
    fastcall    = auto()
        # 一些参数通过寄存器传递
        # 其余参数通过堆栈传递
        # 通常用于提高函数调用的性能
    
    msfastcall  = auto()
        # 类似fastcall
        # 但是寄存器的使用方式可能会略有不同
        # 仅在微软编译器上有效
    
    vectorcall  = auto()
        # 主要用于处理SIMD（单指令多数据）指令集
        # 适用于函数参数中包含矢量类型的情况




