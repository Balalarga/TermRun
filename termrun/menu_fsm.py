import os
from pathlib import Path
from typing import List, Tuple

import invoke
from rich import print
import termrun


class BaseRunnerMenuFsm:
    def __init__(self):
        self.nodes = [self.create_runnable_menu_model()]
        self.pwd: List[str] = [""]

    def create_runnable_menu_model(self):
        paths = []
        for func_info in termrun.runnable_funcs_registry:
            paths.append(
                (func_info.path_from_pwd / func_info.get_func_module_name(), func_info)
            )
        tree = self.create_file_tree(paths)
        return tree

    @staticmethod
    def create_file_tree(paths: List[Tuple[Path, termrun.RunnableFunctionInfo]]):
        tree = {}
        for path, func in paths:
            current_level = tree
            for i, part in enumerate(path.parts):
                if part not in current_level:
                    current_level[part] = [] if i == len(path.parts) - 1 else {}
                current_level = current_level[part]
            current_level.append(func)
        return tree

    def draw(self) -> bool:
        return False

    def select(self, node) -> bool:
        pass

    def execute(self):
        pass

    def draw_help(self, idx):
        pass

    def draw_pwd(self):
        pass


class CliMenu(BaseRunnerMenuFsm):
    def draw(self):
        os.system("cls" if os.name == "nt" else "clear")
        self.draw_pwd()

        if not self.select(self.nodes[-1]):
            print("[red]\nInvalid choice!!!\n[/red]")
            input("Press any key to continue...")

        if len(self.nodes) == 0:
            return False

        if type(self.nodes[-1]) is termrun.RunnableFunctionInfo:
            self.execute()

        return True

    @staticmethod
    def is_leaf(node):
        return type(node) is list

    def select(self, node):
        print("0. Return")
        for i, d in enumerate(node if self.is_leaf(node) else list(node.keys())):
            if self.is_leaf(node):
                print(f"{i + 1}. [blue]{d.text}[/blue]")
            else:
                print(f"{i + 1}. {d}")
        try:
            in_str = input("\nSelect number: ")
            in_str = in_str.strip()
            num = int(in_str)
            if num != 0:
                if self.is_leaf(node):
                    self.nodes.append(node[num - 1])
                    self.pwd.append(node[num - 1].text)
                else:
                    self.nodes.append(node[list(node.keys())[num - 1]])
                    self.pwd.append(list(node.keys())[num - 1])
            else:
                self.nodes.pop()
                self.pwd.pop()
            print()
            return True
        except ValueError:
            return False

    def execute(self):
        print("-" * 20, " Execute ", "-" * 20, "\n")
        func: termrun.RunnableFunctionInfo = self.nodes[-1]
        ctx = invoke.Context()
        func.func(ctx)
        self.nodes.pop()
        self.pwd.pop()
        print()
        print("-" * 21, " Done! ", "-" * 21, "\n")
        input("\nPress any key to continue...")

    def draw_help(self, idx):
        node = self.nodes[-1][idx]
        print(node)

    def draw_pwd(self):
        pwd = "/".join(self.pwd)
        print(f"Pwd: {pwd}\n")
