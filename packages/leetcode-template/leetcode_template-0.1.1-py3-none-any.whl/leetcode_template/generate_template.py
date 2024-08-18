import json
import os

try:
    with open("signature.json", "r") as f:
        signature_json = json.load(f)
except FileNotFoundError:
    print(
        "signature.json not found. A new one will be created. Please edit the file with the correct signature and test cases."
    )
    with open("signature.json", "w") as f:
        f.write("""{
    "problemNumber": 605,
    "returnType": "bool",
    "functionName": "canPlaceFlowers",
    "parameters": [
        "std::vector<int>& flowerbed",
        "int n"
    ],
    "includeList": ["vector"],
    "testCases":[{
        "testName": "Test1",
        "input": [
            "std::vector<int> flowerbed {1,0,0,0,0,0,1};",
            "int n = 1;"
        ],
        "inputParams": ["flowerbed", "n"],
        "expectedOutput": "true"
    },

    {
        "testName": "Test2",
        "input": [
            "std::vector<int> flowerbed = {1,0,0,0,1,0,1,0,0,1};",
            "int n = 2;"
        ],
        "inputParams": ["flowerbed", "n"],
        "expectedOutput": "false"
    }

    ]
}""")
    exit(1)


if not os.path.exists("include"):
    os.makedirs("include")

if not os.path.exists("src"):
    os.makedirs("src")

if not os.path.exists("tests"):
    os.makedirs("tests")


CMAKELISTS_TEMPLATE = """# set the project name to the name of the current directory
get_filename_component(PROJECT_NAME ${CMAKE_CURRENT_SOURCE_DIR} NAME)


# set source files
set(SOURCE_DIR "src")
file(GLOB_RECURSE SOURCES "${SOURCE_DIR}/*.cpp")


# set test files
set(TEST_DIR "tests")
file(GLOB_RECURSE TEST_SOURCES "${TEST_DIR}/test*.cpp")

# set include directories
include_directories("include")


include(FetchContent)
        FetchContent_Declare(
          googletest
          URL https://github.com/google/googletest/archive/b514bdc898e2951020cbdca1304b75f5950d1f59.zip
        )
        # For Windows: Prevent overriding the parent project's compiler/linker settings
        set(gtest_force_shared_crt ON CACHE BOOL "" FORCE)
        FetchContent_MakeAvailable(googletest)
        

enable_testing()

include(GoogleTest)

foreach(TEST_SOURCE ${TEST_SOURCES})
    get_filename_component(TEST_NAME ${TEST_SOURCE} NAME_WE)
    add_executable(${PROJECT_NAME}_${TEST_NAME} ${TEST_SOURCE} ${SOURCES})
    target_link_libraries(${PROJECT_NAME}_${TEST_NAME} gtest_main)
    gtest_discover_tests(${PROJECT_NAME}_${TEST_NAME})
endforeach()
"""


def get_function_signature(signature_json):
    return f"{signature_json['returnType']} {signature_json['functionName']}({', '.join(signature_json['parameters'])})"


def get_impl_function_declaration(signature_json):
    return f"{signature_json['returnType']} Solution::{signature_json['functionName']}({', '.join(signature_json['parameters'])})"


def get_include_list(signature_json):
    include_list = ""

    for include in signature_json["includeList"]:
        include_list += f"#include <{include}>\n"

    return include_list


HEADER_TEMPLATE = f"""
#ifndef SOLUTION_{signature_json["problemNumber"]}_H

{get_include_list(signature_json)}


class Solution {{
public:
  static {get_function_signature(signature_json)};
}};

#endif // SOLUTION_{signature_json["problemNumber"]}_H

"""

IMPLEMENTATION_TEMPLATE = f"""#include "solution_{signature_json["problemNumber"]}.h"

using namespace std;

{get_impl_function_declaration(signature_json)} {{
    // your code here
    
    return {signature_json["returnType"]}();
}}
"""

TEST_TEMPLATE = f"""#include "solution_{signature_json["problemNumber"]}.h"
#include <gtest/gtest.h>

#define SUITE_NAME Test{signature_json["problemNumber"]}

using namespace std;

"""


def make_tests(signature_json):
    tests = TEST_TEMPLATE
    for test_arr in signature_json["testCases"]:
        tests += f"""TEST(SUITE_NAME, {test_arr["testName"]}) {{
  {"\n  ".join(test_arr["input"])}

  ASSERT_EQ(Solution::{signature_json["functionName"]}({",".join(test_arr["inputParams"])}), {test_arr["expectedOutput"]}) << "Assertion Failed";
}}
"""

    return tests


with open("CMakeLists.txt", "w") as f:
    f.write(CMAKELISTS_TEMPLATE)

with open(f"include/solution_{signature_json["problemNumber"]}.h", "w") as f:
    f.write(HEADER_TEMPLATE)

with open("src/solution.cpp", "w") as f:
    f.write(IMPLEMENTATION_TEMPLATE)

with open("tests/tests.cpp", "w") as f:
    f.write(make_tests(signature_json))
