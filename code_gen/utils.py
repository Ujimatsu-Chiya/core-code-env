from dataclasses import dataclass
from enum import Enum, auto
import re
from typing import List


class TypeEnum(Enum):
    BOOL = auto()
    INT = auto()
    LONG = auto()
    DOUBLE = auto()
    STRING = auto()
    INT_LIST = auto()
    INT_LIST_LIST = auto()
    DOUBLE_LIST = auto()
    STRING_LIST = auto()
    BOOL_LIST = auto()
    TREENODE = auto()
    LISTNODE = auto()
    LONG_LIST = auto()
    NONE = auto()

    @staticmethod
    def get_base_type(p_type: 'TypeEnum'):
        mp = {
            TypeEnum.INT_LIST: TypeEnum.INT,
            TypeEnum.BOOL_LIST: TypeEnum.BOOL,
            TypeEnum.DOUBLE_LIST: TypeEnum.DOUBLE,
            TypeEnum.STRING_LIST: TypeEnum.STRING,
            TypeEnum.INT_LIST_LIST: TypeEnum.INT_LIST,
            TypeEnum.LONG_LIST: TypeEnum.LONG,
        }
        assert p_type in mp.keys()
        return mp[p_type]

    @staticmethod
    def get_dimension(p_type: 'TypeEnum'):
        return {
            TypeEnum.BOOL: 0,
            TypeEnum.BOOL_LIST: 1,
            TypeEnum.INT: 0,
            TypeEnum.LONG: 0,
            TypeEnum.LONG_LIST: 1,
            TypeEnum.DOUBLE: 0,
            TypeEnum.STRING: 0,
            TypeEnum.INT_LIST: 1,
            TypeEnum.INT_LIST_LIST: 2,
            TypeEnum.DOUBLE_LIST: 1,
            TypeEnum.STRING_LIST: 1,
            TypeEnum.TREENODE: 0,
            TypeEnum.LISTNODE: 0,
            TypeEnum.NONE: -1
        }[p_type]

@dataclass(frozen=True)
class TypeSpec:
    lang_type: str
    default: str
    des_func: str
    ser_func: str


def split_pascal_case(s):
    if re.match(r'^[A-Z][a-zA-Z]*$', s):
        words = re.findall(r'[A-Z][a-z]*', s)
        return [word.lower() for word in words]
    else:
        return []


def split_camel_case(s):
    if re.match(r'^[a-z]+([A-Z][a-z]*)*$', s):
        words = re.findall(r'[a-z]+|[A-Z][a-z]*', s)
        return [word.lower() for word in words]
    else:
        return []
    

def split_snake_case(s):
    if re.match(r'^[a-z]+(_[a-z]+)*$', s):
        words = s.split('_')
        return [word.lower() for word in words]
    else:
        return []

def split_words(s):
    ls = [res for res in [split_pascal_case(s), split_camel_case(s), split_snake_case(s)] if res]
    assert len(ls) > 0
    return ls[0]

def to_pascal_case(s):
    words = split_words(s)
    return "".join([word[0].upper() + word[1:] for word in words])

def to_camel_case(s):
    words = split_words(s)
    return words[0] + "".join([word[0].upper() + word[1:] for word in words[1:]])

def to_snake_case(s):
    words = split_words(s)
    return "_".join(words)

json_default_val = {
    TypeEnum.BOOL : 'false',
    TypeEnum.INT : '0',
    TypeEnum.LONG : '0',
    TypeEnum.DOUBLE : '0.0',
    TypeEnum.STRING: '"s"',
    TypeEnum.INT_LIST: '[1]',
    TypeEnum.INT_LIST_LIST: '[[1,2],[3,4]]',
    TypeEnum.DOUBLE_LIST: '[1.0]',
    TypeEnum.STRING_LIST: '["a"]',
    TypeEnum.BOOL_LIST: '[false, true]',
    TypeEnum.TREENODE: '[1,null,2]',
    TypeEnum.LISTNODE: '[1,2]',
    TypeEnum.LONG_LIST : '[1]',
    TypeEnum.NONE : 'null'
}

@dataclass
class MethodDef:
    function_name: str
    params_type: List[TypeEnum]
    params_name: List[str]
    return_type: TypeEnum

    def generate(self) -> str:
        raise NotImplementedError()

@dataclass
class ClassDef:
    """用来描述一个类具有哪些方法"""
    name: str
    constructor: MethodDef
    methods: List[MethodDef]

    def __post_init__(self):
        raise NotImplementedError()

    def constructor_generate(self):
        raise NotImplementedError()