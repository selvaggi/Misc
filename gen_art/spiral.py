import numpy as np
import matplotlib.pyplot as plt
import math

def fermat_spiral(dot):
    data=[]
    d=dot*0.1
    for i in range(dot):
        t = i / d * np.pi
        x = (1 +  t) * math.cos(t)
        y = (1 +  t) * math.sin(t)
        data.append([x,y])
    narr = np.array(data)
    f_s = np.concatenate((narr,-narr))
    return f_s

f_spiral = fermat_spiral(2000)
plt.scatter(f_spiral[len(f_spiral)//2:,0],f_spiral[len(f_spiral)//2:,1])
plt.scatter(f_spiral[:len(f_spiral)//2,0],f_spiral[:len(f_spiral)//2,1])
plt.show()
