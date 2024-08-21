# codefeedback

## Description:
The package is used for students to check their codes in jupyter notebook. 
The ai functionality will be implemented after security check (only for Imperial students). 

It supports code check including syntax, structure, method, and variable check. The 
graph will display on the jupyter terminal (both res & ans), but students should check it by themselves.

## Installation:
The package is released on Pypi, so use ```pip install codefeedback``` (depending on different system)
can download the package.

## Magic Line:

- %load_ext codefeedback: load all extensions in the package
- %load_module: import all necessary modules (Notice that dynamic import is not allowed)
- %load_answer script_name: load the answer sheet (currently support .py, .csv) 
- %check task_name: set it to the end of your code and specify the task name