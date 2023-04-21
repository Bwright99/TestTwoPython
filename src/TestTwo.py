
class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.current = 0

    def parse(self):
        return self.stmt_list() 

    def match(self, expected_token):
        if self.tokens[self.current] == expected_token:
            self.current += 1
            return True
        else:
            return False

    def stmt(self):
        if self.if_stmt() or self.block() or self.assign() or self.declare() or self.while_loop():
            return True
        else:
            return False

    def stmt_list(self):
        while self.stmt():
            if not self.match(";"):
                return False
        return True

    def while_loop(self):
        if self.match("while") and self.match("(") and self.bool_expr() and self.match(")") and self.block():
            return True
        else:
            return False

    def if_stmt(self):
        if self.match("if") and self.match("(") and self.bool_expr() and self.match(")") and self.block():
            if self.match("else"):
                return self.block()
            else:
                return True
        else:
            return False

    def block(self):
        if self.match("{") and self.stmt_list() and self.match("}"):
            return True
        else:
            return False

    def declare(self):
        if self.match("DataType") and self.match("ID"):
            while self.match(",") and self.match("ID"):
                pass
            return True
        else:
            return False

    def assign(self):
        if self.match("ID") and self.match("=") and self.expr():
            return True
        else:
            return False

    def expr(self):
        if self.term():
            while self.match("+") or self.match("-"):
                if not self.term():
                    return False
            return True
        else:
            return False

    def term(self):
        if self.fact():
            while self.match("*") or self.match("/") or self.match("%"):
                if not self.fact():
                    return False
            return True
        else:
            return False

    def fact(self):
        if self.match("ID") or self.match("INT_LIT") or self.match("FLOAT_LIT"):
            return True
        elif self.match("(") and self.expr() and self.match(")"):
            return True
        else:
            return False

    def bool_expr(self):
        if self.bterm():
            while self.match(">") or self.match("<") or self.match(">=") or self.match("<="):
                if not self.bterm():
                    return False
            return True
        else:
            return False

    def bterm(self):
        if self.band():
            while self.match("==") or self.match("!="):
                if not self.band():
                    return False
            return True
        else:
            return False

    def band(self):
        if self.bor():
            while self.match("&&"):
                if not self.bor():
                    return False
            return True
        else:
            return False

    def bor(self):
        if self.expr():
            while self.match("||"):
                if not self.expr():
                    return False
            return True
        else:
            return False
        
tokens = ['if', '(', 'x', '<', '>', 'y', ')', '{', 'x', '=', 'y', ';', '}', 'else', '{', 'y', '=', 'x', ';', '}', 'while', 'while_loop', '&&','||', '>=', '<=', '==', '!=', '(', ')', '{', '}', ';', 'DataType', 'ID', 'INT_LIT', 'FLOAT_LIT', '+', '-', '*', '/', '%', '>', '<', ',', '='] 

parser = Parser(tokens)
result = parser.parse()
print(result)

""" 
<STMT> -> <IF> | <BLOCK> | <ASSIGN> | <DECLARE> | <WHILE> 
<STMT_LIST> -> <STMT> {; <STMT>}
<WHILE_LOOP> -> while ( <BOOL_EXPR> ) <BLOCK>
<IF_STMT> -> if ( <BOOL_EXPR> ) <BLOCK> [else <BLOCK>]
<BLOCK> -> { <STMNT_LIST> }
<DECLARE> -> DataType ID {, ID}
<ASSIGN> -> ID = <EXPR>
<EXPR> -> <TERM> {+ <TERM> | - <TERM>}
<TERM> -> <FACT> {*  | / | % }
<FACT> -> ID | INT_LIT | FLOAT_LIT | ( <EXPR> )
<BOOL_EXPR> -> <BTERM> {> | < | >= | <= <BTERM>}
<BTERM> -> <BAND> {> | < | >= | <=}
<BAND> -> <BOR> {&& <BOR>}
<BOR> -> <EXPR> {|| <EXPR>}

Mstmnt(<STMT>,s)Δ=case<STMT>of
    <IF>=>Mif(<IF>)
    <BLOCK>-> if BLOCK(<BLOCK>,s)==undefined then error else BLOCK(<BLOCK>,s)
    <ASSIGN>-> if ASSIGN(<ASSIGN>,s)==undefined then error else ASSIGN(<ASSIGN>,s)
    <DECLARE>-> if DECLARE(<DECLARE>,s)==undefined then error else DECLARE(<DECLARE>,s)
    <WHILE>-> Mwhile(<WHILE>)
    <STMNT>=>Mstmnt(<STMNT>)
        then Mstmnt_list(<STMNT_LIST>,s)Δ
    <While_loop>=>Mwhile_loop(<WHILE_LOOP>==(<Bool_expr>) then (<BLOCK>))
    <IF_STMT>=>Mif_stmt(<IF_STMT>==if (<Bool_expr>) then (<BLOCK>) else (<BLOCK>))
    if <BLOCK>=>Mblock(<BLOCK>=={<STMNT_LIST>})
        <DECLARE>=>Mdeclare(<DECLARE>==DataType ID {, ID})
        <ASSIGN>=>Massign(<ASSIGN>==ID = <EXPR>)
    then
        <EXPR>=>Mexpr(<EXPR>==<TERM> {+ <TERM> | - <TERM>},s)
        <TERM>=>Mterm(<TERM>==<FACT> {*  | / | % },s)
        <FACT>=>Mfact(<FACT>==ID | INT_LIT | FLOAT_LIT | ( <EXPR> ),s)
    if <bool_expr>=>Mbool_expr(<BOOL_EXPR>==<BTERM> {> | < | >= | <= <BTERM>},s) 
    then <BTERM>=>Mbterm(<BTERM>==<BAND> {> | < | >= | <=},s)
         <BAND>=>Mband(<BAND>==<BOR> {&& <BOR>},s)

<STMT> : token -> token
<IF> : token -> token 
If the boolean expression is true, evaluate the first block, otherwise evaluate the second block (if it exists).

<BLOCK> : token -> token
Evaluate each statement in the statement list in order.

<ASSIGN> : token -> token
Update the value of the variable with the value of the expression.

<DECLARE> : token -> token
Add the declared variables to the state with a default value of 0.

<WHILE> : token -> token
Evaluate the boolean expression and if it is true, evaluate the block and repeat until the boolean expression is false.

<STMT_LIST> : token -> token
Evaluate each statement in the list in order.

<WHILE_LOOP> : token -> token
Evaluate the boolean expression and if it is true, evaluate the block and repeat until the boolean expression is false.

<IF_STMT> : token -> token
If the boolean expression is true, evaluate the first block, otherwise evaluate the second block (if it exists).

<BLOCK> : token -> token
Evaluate each statement in the statement list in order.

<DECLARE> : token -> token
Add the declared variables to the state with a default value of 0.

<ASSIGN> : token -> token
Update the value of the variable with the value of the expression.

<EXPR> : token -> result
Evaluate the expression and return
 """