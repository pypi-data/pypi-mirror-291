
# parsetab.py
# This file is automatically generated. Do not edit.
# pylint: disable=W,C,R
_tabversion = '3.10'

_lr_method = 'LALR'

_lr_signature = 'leftORleftANDleftEQUALTONOTEQUALTOleftLESSTHANGREATERTHANLESSTHANEQUALGREATERTHANEQUALleftPLUSMINUSleftTIMESDIVIDEDBYMODULOleftEXPONENTrightUMINUSAND COMMA COMMENT DIVIDEDBY EQUALS EQUALTO EXPONENT FALSE FILENAMEDEC GREATERTHAN GREATERTHANEQUAL LBRACKET LESSTHAN LESSTHANEQUAL LPAREN MINUS MODULO NEWLINE NOTEQUALTO NUMBER OR PLUS PROJECTDEC RBRACKET RPAREN SEMICOLON STRING TIMES TRUE UMINUS VARIABLEprogram : file_declaration variable_list\n               | file_declaration\n               | variable_list\n               | file_declaration : PROJECTDEC STRING SEMICOLON\n                        | PROJECTDEC STRING FILENAMEDEC STRING SEMICOLONvariable_list : variable_dec variable_list\n                     | variable_decvariable_dec : VARIABLE EQUALS expression SEMICOLONexpression : expression PLUS expression\n                  | expression MINUS expression\n                  | expression TIMES expression\n                  | expression DIVIDEDBY expression\n                  | expression MODULO expression\n                  | expression EXPONENT expression\n                  | MINUS expression %prec UMINUS\n                  | LPAREN expression RPAREN\n                  | STRING\n                  | NUMBER\n                  | condition\n                  | listcondition : expression LESSTHAN expression\n                 | expression GREATERTHAN expression\n                 | expression LESSTHANEQUAL expression\n                 | expression GREATERTHANEQUAL expression\n                 | expression EQUALTO expression\n                 | expression NOTEQUALTO expression\n                 | expression AND expression\n                 | expression OR expression\n                 | booleanboolean : TRUE\n               | FALSElist : LBRACKET expression_list RBRACKET\n            | LBRACKET RBRACKETexpression_list : expression\n                       | expression_list COMMA expression'
    
_lr_action_items = {'$end':([0,1,2,3,5,7,9,11,25,45,],[-4,0,-2,-3,-8,-1,-7,-5,-9,-6,]),'PROJECTDEC':([0,],[4,]),'VARIABLE':([0,2,5,11,25,45,],[6,6,6,-5,-9,-6,]),'STRING':([4,10,12,14,15,21,26,27,28,29,30,31,32,33,34,35,36,37,38,39,62,],[8,16,24,16,16,16,16,16,16,16,16,16,16,16,16,16,16,16,16,16,16,]),'EQUALS':([6,],[10,]),'SEMICOLON':([8,13,16,17,18,19,20,22,23,24,40,43,46,47,48,49,50,51,52,53,54,55,56,57,58,59,60,61,],[11,25,-18,-19,-20,-21,-30,-31,-32,45,-16,-34,-10,-11,-12,-13,-14,-15,-22,-23,-24,-25,-26,-27,-28,-29,-17,-33,]),'FILENAMEDEC':([8,],[12,]),'MINUS':([10,13,14,15,16,17,18,19,20,21,22,23,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,41,43,44,46,47,48,49,50,51,52,53,54,55,56,57,58,59,60,61,62,63,],[14,27,14,14,-18,-19,-20,-21,-30,14,-31,-32,14,14,14,14,14,14,14,14,14,14,14,14,14,14,-16,27,-34,27,-10,-11,-12,-13,-14,-15,27,27,27,27,27,27,27,27,-17,-33,14,27,]),'LPAREN':([10,14,15,21,26,27,28,29,30,31,32,33,34,35,36,37,38,39,62,],[15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,]),'NUMBER':([10,14,15,21,26,27,28,29,30,31,32,33,34,35,36,37,38,39,62,],[17,17,17,17,17,17,17,17,17,17,17,17,17,17,17,17,17,17,17,]),'LBRACKET':([10,14,15,21,26,27,28,29,30,31,32,33,34,35,36,37,38,39,62,],[21,21,21,21,21,21,21,21,21,21,21,21,21,21,21,21,21,21,21,]),'TRUE':([10,14,15,21,26,27,28,29,30,31,32,33,34,35,36,37,38,39,62,],[22,22,22,22,22,22,22,22,22,22,22,22,22,22,22,22,22,22,22,]),'FALSE':([10,14,15,21,26,27,28,29,30,31,32,33,34,35,36,37,38,39,62,],[23,23,23,23,23,23,23,23,23,23,23,23,23,23,23,23,23,23,23,]),'PLUS':([13,16,17,18,19,20,22,23,40,41,43,44,46,47,48,49,50,51,52,53,54,55,56,57,58,59,60,61,63,],[26,-18,-19,-20,-21,-30,-31,-32,-16,26,-34,26,-10,-11,-12,-13,-14,-15,26,26,26,26,26,26,26,26,-17,-33,26,]),'TIMES':([13,16,17,18,19,20,22,23,40,41,43,44,46,47,48,49,50,51,52,53,54,55,56,57,58,59,60,61,63,],[28,-18,-19,-20,-21,-30,-31,-32,-16,28,-34,28,28,28,-12,-13,-14,-15,28,28,28,28,28,28,28,28,-17,-33,28,]),'DIVIDEDBY':([13,16,17,18,19,20,22,23,40,41,43,44,46,47,48,49,50,51,52,53,54,55,56,57,58,59,60,61,63,],[29,-18,-19,-20,-21,-30,-31,-32,-16,29,-34,29,29,29,-12,-13,-14,-15,29,29,29,29,29,29,29,29,-17,-33,29,]),'MODULO':([13,16,17,18,19,20,22,23,40,41,43,44,46,47,48,49,50,51,52,53,54,55,56,57,58,59,60,61,63,],[30,-18,-19,-20,-21,-30,-31,-32,-16,30,-34,30,30,30,-12,-13,-14,-15,30,30,30,30,30,30,30,30,-17,-33,30,]),'EXPONENT':([13,16,17,18,19,20,22,23,40,41,43,44,46,47,48,49,50,51,52,53,54,55,56,57,58,59,60,61,63,],[31,-18,-19,-20,-21,-30,-31,-32,-16,31,-34,31,31,31,31,31,31,-15,31,31,31,31,31,31,31,31,-17,-33,31,]),'LESSTHAN':([13,16,17,18,19,20,22,23,40,41,43,44,46,47,48,49,50,51,52,53,54,55,56,57,58,59,60,61,63,],[32,-18,-19,-20,-21,-30,-31,-32,-16,32,-34,32,-10,-11,-12,-13,-14,-15,-22,-23,-24,-25,32,32,32,32,-17,-33,32,]),'GREATERTHAN':([13,16,17,18,19,20,22,23,40,41,43,44,46,47,48,49,50,51,52,53,54,55,56,57,58,59,60,61,63,],[33,-18,-19,-20,-21,-30,-31,-32,-16,33,-34,33,-10,-11,-12,-13,-14,-15,-22,-23,-24,-25,33,33,33,33,-17,-33,33,]),'LESSTHANEQUAL':([13,16,17,18,19,20,22,23,40,41,43,44,46,47,48,49,50,51,52,53,54,55,56,57,58,59,60,61,63,],[34,-18,-19,-20,-21,-30,-31,-32,-16,34,-34,34,-10,-11,-12,-13,-14,-15,-22,-23,-24,-25,34,34,34,34,-17,-33,34,]),'GREATERTHANEQUAL':([13,16,17,18,19,20,22,23,40,41,43,44,46,47,48,49,50,51,52,53,54,55,56,57,58,59,60,61,63,],[35,-18,-19,-20,-21,-30,-31,-32,-16,35,-34,35,-10,-11,-12,-13,-14,-15,-22,-23,-24,-25,35,35,35,35,-17,-33,35,]),'EQUALTO':([13,16,17,18,19,20,22,23,40,41,43,44,46,47,48,49,50,51,52,53,54,55,56,57,58,59,60,61,63,],[36,-18,-19,-20,-21,-30,-31,-32,-16,36,-34,36,-10,-11,-12,-13,-14,-15,-22,-23,-24,-25,-26,-27,36,36,-17,-33,36,]),'NOTEQUALTO':([13,16,17,18,19,20,22,23,40,41,43,44,46,47,48,49,50,51,52,53,54,55,56,57,58,59,60,61,63,],[37,-18,-19,-20,-21,-30,-31,-32,-16,37,-34,37,-10,-11,-12,-13,-14,-15,-22,-23,-24,-25,-26,-27,37,37,-17,-33,37,]),'AND':([13,16,17,18,19,20,22,23,40,41,43,44,46,47,48,49,50,51,52,53,54,55,56,57,58,59,60,61,63,],[38,-18,-19,-20,-21,-30,-31,-32,-16,38,-34,38,-10,-11,-12,-13,-14,-15,-22,-23,-24,-25,-26,-27,-28,38,-17,-33,38,]),'OR':([13,16,17,18,19,20,22,23,40,41,43,44,46,47,48,49,50,51,52,53,54,55,56,57,58,59,60,61,63,],[39,-18,-19,-20,-21,-30,-31,-32,-16,39,-34,39,-10,-11,-12,-13,-14,-15,-22,-23,-24,-25,-26,-27,-28,-29,-17,-33,39,]),'RPAREN':([16,17,18,19,20,22,23,40,41,43,46,47,48,49,50,51,52,53,54,55,56,57,58,59,60,61,],[-18,-19,-20,-21,-30,-31,-32,-16,60,-34,-10,-11,-12,-13,-14,-15,-22,-23,-24,-25,-26,-27,-28,-29,-17,-33,]),'RBRACKET':([16,17,18,19,20,21,22,23,40,42,43,44,46,47,48,49,50,51,52,53,54,55,56,57,58,59,60,61,63,],[-18,-19,-20,-21,-30,43,-31,-32,-16,61,-34,-35,-10,-11,-12,-13,-14,-15,-22,-23,-24,-25,-26,-27,-28,-29,-17,-33,-36,]),'COMMA':([16,17,18,19,20,22,23,40,42,43,44,46,47,48,49,50,51,52,53,54,55,56,57,58,59,60,61,63,],[-18,-19,-20,-21,-30,-31,-32,-16,62,-34,-35,-10,-11,-12,-13,-14,-15,-22,-23,-24,-25,-26,-27,-28,-29,-17,-33,-36,]),}

_lr_action = {}
for _k, _v in _lr_action_items.items():
   for _x,_y in zip(_v[0],_v[1]):
      if not _x in _lr_action:  _lr_action[_x] = {}
      _lr_action[_x][_k] = _y
del _lr_action_items

_lr_goto_items = {'program':([0,],[1,]),'file_declaration':([0,],[2,]),'variable_list':([0,2,5,],[3,7,9,]),'variable_dec':([0,2,5,],[5,5,5,]),'expression':([10,14,15,21,26,27,28,29,30,31,32,33,34,35,36,37,38,39,62,],[13,40,41,44,46,47,48,49,50,51,52,53,54,55,56,57,58,59,63,]),'condition':([10,14,15,21,26,27,28,29,30,31,32,33,34,35,36,37,38,39,62,],[18,18,18,18,18,18,18,18,18,18,18,18,18,18,18,18,18,18,18,]),'list':([10,14,15,21,26,27,28,29,30,31,32,33,34,35,36,37,38,39,62,],[19,19,19,19,19,19,19,19,19,19,19,19,19,19,19,19,19,19,19,]),'boolean':([10,14,15,21,26,27,28,29,30,31,32,33,34,35,36,37,38,39,62,],[20,20,20,20,20,20,20,20,20,20,20,20,20,20,20,20,20,20,20,]),'expression_list':([21,],[42,]),}

_lr_goto = {}
for _k, _v in _lr_goto_items.items():
   for _x, _y in zip(_v[0], _v[1]):
       if not _x in _lr_goto: _lr_goto[_x] = {}
       _lr_goto[_x][_k] = _y
del _lr_goto_items
_lr_productions = [
  ("S' -> program","S'",1,None,None,None),
  ('program -> file_declaration variable_list','program',2,'p_program','parser.py',18),
  ('program -> file_declaration','program',1,'p_program','parser.py',19),
  ('program -> variable_list','program',1,'p_program','parser.py',20),
  ('program -> <empty>','program',0,'p_program','parser.py',21),
  ('file_declaration -> PROJECTDEC STRING SEMICOLON','file_declaration',3,'p_file_declaration','parser.py',41),
  ('file_declaration -> PROJECTDEC STRING FILENAMEDEC STRING SEMICOLON','file_declaration',5,'p_file_declaration','parser.py',42),
  ('variable_list -> variable_dec variable_list','variable_list',2,'p_variable_list','parser.py',54),
  ('variable_list -> variable_dec','variable_list',1,'p_variable_list','parser.py',55),
  ('variable_dec -> VARIABLE EQUALS expression SEMICOLON','variable_dec',4,'p_variable_dec','parser.py',62),
  ('expression -> expression PLUS expression','expression',3,'p_expression','parser.py',69),
  ('expression -> expression MINUS expression','expression',3,'p_expression','parser.py',70),
  ('expression -> expression TIMES expression','expression',3,'p_expression','parser.py',71),
  ('expression -> expression DIVIDEDBY expression','expression',3,'p_expression','parser.py',72),
  ('expression -> expression MODULO expression','expression',3,'p_expression','parser.py',73),
  ('expression -> expression EXPONENT expression','expression',3,'p_expression','parser.py',74),
  ('expression -> MINUS expression','expression',2,'p_expression','parser.py',75),
  ('expression -> LPAREN expression RPAREN','expression',3,'p_expression','parser.py',76),
  ('expression -> STRING','expression',1,'p_expression','parser.py',77),
  ('expression -> NUMBER','expression',1,'p_expression','parser.py',78),
  ('expression -> condition','expression',1,'p_expression','parser.py',79),
  ('expression -> list','expression',1,'p_expression','parser.py',80),
  ('condition -> expression LESSTHAN expression','condition',3,'p_condition','parser.py',100),
  ('condition -> expression GREATERTHAN expression','condition',3,'p_condition','parser.py',101),
  ('condition -> expression LESSTHANEQUAL expression','condition',3,'p_condition','parser.py',102),
  ('condition -> expression GREATERTHANEQUAL expression','condition',3,'p_condition','parser.py',103),
  ('condition -> expression EQUALTO expression','condition',3,'p_condition','parser.py',104),
  ('condition -> expression NOTEQUALTO expression','condition',3,'p_condition','parser.py',105),
  ('condition -> expression AND expression','condition',3,'p_condition','parser.py',106),
  ('condition -> expression OR expression','condition',3,'p_condition','parser.py',107),
  ('condition -> boolean','condition',1,'p_condition','parser.py',108),
  ('boolean -> TRUE','boolean',1,'p_boolean','parser.py',120),
  ('boolean -> FALSE','boolean',1,'p_boolean','parser.py',121),
  ('list -> LBRACKET expression_list RBRACKET','list',3,'p_list','parser.py',125),
  ('list -> LBRACKET RBRACKET','list',2,'p_list','parser.py',126),
  ('expression_list -> expression','expression_list',1,'p_expression_list','parser.py',133),
  ('expression_list -> expression_list COMMA expression','expression_list',3,'p_expression_list','parser.py',134),
]
