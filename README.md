This program code is developed in:- 
```
Python3:            Python 3.10.6
IDE:                Visual Studio Code
    Version:        1.77.3
    OS:             Windows_NT x64 10.0.22621
    Sandboxed:      No
Machine:
    Processor:      Intel(R) Core(TM) i5-8300H CPU @ 2.30GHz
    Installed RAM:  32.0 GB (31.8 GB usable)
    System type:    64-bit operating system, x64-based processor
OS:
    Edition:        Windows 11 Home Single Language
    Version:        22H2
    OS build:       22621.1555
```

no additional libraries are required to run the program: it only uses libraries that are included with standard installation of the mentioned python version<br>

---

To invoke the operable program "Python", precede arguments with:<br>
python or py (given that the running environment recognizes the global environment variable and points to the bin folder of the python installation )<br>

The code is invoked with the following command-line arguments:<br>
bnet.py <training_data> <query variable values> [given <evidence variable values>]

<training_data> is a *required* argument with text file type <br>
<query variable values>:Values of Query Variable<br>
<evidence variable values>:Values of Evidence Variable (if any)<br>
Format for the variable values (case sensitive):
      
```
      Bt if B is true, Bf if B is false
      Gt if G is true, Gf if G is false
      Ct if C is true, Cf if C is false
      Ft if F is true, Ff if F is false
```

examples of command-line invocation of the program (exclude `,`lines preceded by - are description of what the arguments expect from the code):<br>
`python bnet.py training_data.txt Bt Gf Ct Ff`  <br>
      -Train the Bayesian Network and use it to calculate P(B=t, G=f, C=t, F=f)<br>
`python bnet.py training_data.txt Bt Gf given Ff ` <br>
      -Train the Bayesian Network and use it to calculate P(B=t, G=f | F=f)<br>
`python bnet.py training_data.txt Bt Ff`  <br>
      -Train the Bayesian Network and use it to calculate P(B=t, F=f)<br>

---
There are no additional files necessary to run the main "bnet.py" file<br>
The Bayes' Network used in this program is as illustrated in bnet.png<br>

---
## Structure and Operation:

 • File: README.txt<br>
The text file contains instructions for running bnet.py. The file specifies the required and optional command-line arguments for running the program. <br>
The file also provides information on the development environment and system requirements for running the program, and the program structure and implementation.<br>

 • File: bnet.png<br>
Illustration of the Bayesian Network that the program is based on.<br>

 • File: BNet(ref).png<br>
Illustration of the Bayesian Network that the program is based on, with probability tables that the training data should result in.<br>

 • File: training_data.txt<br>
The text file that containg recorded event observation that is used by the program to calculate the required probabilities, according to the Bayes Network. Format of the data to be contained in the file:<br>
-The first number is 0 if there is no baseball game on TV (B is false), and 1 if there is a baseball game on TV (B is true).<br>
-The second number is 0 if George does not watch TV (G is false), and 1 if George watches TV (G is true).<br>
-The third number is 0 if George is not out of cat food (C is false), and 1 if George is out of cat food (C is true).<br>
-The fourth number is 0 if George does not feed the cat (F is false), and 1 if George feeds the cat (F is true).<br>
Each of these numbers is seperated by spaces, and every entry is seperated by a "newline" character. The name of this file is the second argument(index 1) to be passed to python after invoking the program file 'bnet.py' and is a required argument.<br>

 • File: bnet.py<br>
This file contains the main code for calculating conditional probabilities based on the Bayes' Network. It defines several functions and implements the calculation of conditional probabilities. <br>
"import sys"and "from collections import defaultdict" lines import the only additional (included with standard installation of python) libraries required for the running of the code. It is used for passing arguments from the command line, and creating the data structure to store the count values for each probabilities.<br>
      |
 + It calculates conditional probability using:<br>
      `P(query_variable|evidence_variables) = P(query_variable ∧ evidence_variables)/P(evidence_variables)` <br>
 + It performs inference by enumeration using:<br>
      `P = ΣP(B ∧ G ∧ C ∧ F)`<br>
      Taking values(0(False) or 1(True)) static for the ones given, and/or considering all combinations of 0(False) and 1(True) for the ones not explicitly asked for.<br>

 - Function: numcalc(queryl, query_variables,altset)<br>
This function takes three arguments. The first argument, queryl, is a tuple of the query variables. <br>
The second argument, query_variables, is a dictionary containing the query variables and their values. <br>
The third argument, altset, is a list of the alternate values for the variables not in the queryl (to consider both-true and false for variables not explicitly given value for, as per the formula in `File: bnet.py` entry above). <br>
The function returns a dictionary containing the values of all variables, both in the query and not in the query.<br>

 - Function: enumerate(query_variables)<br>
This function takes one argument, query_variables, which is a dictionary containing the query variables and their values (we consider numerator or denominator as a whole as query_variables here, for the formula in `File: bnet.py` entry above). <br>
The function computes the probability of the query by summing over all possible values of the variables not in the query. <br>
It uses the numcalc() function to compute the values of all variables, both in the query and not in the query.<br>

 - Function: calculate_conditional_probability(query_variables, evidence_variables<br>
This function handles the query variables and the evidence variables calculation. It calls the enumerate function seperately for numerator and denominator and returns the final result calculated (as per the formula in `File: bnet.py` entry above) back to the main function. [NOTE: While computing the division, a small value of 1*e-16 is added to the denominator, to counter P(evidence_variables)=0]<br>

 - Main code block<br>
The main code block first checks the command-line arguments and initializes the query variables accordingly. <br>
Then, it loads the data from the dataset in the mentioned format. Next, it iterates over the data and create a count which is then converted to probabilities and joint probabilities. <br>
[NOTE: the probablity value is rounded after 9 decimal places, to match the values exactly as given in the Bayesian Network probablity tables (find reference network in: `File: BNet(ref).png`). This also counters the 1*e-16 correction value that we added to the denominator in `Function:calculate_conditional_probability`]<br>
It contains the main block to call the calculate_conditional_probability function and prints the result as output. <br>
      |
 +  The output format is: <br>
      `P({query variables=<True/False>} | {evidence variables=<True/False>}) = {probability}`

---
