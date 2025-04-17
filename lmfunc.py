from typing import List

from mcfunc import Function
from util import Mappings
from compiler import compiler
from compiler import parser

def generate(filename: str, mappings: dict or Mappings, debug=False) -> List[Function]:
   return [parse_ast(func.ast, func.name, mappings) for func in compiler.from_file(filename, debug)]


def parse_ast(ast: List[parser.ASTNode], name: str, mappings: dict or Mappings) -> Function:
   lines = []

   

   return Function(name, lines)
