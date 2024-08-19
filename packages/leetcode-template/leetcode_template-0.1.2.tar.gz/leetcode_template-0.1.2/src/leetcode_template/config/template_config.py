import json
import os

SIGNATURE_TEMPLATE = """{
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
}"""


class Config:
    def __init__(self, signature_json_filename: str = "signature.json"):
        self._load(signature_json_filename)

    def _load(self, signature_json_filename: str):
        if not os.path.exists(signature_json_filename):
            print(
                f"Signature file {signature_json_filename} not found. A new one called 'signature.json' will be created. Please edit the file with the correct signature and test cases."
            )
            with open("signature.json", "w") as f:
                f.write(SIGNATURE_TEMPLATE)

            exit(1)

        with open(signature_json_filename, "r") as signature_json:
            self.signature_json = json.load(signature_json)

    def get_problem_number_config(self):
        if self.signature_json.get("problemNumber") is None:
            raise ValueError("problemNumber not found in signature.json")
        return self.signature_json["problemNumber"]

    def get_return_type_config(self):
        if self.signature_json.get("returnType") is None:
            raise ValueError("returnType not found in signature.json")
        return self.signature_json["returnType"]

    def get_function_name_config(self):
        if self.signature_json.get("functionName") is None:
            raise ValueError("functionName not found in signature.json")
        return self.signature_json["functionName"]

    def get_parameters_config(self):
        if self.signature_json.get("parameters") is None:
            raise ValueError("parameters not found in signature.json")
        return self.signature_json["parameters"]

    def get_include_list_config(self):
        if self.signature_json.get("includeList") is None:
            raise ValueError("includeList not found in signature.json")
        return self.signature_json["includeList"]

    def get_test_cases_config(self):
        if self.signature_json.get("testCases") is None:
            raise ValueError("testCases not found in signature.json")
        return self.signature_json["testCases"]

    def get_function_signature(self):
        return f"{self.get_return_type_config()} {self.get_function_name_config()}({', '.join(self.get_parameters_config())})"

    def get_impl_function_declaration(self):
        return f"{self.get_return_type_config()} Solution::{self.get_function_name_config()}({', '.join(self.get_parameters_config())})"
        # return f"{signature_json['returnType']} Solution::{signature_json['functionName']}({', '.join(signature_json['parameters'])})"

    def get_include_list(self):
        include_list = ""
        for include in self.get_include_list_config():
            include_list += f"#include <{include}>\n"
        return include_list
