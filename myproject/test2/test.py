import matlab.engine
import matlab
import matlab.engine
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import rcParams

eng = matlab.engine.start_matlab()
eng.cd("C:\\Users\\whitefork\\Desktop\\python\\myproject\\test2",nargout=0)

returnP=[]
y_pred=[]
myflag1=float(1)
myflag2=float(1)
myflag3=float(1)
[returnP,y_pred]=eng.pvd_disp(myflag1,myflag2,myflag3,nargout=2)
print(returnP)
print(y_pred)

eng.exit()