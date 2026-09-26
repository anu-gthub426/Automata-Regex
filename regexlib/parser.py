from .ast_nodes import Literal, Concat, Union, Star, Plus, Question

class Parser:

    def __init__(self, pattern):

        self.pattern=pattern
        self.pos=0

    def parse(self):

        node=self.parse_union()

        if self.pos!=len(self.pattern):

            raise ValueError("Unexpected character: " + self.pattern[self.pos])

        return node

    def parse_union(self):

        node=self.parse_concat()

        while self.pos<len(self.pattern) and self.pattern[self.pos] == '|':

            self.pos+=1
            right=self.parse_concat()
            node=Union(node,right)

        return node

    def parse_concat(self):

        node=self.parse_factor()

        while self.pos<len(self.pattern):

            char=self.pattern[self.pos]

            if char in '|)':

                break

            right=self.parse_factor()
            node=Concat(node,right)

        return node

    def parse_factor(self):

        if self.pos>=len(self.pattern):

            raise ValueError("Unexpected end of pattern")

        char=self.pattern[self.pos]

        if char=='(':

            self.pos+=1
            node=self.parse_union()

            if self.pos>=len(self.pattern) or self.pattern[self.pos]!=')':

                raise ValueError("Missing closing parenthesis")

            self.pos+=1

        elif char in '|)*+?':

            raise ValueError("Unexpected character: " + char)

        else:

            self.pos+=1
            node=Literal(char)

        while self.pos<len(self.pattern):

            char=self.pattern[self.pos]

            if char=='*':

                self.pos+=1

                node=Star(node)

            elif char=='+':

                self.pos+=1

                node=Plus(node)

            elif char=='?':

                self.pos+=1

                node=Question(node)

            else:

                break

        return node


def parse(pattern):

    return Parser(pattern).parse()