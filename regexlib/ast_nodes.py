from dataclasses import dataclass

class ASTNode:

    pass

@dataclass
class Literal(ASTNode):

    value: str


@dataclass
class Concat(ASTNode):

    left: ASTNode
    right: ASTNode


@dataclass
class Union(ASTNode):

    left: ASTNode
    right: ASTNode


@dataclass
class Star(ASTNode):

    child: ASTNode


@dataclass
class Plus(ASTNode):

    child: ASTNode


@dataclass
class Question(ASTNode):

    child: ASTNode