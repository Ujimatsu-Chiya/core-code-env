from typing import List
from utils import *
from py_gen_main import py_test
from cpp_gen_main import cpp_test
from java_gen_main import java_test
from c_gen_main import c_test
from ts_gen_main import ts_test
from js_gen_main import js_test
from go_gen_main import go_test

import os

def test(function_name:str, params_type:List[TypeEnum], params_name:List[str], return_type:TypeEnum):
    assert len(params_name) == len(params_type)
    RESULT = 'result'
    operations = {
        'c': [c_test, to_snake_case, to_snake_case],
        'cpp': [cpp_test, to_snake_case, to_snake_case],
        'java':[java_test, to_camel_case, to_camel_case],
        'py': [py_test, to_snake_case, to_snake_case],
        'ts':[ts_test, to_camel_case, to_camel_case],
        'js':[js_test, to_camel_case, to_camel_case],
        'go':[go_test, to_pascal_case, to_camel_case]
    }
    os.makedirs(RESULT, exist_ok=True)
    for lang, (lang_test, function_name_style, params_name_style) in operations.items():
        result = lang_test(function_name_style(function_name), params_type, list(map(params_name_style, params_name)), return_type)
        if result[0] != 0:
            print(result)
        else:
            result = result[1]
            for filename, code in result.items():
                with open(os.path.join(RESULT, filename),'w') as fp:
                    fp.write(code)

if __name__ == '__main__':
    params_type = [TypeEnum.INT, TypeEnum.LONG, TypeEnum.DOUBLE, TypeEnum.STRING, TypeEnum.INT_LIST,
                   TypeEnum.INT_LIST_LIST, TypeEnum.DOUBLE_LIST, TypeEnum.STRING_LIST, TypeEnum.BOOL_LIST,
                   TypeEnum.BOOL, TypeEnum.TREENODE, TypeEnum.LISTNODE]
    function_name = 'solveMyProblem'
    params_name = [
        "appleTreeInTheMorning",
        "bigMountainWithSnow",
        "coolBreezeOnTheBeach",
        "dancingStarsUnderTheMoonlight",
        "elegantFlowerInTheGarden",
        "funnyDogChasingItsTail",
        "greenAppleFreshFromTheTree",
        "happyBirdSingingInTheTree",
        "interestingBookWithManyStories",
        "joyfulSunriseOnTheHorizon",
        "kindHeartHelpingOthers",
        "laughingChildInThePark"
    ]
    return_type = TypeEnum.INT_LIST_LIST
    print(test('solve', params_type, params_name, return_type))