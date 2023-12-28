from fast_trans.base import *
from fast_trans.functions import *

from fast_trans.more_types import *

class CommandInject(Searcher):

    def __init__(self, funcs: list) -> None:
        super().__init__()
        self.funcs=funcs

    def burptal_search(self):
        for checker in self.funcs:
            for refer in checker.arg_xrefs:
                vulned(SuccessType.COMMANDINJECT,"possible",checker.symbol,hex(refer),checker.bv.get_functions_containing(refer)[0])

class FormatUnconstant(Searcher):

    def __init__(self, func: Checker) -> None:
        super().__init__()
        self.function = func
    
    def burptal_search(self, checkerlist: list=[]):
        if checkerlist == []:
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

