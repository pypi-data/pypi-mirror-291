# Leetcode Template

## Quick Start
```bash
pip install leetcode-template

generate # A config file will be generated in the current directory

# Edit the config file to suit your needs

generate # Rerun the command to generate the directory structure based on the config file

```

## Config File
```json
{
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
}
```
