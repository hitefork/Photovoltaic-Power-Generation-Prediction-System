import matlab.engine
import matlab
import matlab.engine
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import rcParams

eng = matlab.engine.start_matlab()
eng.cd("C:\\Users\\whitefork\\Desktop\\python\\myproject\\test1",nargout=0)

current=[]
voltage=[]
product=[]
label=[]
G=[1000.0,950]
T=[25.0,21]
vstc=[]
istc=[]
pstc=[]
[current,voltage,product,vstc,istc,pstc]=eng.simulate_and_record(G,T,nargout=6)
print(vstc)

print(istc)
print(pstc)

eng.exit()