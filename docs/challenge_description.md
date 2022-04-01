# Challenge description

Water is a daily necessary resource for life, health, economic development and
the ecosystem all over the world.  Although water is still a relatively cheap
and accessible commodity in Europe, drinking water discharges still represent
significant losses to the environment, especially during increasingly frequent
drought periods. On the other hand, faecal wastewater leaks are also undesirable,
as they can further destroy infrastructure and pollute the environment. Public 
utility companies strive to eliminate spills and control their pipeline system 
as soon as possible, but with the increasing diversification, the control of 
such systems is a difficult task. 

Medius is challenging EESTech Challenge participants here!

Teams will have the task of **detecting potential water leakage** before it occurs,
using the data we measure on the micro turbines and the principles of machine
learning. Faster and more efficient detection of potential water discharges can
drastically help reduce drinking water losses.

With the help of pre-prepared data, the participants of the challenge will
be challenged with task of develop an algorithm that will try to automatically 
detect water spills. As its input, the algorithm will obtain measurable quantities
of micro turbines in the form of time series, process them and try to predict or.
detect water outflow.

Implement your solution in [predict.py](leak_detection.py) under the method predict. The method takes in a list of features and should return a boolean.
It should return true if leak is detected, otherwise it should return false. You can create new files and import them into predict.py.
evaluate.py is an example of how predict method will be called for evaluation. You can use it to test your solution.
