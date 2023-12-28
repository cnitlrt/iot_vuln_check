# 字符串格式化漏洞

`fast_trans\method.py`
```python
class FormatUnconstant(Searcher):

    def __init__(self, func: Checker) -> None:
        super().__init__()
        self.function = func
    
    def burptal_search(self, checkerlist: list):
        if checkerlist == None:
            for refer in self.function.arg_xrefs:
                vulned(SuccessType.FORMAT_UNCONSTANT,"possible",
                    self.function.symbol,hex(refer),
                    self.function.bv.get_functions_containing(refer)[0])
        else:
            for checker in checkerlist:
                for refer in checker.arg_xrefs:
                    vulned(SuccessType.FORMAT_UNCONSTANT,"possible",
                    self.function.symbol,hex(refer),
                    self.function.bv.get_functions_containing(refer)[0])
```
符合漏洞的定义都在各个函数对应的Checker函数中
如果传递了一系列的函数，那么输出所有函数对应的疑似漏洞点

这里只要参数不为变量就可，算是简单的

测试用例`testcase\format_constant.py`
