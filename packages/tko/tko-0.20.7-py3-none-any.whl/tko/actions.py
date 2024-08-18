from typing import List, Optional
import os
import shutil
import subprocess

from .run.wdir import Wdir
from .run.basic import DiffMode, ExecutionResult
from .run.param import Param
from .run.diff import Diff
from .util.sentence import Sentence, Token

from .run.basic import Success
from .run.report import Report
from .util.term_color import term_print
from .util.symbols import symbols

from .run.writer import Writer
from .util.runner import Runner
from .util.freerun import Free
from .cdiff import CDiff
from .execution import Execution
from .game.task import Task
from .play.opener import Opener


class FilterMode:

    @staticmethod
    def deep_copy_and_change_dir():
        # path to ~/.tko_filter
        filter_path = os.path.join(os.path.expanduser("~"), ".tko_filter")

        # verify if filter command is available
        if shutil.which("filter_code") is None:
            print("ERROR: comando de filtragem não encontrado")
            print("Instale o feno com 'pip install feno'")
            exit(1)

        subprocess.run(["filter_code", "-rf", ".", "-o", filter_path])

        os.chdir(filter_path)


class Run:

    def __init__(self, target_list: List[str], exec_cmd: Optional[str], param: Param.Basic):
        self.target_list: List[str] = target_list
        self.exec_cmd: Optional[str] = exec_cmd
        self.param: Param.Basic = param
        self.wdir: Wdir = Wdir()
        self.wdir_builded = False
        self.__curses_mode: bool = False
        self.__first_run = False
        self.__success_mode = Success.RANDOM
        # self.__curses_select_mode = False
        self.__lang = ""
        self.__task: Optional[Task] = None
        self.__opener: Optional[Opener] = None

    def set_curses(self, value:bool=True, success: Success=Success.RANDOM):
        self.__curses_mode = value
        self.__success_mode = success
        return self
   
    def set_lang(self, lang:str):
        self.__lang = lang
        return self
    
    def set_opener(self, opener: Opener):
        self.__opener = opener
        return self

    # def set_curses_select_mode(self, value:bool=True):
    #     self.__curses_select_mode = value
    #     return self
    
    def set_task(self, task: Task):
        self.__task = task
        return self

    def set_first_run(self):
        self.__first_run = True
        return self
    
    def execute(self):
        if not self.wdir_builded:
            self.build_wdir()

        if self.__missing_target():
            return
        if self.__list_mode():
            return
        if self.__free_run():
            return
        self.__diff_mode()
        return

    def __remove_duplicates(self):
        # remove duplicates in target list keeping the order
        self.target_list = list(dict.fromkeys(self.target_list))

    def __change_targets_to_filter_mode(self):
        if self.param.filter:
            old_dir = os.getcwd()

            term_print(Report.centralize(" Entrando no modo de filtragem ", "═"))
            FilterMode.deep_copy_and_change_dir()  
            # search for target outside . dir and redirect target
            new_target_list = []
            for target in self.target_list:
                if ".." in target:
                    new_target_list.append(os.path.normpath(os.path.join(old_dir, target)))
                elif os.path.exists(target):
                    new_target_list.append(target)
            self.target_list = new_target_list

    def __print_top_line(self):
        if self.wdir is None:
            return

        term_print(Sentence().add(symbols.opening).add(self.wdir.resume()), end="")
        term_print(" [", end="")
        first = True
        for unit in self.wdir.get_unit_list():
            if first:
                first = False
            else:
                term_print(" ", end="")
            solver = self.wdir.get_solver()
            if solver is None:
                raise Warning("Solver vazio")
            unit.result = Execution.run_unit(solver, unit)
            term_print(Sentence() + ExecutionResult.get_symbol(unit.result), end="")
        term_print("]")

    def __print_diff(self):
        if self.wdir is None or not self.wdir.has_solver():
            return
        
        if self.param.diff_mode == DiffMode.QUIET:
            return
        
        if self.wdir.get_solver().compile_error:
            term_print(self.wdir.get_solver().error_msg)
            return
        
        results = [unit.result for unit in self.wdir.get_unit_list()]
        if ExecutionResult.EXECUTION_ERROR not in results and ExecutionResult.WRONG_OUTPUT not in results:
            return
        
        if not self.param.compact:
            for elem in self.wdir.unit_list_resume():
                term_print(elem)
        
        if self.param.diff_mode == DiffMode.FIRST:
            # printing only the first wrong case
            wrong = [unit for unit in self.wdir.get_unit_list() if unit.result != ExecutionResult.SUCCESS][0]
            if self.param.is_up_down:
                for line in Diff.mount_up_down_diff(wrong):
                    term_print(line)
            else:
                for line in Diff.mount_side_by_side_diff(wrong):
                    term_print(line)
            return

        if self.param.diff_mode == DiffMode.ALL:
            for unit in self.wdir.get_unit_list():
                if unit.result != ExecutionResult.SUCCESS:
                    if self.param.is_up_down:
                        for line in Diff.mount_up_down_diff(unit):
                            term_print(line)
                    else:
                        for line in Diff.mount_side_by_side_diff(unit):
                            term_print(line)

    def build_wdir(self):
        self.wdir_builded = True
        self.__remove_duplicates()
        self.__change_targets_to_filter_mode()
        try:
            self.wdir = Wdir().set_curses(self.__curses_mode).set_lang(self.__lang).set_target_list(self.target_list).set_cmd(self.exec_cmd).build().filter(self.param)
        except FileNotFoundError as e:
            if self.wdir.has_solver():
                self.wdir.get_solver().error_msg += str(e)
                self.wdir.get_solver().compile_error = True
        return self.wdir

    def __missing_target(self) -> bool:
        if self.wdir is None:
            return False
        if not self.wdir.has_solver() and not self.wdir.has_tests():
            term_print(Sentence().addf("", "fail: ") + "Nenhum arquivo de código ou de teste encontrado.")
            return True
        return False
    
    def __list_mode(self) -> bool:
        if self.wdir is None:
            return False

        # list mode
        if not self.wdir.has_solver() and self.wdir.has_tests():
            term_print(Report.centralize(" Nenhum arquivo de código encontrado. Listando casos de teste.", Token("╌")), flush=True)
            term_print(self.wdir.resume())
            for line in self.wdir.unit_list_resume():
                term_print(line)
            return True
        return False

    def __free_run(self) -> bool:
        if self.wdir is None:
            return False
        if self.wdir.has_solver() and (not self.wdir.has_tests()):
            Free.free_run(self.wdir.get_solver(), show_compilling=False, to_clear=False, wait_input=False)
            return True
        return False

    def __diff_mode(self):
        if self.wdir is None:
            return
        
        if self.__curses_mode:
            cdiff = CDiff(self.wdir, self.param, self.__success_mode)
            if self.__first_run:
                cdiff.set_first_run()
            if self.__task is not None:
                cdiff.set_task(self.__task)
            if self.__opener is not None:
                cdiff.set_opener(self.__opener)
            cdiff.run()
        else:
            term_print(Report.centralize(" Testando o código com os casos de teste ", "═"))
            self.__print_top_line()
            self.__print_diff()


class Build:

    def __init__(self, target_out: str, source_list: List[str], param: Param.Manip, to_force: bool):
        self.target_out = target_out
        self.source_list = source_list
        self.param = param
        self.to_force = to_force

    def execute(self):
        try:
            wdir = Wdir().set_sources(self.source_list).build()
            wdir.manipulate(self.param)
            Writer.save_target(self.target_out, wdir.get_unit_list(), self.to_force)
        except FileNotFoundError as e:
            print(str(e))
            return False
        return True
