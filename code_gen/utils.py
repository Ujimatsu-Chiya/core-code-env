from enum import Enum
import re

class TypeEnum(Enum):
    BOOL = 'bool'
    BOOL_LIST = 'bool[]'
    INT = 'int'
    LONG = 'long'
    LONG_LIST = 'long[]'
    DOUBLE = 'double'
    STRING = 'string'
    INT_LIST = 'int[]'
    INT_LIST_LIST = 'int[][]'
    DOUBLE_LIST = 'double[]'
    STRING_LIST = 'string[]'
    TREENODE = 'TreeNode'
    LISTNODE = 'ListNode'

    @staticmethod
    def get_base_type(p_type):
        mp = {
            TypeEnum.INT_LIST: TypeEnum.INT,
            TypeEnum.BOOL_LIST: TypeEnum.BOOL,
            TypeEnum.DOUBLE_LIST: TypeEnum.DOUBLE,
            TypeEnum.STRING_LIST: TypeEnum.STRING,
            TypeEnum.INT_LIST_LIST: TypeEnum.INT_LIST,
            TypeEnum.LONG_LIST: TypeEnum.LONG_LIST
        }
        assert p_type in mp.keys()
        return mp[p_type]


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