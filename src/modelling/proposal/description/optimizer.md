## Description Optimizer Rivers

### Files that are related with the optimization
- FOptimize/Dependencias.xlsx
- FOptimize/Objetivo.xlsx
- FOptimize/Variables.xlsx
- code.py
- optimize.py

##### FOptimize/Dependencias.xlsx

In this file we find a table in wich rows show the variables to optimize and the columns represents the variables that interact to get a value e.g

 - variable: OD
 - depencies : kdbo, teta_DBO

in the case of tetaa_DBO the column, teta_DBO does not exist in the excel file, so this means that this variable will not take part in thi optimization

Each value A_(ij) of row i column j could be a :
- x : means that this value will not be part in the optimization of var i
- 1 : means that this value will be part in the  optimization of the var i and, this var affect possitively its value.
- -1 :  means that this value will be part in the  optimization of the var i and, this var affect negattively its value.


##### FOptimize/Objetivo.xlsx
This is the training dataset to adjust the initial values of the parameters.


##### FOptimize/Variables.xlsx
This is a file which contains the last state of the variables used to run the program, this file change after each execution, and it's readed to take this state for the next run.
-  VariblesOriginales.xlsx, was the first state of the variables. This file is not used, just described in case of any question.


##### code.py
This code was created by @cbdavide in wich me @xdanielsb add a module to optimize the values of the variables using supervised learning. I shall talk just about the optimizer section. The important methods related to code.py are
 - run
 - cargar_variables


 ###### cargar_variables
 ```py
 def cargar_variables():
 ```
 This code loads the initil value for the variables, this values was the last value of the last run.
 The optmizer is called in this way
 ```py
 """
     Compute error, receive the file name who has the last state of the variables, and
     returns the errors, types of errores 'positive or negative', sign_dependency wich represents the dependency sign of that var to the variable to optimize and to_optimize, return a list of the variables that will be optimized.
 """
 errores, types, sign_dependency, to_optimize = computeError(name)
 """
     Here update the values according the error, {gradiente descendente}

     Based on the error returned value before we compute the new value of the variable in this way

     VALUE_VAR_Y = VALUE_VAR_Y  - SIGN_DEPENDENCY_VAR_Y * ERROR_TOTAL_VARY  * VALUE_VAR_Y * LEARNING_RATE * TYPE_VAR_Y

     This code (SIGN_DEPENDENCY_VAR_Y * ERROR_TOTAL_VARY  * VALUE_VAR_Y * LEARNING_RATE * TYPE_VAR_Y) computes the percentage of value that will be reduced of VALUE_VAR_Y, this is done to achieve and optimal faster, also could be done using a delta each epoch, but that will be slower.
 """
 learning_rate = 1
 for var in to_optimize:
     variables[var] += types[var]*errores[var]*variables[var]*learning_rate*sign_dependency[var]*-1
```

###### run
```py
def run(archivo_entrada, tiempo, directorio_salida, variables, show, export,tiempoTotal, epochs=1, estabaEntrenando =True):
```
This code initates the simulation, in which the optimizer is called


##### optimize.py
This script is composed by :
- computeError: computes MSE
- read_dependency_values: given the file, read the dependencies
