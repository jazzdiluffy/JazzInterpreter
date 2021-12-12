
# parsetab.py
# This file is automatically generated. Do not edit.
# pylint: disable=W,C,R
_tabversion = '3.10'

_lr_method = 'LALR'

_lr_signature = 'AND ASSIGN BEGIN BEGINFOR BEGINIF BOOL CBOOL CINT CMBOOL CMINT COMMA CVBOOL CVINT DOUBLE_DOT ELEMENTAL_MUL END ENDFOR ENDIF EQUAL EXIT FALSE FOR FUNCTION GREATER IF INT INT_BINARY INT_DECIMAL LEFT LEFT_BRACKET LEFT_CYCLIC_SHIFT LEFT_FIGURE_BRACKET LESS MATRIX_MUL MBOOL MINT MINUS MOVE NEGATIVE NEW_LINE PLUS RIGHT RIGHT_BRACKET RIGHT_CYCLIC_SHIFT RIGHT_FIGURE_BRACKET SUM TRANSPOSITION TRUE VARIABLE VBOOL VINT WALLprogram : sentence_listsentence_list : sentence_list single_sentence\n                         | single_sentencesingle_sentence : declaration NEW_LINE\n                           | assignment NEW_LINE\n                           | if NEW_LINE\n                           | for NEW_LINEdeclaration : type VARIABLE EQUAL expression\n                       | type VARIABLE EQUAL LEFT_FIGURE_BRACKET list_args RIGHT_FIGURE_BRACKETassignment : variable ASSIGN expressionexpression : math_expression\n                      | variable\n                      | constantmath_expression : expression PLUS expression\n                           | expression MINUS expression\n                           | expression MATRIX_MUL expression\n                           | expression ELEMENTAL_MUL expression\n                           | expression LEFT_CYCLIC_SHIFT\n                           | expression RIGHT_CYCLIC_SHIFT\n                           | expression TRANSPOSITION\n                           | expression LESS expression\n                           | expression GREATER expression\n                           | NEGATIVE expression\n                           | expression AND expressionvariable : VARIABLEtype : int\n                | boolint : INT\n               | CVINT\n               | VINT\n               | CMINT\n               | MINT\n               | CINTbool : BOOL\n                | CMBOOL\n                | MBOOL\n                | CVBOOL\n                | VBOOL\n                | CBOOLconstant : INT_BINARY\n                    | INT_DECIMAL\n                    | TRUE\n                    | FALSElist_args : LEFT_FIGURE_BRACKET list_expressions RIGHT_FIGURE_BRACKET\n                     | list_args COMMA LEFT_FIGURE_BRACKET list_args RIGHT_FIGURE_BRACKET\n                     | list_expressionslist_expressions : list_expressions COMMA expression\n                            | expressionif : IF expression BEGINIF NEW_LINE sentence_list ENDIFfor : FOR VARIABLE EQUAL expression DOUBLE_DOT expression BEGINFOR NEW_LINE sentence_list ENDFOR'
    
_lr_action_items = {'IF':([0,2,3,27,28,29,30,31,61,74,87,89,],[11,11,-3,-2,-4,-5,-6,-7,11,11,11,11,]),'FOR':([0,2,3,27,28,29,30,31,61,74,87,89,],[12,12,-3,-2,-4,-5,-6,-7,12,12,12,12,]),'VARIABLE':([0,2,3,8,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,33,38,44,47,48,49,50,54,55,56,58,60,61,70,74,75,79,83,87,89,],[9,9,-3,32,9,43,-26,-27,-28,-29,-30,-31,-32,-33,-34,-35,-36,-37,-38,-39,-2,-4,-5,-6,-7,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,]),'INT':([0,2,3,27,28,29,30,31,61,74,87,89,],[15,15,-3,-2,-4,-5,-6,-7,15,15,15,15,]),'CVINT':([0,2,3,27,28,29,30,31,61,74,87,89,],[16,16,-3,-2,-4,-5,-6,-7,16,16,16,16,]),'VINT':([0,2,3,27,28,29,30,31,61,74,87,89,],[17,17,-3,-2,-4,-5,-6,-7,17,17,17,17,]),'CMINT':([0,2,3,27,28,29,30,31,61,74,87,89,],[18,18,-3,-2,-4,-5,-6,-7,18,18,18,18,]),'MINT':([0,2,3,27,28,29,30,31,61,74,87,89,],[19,19,-3,-2,-4,-5,-6,-7,19,19,19,19,]),'CINT':([0,2,3,27,28,29,30,31,61,74,87,89,],[20,20,-3,-2,-4,-5,-6,-7,20,20,20,20,]),'BOOL':([0,2,3,27,28,29,30,31,61,74,87,89,],[21,21,-3,-2,-4,-5,-6,-7,21,21,21,21,]),'CMBOOL':([0,2,3,27,28,29,30,31,61,74,87,89,],[22,22,-3,-2,-4,-5,-6,-7,22,22,22,22,]),'MBOOL':([0,2,3,27,28,29,30,31,61,74,87,89,],[23,23,-3,-2,-4,-5,-6,-7,23,23,23,23,]),'CVBOOL':([0,2,3,27,28,29,30,31,61,74,87,89,],[24,24,-3,-2,-4,-5,-6,-7,24,24,24,24,]),'VBOOL':([0,2,3,27,28,29,30,31,61,74,87,89,],[25,25,-3,-2,-4,-5,-6,-7,25,25,25,25,]),'CBOOL':([0,2,3,27,28,29,30,31,61,74,87,89,],[26,26,-3,-2,-4,-5,-6,-7,26,26,26,26,]),'$end':([1,2,3,27,28,29,30,31,],[0,-1,-3,-2,-4,-5,-6,-7,]),'ENDIF':([3,27,28,29,30,31,74,],[-3,-2,-4,-5,-6,-7,80,]),'ENDFOR':([3,27,28,29,30,31,89,],[-3,-2,-4,-5,-6,-7,90,]),'NEW_LINE':([4,5,6,7,9,35,36,37,39,40,41,42,45,46,51,52,53,57,59,62,63,64,65,66,67,68,77,80,85,90,],[28,29,30,31,-25,-11,-12,-13,-40,-41,-42,-43,-10,61,-18,-19,-20,-23,-8,-14,-15,-16,-17,-21,-22,-24,-9,-49,87,-50,]),'ASSIGN':([9,10,],[-25,33,]),'BEGINIF':([9,34,35,36,37,39,40,41,42,51,52,53,57,62,63,64,65,66,67,68,],[-25,46,-11,-12,-13,-40,-41,-42,-43,-18,-19,-20,-23,-14,-15,-16,-17,-21,-22,-24,]),'PLUS':([9,34,35,36,37,39,40,41,42,45,51,52,53,57,59,62,63,64,65,66,67,68,69,73,81,84,],[-25,47,-11,-12,-13,-40,-41,-42,-43,47,-18,-19,-20,47,47,47,47,47,47,47,47,47,47,47,47,47,]),'MINUS':([9,34,35,36,37,39,40,41,42,45,51,52,53,57,59,62,63,64,65,66,67,68,69,73,81,84,],[-25,48,-11,-12,-13,-40,-41,-42,-43,48,-18,-19,-20,48,48,48,48,48,48,48,48,48,48,48,48,48,]),'MATRIX_MUL':([9,34,35,36,37,39,40,41,42,45,51,52,53,57,59,62,63,64,65,66,67,68,69,73,81,84,],[-25,49,-11,-12,-13,-40,-41,-42,-43,49,-18,-19,-20,49,49,49,49,49,49,49,49,49,49,49,49,49,]),'ELEMENTAL_MUL':([9,34,35,36,37,39,40,41,42,45,51,52,53,57,59,62,63,64,65,66,67,68,69,73,81,84,],[-25,50,-11,-12,-13,-40,-41,-42,-43,50,-18,-19,-20,50,50,50,50,50,50,50,50,50,50,50,50,50,]),'LEFT_CYCLIC_SHIFT':([9,34,35,36,37,39,40,41,42,45,51,52,53,57,59,62,63,64,65,66,67,68,69,73,81,84,],[-25,51,-11,-12,-13,-40,-41,-42,-43,51,-18,-19,-20,51,51,51,51,51,51,51,51,51,51,51,51,51,]),'RIGHT_CYCLIC_SHIFT':([9,34,35,36,37,39,40,41,42,45,51,52,53,57,59,62,63,64,65,66,67,68,69,73,81,84,],[-25,52,-11,-12,-13,-40,-41,-42,-43,52,-18,-19,-20,52,52,52,52,52,52,52,52,52,52,52,52,52,]),'TRANSPOSITION':([9,34,35,36,37,39,40,41,42,45,51,52,53,57,59,62,63,64,65,66,67,68,69,73,81,84,],[-25,53,-11,-12,-13,-40,-41,-42,-43,53,-18,-19,-20,53,53,53,53,53,53,53,53,53,53,53,53,53,]),'LESS':([9,34,35,36,37,39,40,41,42,45,51,52,53,57,59,62,63,64,65,66,67,68,69,73,81,84,],[-25,54,-11,-12,-13,-40,-41,-42,-43,54,-18,-19,-20,54,54,54,54,54,54,54,54,54,54,54,54,54,]),'GREATER':([9,34,35,36,37,39,40,41,42,45,51,52,53,57,59,62,63,64,65,66,67,68,69,73,81,84,],[-25,55,-11,-12,-13,-40,-41,-42,-43,55,-18,-19,-20,55,55,55,55,55,55,55,55,55,55,55,55,55,]),'AND':([9,34,35,36,37,39,40,41,42,45,51,52,53,57,59,62,63,64,65,66,67,68,69,73,81,84,],[-25,56,-11,-12,-13,-40,-41,-42,-43,56,-18,-19,-20,56,56,56,56,56,56,56,56,56,56,56,56,56,]),'DOUBLE_DOT':([9,35,36,37,39,40,41,42,51,52,53,57,62,63,64,65,66,67,68,69,],[-25,-11,-12,-13,-40,-41,-42,-43,-18,-19,-20,-23,-14,-15,-16,-17,-21,-22,-24,75,]),'COMMA':([9,35,36,37,39,40,41,42,51,52,53,57,62,63,64,65,66,67,68,71,72,73,76,82,84,86,88,],[-25,-11,-12,-13,-40,-41,-42,-43,-18,-19,-20,-23,-14,-15,-16,-17,-21,-22,-24,78,79,-48,79,-44,-47,78,-45,]),'RIGHT_FIGURE_BRACKET':([9,35,36,37,39,40,41,42,51,52,53,57,62,63,64,65,66,67,68,71,72,73,76,82,84,86,88,],[-25,-11,-12,-13,-40,-41,-42,-43,-18,-19,-20,-23,-14,-15,-16,-17,-21,-22,-24,77,-46,-48,82,-44,-47,88,-45,]),'BEGINFOR':([9,35,36,37,39,40,41,42,51,52,53,57,62,63,64,65,66,67,68,81,],[-25,-11,-12,-13,-40,-41,-42,-43,-18,-19,-20,-23,-14,-15,-16,-17,-21,-22,-24,85,]),'NEGATIVE':([11,33,38,44,47,48,49,50,54,55,56,58,60,70,75,79,83,],[38,38,38,38,38,38,38,38,38,38,38,38,38,38,38,38,38,]),'INT_BINARY':([11,33,38,44,47,48,49,50,54,55,56,58,60,70,75,79,83,],[39,39,39,39,39,39,39,39,39,39,39,39,39,39,39,39,39,]),'INT_DECIMAL':([11,33,38,44,47,48,49,50,54,55,56,58,60,70,75,79,83,],[40,40,40,40,40,40,40,40,40,40,40,40,40,40,40,40,40,]),'TRUE':([11,33,38,44,47,48,49,50,54,55,56,58,60,70,75,79,83,],[41,41,41,41,41,41,41,41,41,41,41,41,41,41,41,41,41,]),'FALSE':([11,33,38,44,47,48,49,50,54,55,56,58,60,70,75,79,83,],[42,42,42,42,42,42,42,42,42,42,42,42,42,42,42,42,42,]),'EQUAL':([32,43,],[44,58,]),'LEFT_FIGURE_BRACKET':([44,60,78,83,],[60,70,83,70,]),}

_lr_action = {}
for _k, _v in _lr_action_items.items():
   for _x,_y in zip(_v[0],_v[1]):
      if not _x in _lr_action:  _lr_action[_x] = {}
      _lr_action[_x][_k] = _y
del _lr_action_items

_lr_goto_items = {'program':([0,],[1,]),'sentence_list':([0,61,87,],[2,74,89,]),'single_sentence':([0,2,61,74,87,89,],[3,27,3,27,3,27,]),'declaration':([0,2,61,74,87,89,],[4,4,4,4,4,4,]),'assignment':([0,2,61,74,87,89,],[5,5,5,5,5,5,]),'if':([0,2,61,74,87,89,],[6,6,6,6,6,6,]),'for':([0,2,61,74,87,89,],[7,7,7,7,7,7,]),'type':([0,2,61,74,87,89,],[8,8,8,8,8,8,]),'variable':([0,2,11,33,38,44,47,48,49,50,54,55,56,58,60,61,70,74,75,79,83,87,89,],[10,10,36,36,36,36,36,36,36,36,36,36,36,36,36,10,36,10,36,36,36,10,10,]),'int':([0,2,61,74,87,89,],[13,13,13,13,13,13,]),'bool':([0,2,61,74,87,89,],[14,14,14,14,14,14,]),'expression':([11,33,38,44,47,48,49,50,54,55,56,58,60,70,75,79,83,],[34,45,57,59,62,63,64,65,66,67,68,69,73,73,81,84,73,]),'math_expression':([11,33,38,44,47,48,49,50,54,55,56,58,60,70,75,79,83,],[35,35,35,35,35,35,35,35,35,35,35,35,35,35,35,35,35,]),'constant':([11,33,38,44,47,48,49,50,54,55,56,58,60,70,75,79,83,],[37,37,37,37,37,37,37,37,37,37,37,37,37,37,37,37,37,]),'list_args':([60,83,],[71,86,]),'list_expressions':([60,70,83,],[72,76,72,]),}

_lr_goto = {}
for _k, _v in _lr_goto_items.items():
   for _x, _y in zip(_v[0], _v[1]):
       if not _x in _lr_goto: _lr_goto[_x] = {}
       _lr_goto[_x][_k] = _y
del _lr_goto_items
_lr_productions = [
  ("S' -> program","S'",1,None,None,None),
  ('program -> sentence_list','program',1,'p_program','JazzParser.py',15),
  ('sentence_list -> sentence_list single_sentence','sentence_list',2,'p_sentence_list','JazzParser.py',19),
  ('sentence_list -> single_sentence','sentence_list',1,'p_sentence_list','JazzParser.py',20),
  ('single_sentence -> declaration NEW_LINE','single_sentence',2,'p_single_sentence','JazzParser.py',27),
  ('single_sentence -> assignment NEW_LINE','single_sentence',2,'p_single_sentence','JazzParser.py',28),
  ('single_sentence -> if NEW_LINE','single_sentence',2,'p_single_sentence','JazzParser.py',29),
  ('single_sentence -> for NEW_LINE','single_sentence',2,'p_single_sentence','JazzParser.py',30),
  ('declaration -> type VARIABLE EQUAL expression','declaration',4,'p_declaration','JazzParser.py',34),
  ('declaration -> type VARIABLE EQUAL LEFT_FIGURE_BRACKET list_args RIGHT_FIGURE_BRACKET','declaration',6,'p_declaration','JazzParser.py',35),
  ('assignment -> variable ASSIGN expression','assignment',3,'p_assignment','JazzParser.py',44),
  ('expression -> math_expression','expression',1,'p_expression','JazzParser.py',49),
  ('expression -> variable','expression',1,'p_expression','JazzParser.py',50),
  ('expression -> constant','expression',1,'p_expression','JazzParser.py',51),
  ('math_expression -> expression PLUS expression','math_expression',3,'p_math_expression','JazzParser.py',55),
  ('math_expression -> expression MINUS expression','math_expression',3,'p_math_expression','JazzParser.py',56),
  ('math_expression -> expression MATRIX_MUL expression','math_expression',3,'p_math_expression','JazzParser.py',57),
  ('math_expression -> expression ELEMENTAL_MUL expression','math_expression',3,'p_math_expression','JazzParser.py',58),
  ('math_expression -> expression LEFT_CYCLIC_SHIFT','math_expression',2,'p_math_expression','JazzParser.py',59),
  ('math_expression -> expression RIGHT_CYCLIC_SHIFT','math_expression',2,'p_math_expression','JazzParser.py',60),
  ('math_expression -> expression TRANSPOSITION','math_expression',2,'p_math_expression','JazzParser.py',61),
  ('math_expression -> expression LESS expression','math_expression',3,'p_math_expression','JazzParser.py',62),
  ('math_expression -> expression GREATER expression','math_expression',3,'p_math_expression','JazzParser.py',63),
  ('math_expression -> NEGATIVE expression','math_expression',2,'p_math_expression','JazzParser.py',64),
  ('math_expression -> expression AND expression','math_expression',3,'p_math_expression','JazzParser.py',65),
  ('variable -> VARIABLE','variable',1,'p_variable','JazzParser.py',70),
  ('type -> int','type',1,'p_type','JazzParser.py',74),
  ('type -> bool','type',1,'p_type','JazzParser.py',75),
  ('int -> INT','int',1,'p_int','JazzParser.py',79),
  ('int -> CVINT','int',1,'p_int','JazzParser.py',80),
  ('int -> VINT','int',1,'p_int','JazzParser.py',81),
  ('int -> CMINT','int',1,'p_int','JazzParser.py',82),
  ('int -> MINT','int',1,'p_int','JazzParser.py',83),
  ('int -> CINT','int',1,'p_int','JazzParser.py',84),
  ('bool -> BOOL','bool',1,'p_bool','JazzParser.py',88),
  ('bool -> CMBOOL','bool',1,'p_bool','JazzParser.py',89),
  ('bool -> MBOOL','bool',1,'p_bool','JazzParser.py',90),
  ('bool -> CVBOOL','bool',1,'p_bool','JazzParser.py',91),
  ('bool -> VBOOL','bool',1,'p_bool','JazzParser.py',92),
  ('bool -> CBOOL','bool',1,'p_bool','JazzParser.py',93),
  ('constant -> INT_BINARY','constant',1,'p_constant','JazzParser.py',97),
  ('constant -> INT_DECIMAL','constant',1,'p_constant','JazzParser.py',98),
  ('constant -> TRUE','constant',1,'p_constant','JazzParser.py',99),
  ('constant -> FALSE','constant',1,'p_constant','JazzParser.py',100),
  ('list_args -> LEFT_FIGURE_BRACKET list_expressions RIGHT_FIGURE_BRACKET','list_args',3,'p_list_args','JazzParser.py',104),
  ('list_args -> list_args COMMA LEFT_FIGURE_BRACKET list_args RIGHT_FIGURE_BRACKET','list_args',5,'p_list_args','JazzParser.py',105),
  ('list_args -> list_expressions','list_args',1,'p_list_args','JazzParser.py',106),
  ('list_expressions -> list_expressions COMMA expression','list_expressions',3,'p_list_expressions','JazzParser.py',115),
  ('list_expressions -> expression','list_expressions',1,'p_list_expressions','JazzParser.py',116),
  ('if -> IF expression BEGINIF NEW_LINE sentence_list ENDIF','if',6,'p_if','JazzParser.py',123),
  ('for -> FOR VARIABLE EQUAL expression DOUBLE_DOT expression BEGINFOR NEW_LINE sentence_list ENDFOR','for',10,'p_for','JazzParser.py',129),
]