import re
from typing import List, Tuple, Optional

import util
from mcfunc import Function
from util import Mappings

def verify_args(param_string: str, args: list):
   type_lookup = {
      float: "F",
      str: "S"
   }

   if len(param_string) != len(args): return False
   params = [c for c in param_string]
   for i in range(len(args)):
      if len(params) == 0: return False
      if params[0] != type_lookup[type(args[i])]: return False
      params.pop(0)
   if len(params) == 0: return True
   else: return False


def translate_global(function: str, args: list, mappings: dict or Mappings) -> Tuple[bool, Optional[str]]:
   if type(mappings) == Mappings: mappings = mappings.to_dict()
   global_functions = util.get_all(mappings, "owner", "Global")
   function_pattern = re.compile(fr'(^{function}\([^)]*\)(\w*))')
   translatable = None
   types = None
   for func in global_functions:
      for match in re.finditer(function_pattern, func.get("subcommand")):
         types = match.group(2)
         translatable = func.get("translatable")
         break
   if translatable:
      args_valid = verify_args(types, args)
      return args_valid, translatable if args_valid else None
   else:
      return False, None

def generate(filename: str, mappings: dict or Mappings) -> List[Function]:
   functions = []
   file_string = ""
   with open(filename, "r") as file:
      file_string = file.read()

   pattern = re.compile(
      r"def\s+(\w+)\s*\(([^)]*)\)\s*{(.*?)}",
      re.DOTALL
   )

   for huge_match in pattern.finditer(file_string):
      name = huge_match.group(1)
      param_str = huge_match.group(2).strip()
      body = huge_match.group(3).strip()

      # Extract parameters (comma-separated)
      params = [p.strip() for p in param_str.split(",") if p.strip()] if param_str else []

      # Split the body into individual non-empty lines, stripping each
      lines = [line.strip() for line in body.splitlines() if line.strip()]
      commands = []
      variables = {}

      # variable_pattern = re.compile(r'\s*let\s+(\w+)\s*=\s*(?:"([^"]*)"|(\d+(?:\.\d+)?));')
      variable_pattern = re.compile(r'\s*let\s+(\w+)\s*=\s*(?:"([^"]*)"|(-?\d+(?:\.\d+)?));')
      global_func_pattern = re.compile(r'^(\s*\w+)\(([\w,\s*]*)\);')

      fb = False
      for line in lines:
         if fb:
            break
         for match in variable_pattern.finditer(line):
            key = match.group(1)
            value = match.group(2) if match.group(2) is not None else match.group(3)
            try:
               variables[key] = float(value)
            except ValueError:
               variables[key] = value.strip()

         for match in global_func_pattern.finditer(line):
            func_name = match.group(1)
            args = (match.group(2) if match.group(2) is not None else match.group(3)).split(", ")
            args = [variables[i] if variables.keys().__contains__(i) else i for i in args]
            func_result = translate_global(func_name, args, mappings)
            if func_result[0]:
               commands.append(util.string_format(func_result[1], args))
            else:
               fb = True
               break

      functions.append(Function(name, commands, True))

   return functions