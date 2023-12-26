from binaryninja import *
from rprint import *
import angr

#函数检查基本类
class Checker(object):
    def __init__(self,
                 prog_bv: BinaryView,
                 func: str,     #函数名称
                 args=1,        #需要的参数个数
                 ) -> None:
        self.bv = prog_bv
        self.symbol = func
        self.address = self.get_function_addr()

        self.ref = self.bv.get_code_refs(self.address)
        self.args = args
        self.all_args = {}
        if self.address !=None:
            self.get_dict()

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
        for ref in self.ref:
            func = ref.function
            temp_arg = []
            for i in range(self.args):
                temp_arg.append(func.get_parameter_at(ref.address,None,i))
            self.all_args.update({ref.address:temp_arg})
        
class Searcher(object):
     def __init__(self,
                  binname:str,
                  src_checker,
                  dest_checker
                  ) -> None:
        
        # 创建一个 Angr 项目
        p=angr.Project(binname,auto_load_libs=False)

        state=p.factory.entry_state()
        #state=p.factory.blank_state() #no-initalize
        #state=p.factory.full_init__state() #full-initalize

        simgr=p.factory.simgr(state)

        Find = dest_checker
        Avoid = src_checker

        res=simgr.explore(find = Find)
        if res.found[0]:
            print (res.found[0].posix.dumps(0))

        # project = angr.Project(binary_path, auto_load_libs=False)

        # # 创建一个符号执行状态
        # # state = project.factory.blank_state(addr=src_checker)
        # state = project.factory.entry_state()
        # # 进行动态符号执行
        # simulation = project.factory.simgr(state)
        # simulation.explore(find=dest_checker)

        # # 获取找到的路径
        # if simulation.found:
        #     found_state = simulation.found[0]
        #     print("Found Path:", found_state.posix.dumps(0))



class CommandInjectChecker(object):
    def __init__(self, Checkers=[]) -> None:
        pass


