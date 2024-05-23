import matlab.engine
import matlab
import matlab.engine
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import rcParams

eng = matlab.engine.start_matlab()
eng.cd("C:\\Users\\whitefork\\Desktop\\python\\myproject\\DRLR",nargout=0)

accuracy=[]
precision=[]
recall=[]
F1_score=[]
[accuracy,precision,recall,F1_score]=eng.DRLR3(nargout=4)
print(accuracy)
print(precision)
print(recall)
print(F1_score)

eng.exit()