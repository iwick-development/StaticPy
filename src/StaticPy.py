import os
import sys
import json
import glob

def displayError(file, line, title, description):
    print("StaticPy Error | Failed to build " + file)
    print("\t" + file + ":" + str(line))
    print("\t" + title)
    print("\t\t" + description)
    sys.exit(1)

def detectVariableType(self, value):
    if value.startswith('"') or value.startswith("'"):
        return "string"
    elif value.startswith("["):
        return "list"
    elif value.startswith("{"):
        return "dict"
    elif value == "True" or value == "False":
        return "bool"
    elif value.isdigit() and not "." in value:
        return "int"
    elif "." in value:
        return "float"
    elif value.replace(":", "").split("(", 1)[-1] == ")":
        if value.replace(":", "") in self.functions:
            return self.functions[value.replace(":", "")]
    return "Null"

validTypes = ["string", "list", "dict", "bool", "bool", "int", "float", "void"]

class Convert:
    def __init__(self, file):
        self.output = []
        self.variables = {}
        self.functions = {}
        self.file = file
        self.lineNum = 1
        self.checkReturn = False

        self.parseFile()
    
    def convertToPy(self, string):
        spaces = ""
        if len(string) == 1:
            return string[0]
        
        if string[0] == '':
            while string[0] == "":
                spaces += " "
                string.remove("")
        
        if string[0] == "var":
            if not string[2] in validTypes:
                displayError(
                    self.file, 
                    self.lineNum, 
                    "InvalidType", 
                    string[2] + " is not a valid type"
                )

            variableType = detectVariableType(self, " ".join(string[string.index("=")+1:]))
            if variableType != string[2]:
                displayError(
                    self.file, 
                    self.lineNum, 
                    "VariableTypeError", 
                    string[1] + " was set as '" + string[2] + "' but defined as '" + variableType + "'"
                )
            if string[1] in self.variables:
                displayError(
                    self.file, 
                    self.lineNum, 
                    "VariableDefError", 
                    string[1] + " is already defined"
                )
            self.variables[string[1]] = variableType
            return spaces + string[1] + " = " + " ".join(string[string.index("=")+1:])
        elif string[1] == "=":
            if detectVariableType(self, string[2]) == "Null":
                displayError(
                    self.file, 
                    self.lineNum, 
                    "InvalidType", 
                    string[2] + " is not a valid type"
                )
            
            variableName = string[0]
            variableValue = string[2]
            if not variableName in self.variables:
                displayError(
                    self.file, 
                    self.lineNum, 
                    "VariableDefError", 
                    variableName + " is not defined"
                )
            if self.variables[variableName] != detectVariableType(self, variableValue):
                displayError(
                    self.file, 
                    self.lineNum, 
                    "VariableTypeError", 
                    variableName + " was set as '" + detectVariableType(self, variableValue) + "' but defined as '" + self.variables[variableName] + "'"
                )
            return spaces + " ".join(string)
        elif string[0] == "def":
            if len(string) < 3:
                displayError(
                    self.file, 
                    self.lineNum, 
                    "InvalidSyntax", 
                    "Invalid Syntax"
                )
            if not string[1] in validTypes:
                displayError(
                    self.file, 
                    self.lineNum, 
                    "InvalidType", 
                    string[2] + " is not a valid type"
                )

            returnType = string[1]
            if returnType != "void":
                self.checkReturn = {'functionLocation': self.lineNum, 'functionType': returnType}
            
            if string[2].replace(":", "") in self.functions:
                displayError(
                    self.file, 
                    self.lineNum, 
                    "FunctionDefError", 
                    string[2].replace(":", "") + " is already defined"
                )
            self.functions[string[2].replace(":", "")] = returnType
            return "def " + string[2]
        elif string[0] == "return" and self.checkReturn:
            detectedType = detectVariableType(self, string[1])
            if detectedType != "Null":
                if detectedType != self.checkReturn["functionType"]:
                    displayError(
                        self.file, 
                        self.lineNum, 
                        "FunctionTypeError", 
                        "Function at line " + str(self.checkReturn["functionLocation"]) + " cant return a " + detectedType
                    )
            elif string[1] in self.variables:
                detectType = self.variables[string[1]]
                if detectType != self.checkReturn["functionType"]:
                    displayError(
                        self.file, 
                        self.lineNum, 
                        "FunctionTypeError", 
                        "Function at line " + str(self.checkReturn["functionLocation"]) + " cant return a " + detectType
                    )
                self.checkReturn = False

        if len(string) == 1:
            return string[0]
        
        return spaces + " ".join(string)

    def parseFile(self):
        with open(self.file) as f:
            self.fileLines = f.read().splitlines()
    
        for line in self.fileLines:
            spaces = line.split(" ")
            self.output.append(self.convertToPy(spaces))
            self.lineNum += 1
            
        with open(self.file.replace(".spy", ".py").replace("src\\", ""), "w") as f:
            f.write("\n".join(self.output))

        self.output = []
        self.variables = {}
        self.functions = {}
        self.lineNum = 1

if len(sys.argv) != 2:
    print("Invalid arguments")
    print("Usage:")
    print("\tstaticpy.exe 'test.py'")
elif not os.path.exists(sys.argv[1]):
    print("Unable to locate: " + sys.argv[1])
else:
    Convert(sys.argv[1])
