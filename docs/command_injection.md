# 命令注入检测

`fast_trans\base.py`
```python
class Searcher(object):
    def __init__(self,) -> None:
        self.path=[]

    def get_cross(self, dictA: dict, dictB: dict):
        keys = []
        for va in dictA:
            for vb in dictB:
                if dictA[va].value == dictB[vb].value:
                    keys.append({va:dictA[va], vb:dictB[vb]})
        return keys
    
    def get_result(self):
        for path in self.path:
            vulned(SuccessType.COMMANDINJECT, hex(list(path.keys())[0]),"--->",hex(list(path.keys())[1]),"  same var:", hex(list(path.values())[0].value))
```
这是一个搜索方法类，`get_cross`方法对两个字典查找值相同的关键字

- 两个字典大致为 `{函数被引用地址: 引用时的参数值}`

- 如果 函数A被引用地址的参数值==函数B被引用地址的参数值，
那么认为二者就有一条能达到的调用路线，仍需要人工验证


`fast_trans\method.py`
```python
class CommandInject(Searcher):

    def __init__(self, funcs: list) -> None:
        super().__init__()
        self.funcs=funcs

    def burptal_search(self):
        for checker in self.funcs:
            for refer in checker.arg_xrefs:
                vulned(SuccessType.COMMANDINJECT,"possible",checker.symbol,hex(refer),checker.bv.get_functions_containing(refer)[0])
```
继承自`fast_trans.base`中的`Searcher`

`burptal_search`：

- 找出所有符合在`funcs： list<Checker>`中的所有引用

- 使用方法见`testcase\injection_test.py`

**仍然存在的问题**

要增强对函数参数的引用判定，例如通过在对变量赋值的位置判断变量类型(函数参数、栈上等)、是否可控等

加强判断过后可以降低误判率和找到更复杂的调用路径，减少人工分析的工作量