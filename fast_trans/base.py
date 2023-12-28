from binaryninja import *
from rprint import *
import networkx as nx
import matplotlib.pyplot as plt


#函数检查基本类
class Checker(object):
    def __init__(self,
                 prog_bv: BinaryView,
                 func: str,     #函数名称
                 args=1,        #需要的参数个数
                 ) -> None:
        self.bv = prog_bv
        self.symbol = func
        self.function = self.get_func_byname()
        if self.function:
            self.address = self.function.start
        else:
            self.address = None

        # self.ref = self.bv.get_code_refs(self.address)
        self.args = args
        self.arg_xrefs = {}
        if self.address !=None:
            self.get_dict()
        self.parent_call = []
        self.get_parent_func()
        # self.G = nx.DiGraph()
        # self.G.add_node(hex(self.address))
        # self.create_basic_block_graph(self.address)

    def get_func_byname(self):
        for func in self.bv.functions:
            if func.symbol.name == self.symbol:
                return func
        return None

    def get_function_addr(self):
        syms = []
        if self.symbol in self.bv.symbols:
            syms = self.bv.symbols[self.symbol]
        for i in syms:
            if "mips32" == self.bv.arch.name or "mipsel32" == self.bv.arch.name:
                if i.type == SymbolType.ImportAddressSymbol:
                                return i.address
            else:
                if i.type == SymbolType.ImportedFunctionSymbol:
                    return i.address
        return None
    
    def is_constant(self, a):
        return a.type == RegisterValueType.ConstantPointerValue or a.type == RegisterValueType.ConstantValue

    def get_dict(self):         #重载该函数实现分类  
        if self.address == None:
            return
        for ref in self.bv.get_code_refs(self.address):
            func = ref.function
            temp_arg = []       #get_var_uses
            for i in range(self.args):
                temp_arg.append(func.get_parameter_at(ref.address,None,i))
            self.arg_xrefs.update({ref.address:temp_arg})

    def get_parent_func(self):
        for addr in self.arg_xrefs.keys():
            self.parent_call.append(self.bv.get_functions_containing(addr)[0])
        # for func in self.parent_call:
        #     info(func)

    def create_basic_block_graph(self, func_addr: int):
        for refer in self.arg_xrefs.keys():
            self.G.add_node(hex(refer))
            self.G.add_edge(hex(func_addr), hex(refer))

    def visualize_basic_block_graph(self):
        pos = nx.spring_layout(self.G)
        nx.draw(self.G, pos, with_labels=True, font_weight='bold', node_size=700, node_color="skyblue")
        plt.show()


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
        
class CommandInjectChecker(object):
    def __init__(self, Checkers=[]) -> None:
        pass
