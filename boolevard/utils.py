import pyeda
import re
from pyeda.inter import *

pyeda.boolalg.expr.Variable = pyeda.boolalg.expr.ExprVariable
pyeda.boolalg.expr._One = pyeda.boolalg.expr._ExprOne
pyeda.boolalg.expr._Zero = pyeda.boolalg.expr._ExprZero
pyeda.boolalg.expr.Complement = pyeda.boolalg.expr.ExprComplement
pyeda.boolalg.expr.NotOp = pyeda.boolalg.expr.ExprNot
pyeda.boolalg.expr.OrOp = pyeda.boolalg.expr.ExprOr
pyeda.boolalg.expr.AndOp = pyeda.boolalg.expr.ExprAnd

re_ss = re.compile(r"^stablestate:\s*(.*)")
re_equation = re.compile(r"^equation:\s+(.*?)\s*\*")
re_rule = re.compile(r"^equation.*=\s*(.*)")
re_replace_vars = re.compile(r'\b\w+\b')
re_notation = re.compile(r"(\b\w+)(′)")