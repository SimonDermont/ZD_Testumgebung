
start_conditions = [0.01,0.0001,1,-0.001]
for i, val in enumerate(start_conditions):
    if val < 0.001 and val > -0.001:
        start_conditions[i]=0


print (start_conditions)