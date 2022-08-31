import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from numpy.polynomial import polynomial as poly

def find_correct_inters(poly,val,start,end):
    moved_poly = poly-val
    roots = np.polynomial.polynomial.polyroots(moved_poly.coef)
    for i, root in enumerate(roots):
        if start < root < end:
            if roots[i].imag == 0:
                print("int point is:")
                print(root.real)

t = np.linspace(-3.4,2.5,200)

Arr = np.array([5,48,-32,-28,8,4])
p = np.polynomial.Polynomial(Arr)


print(p)
inter = 150
st = -3.5
en = 2.5
new_p = p-inter
print(new_p)
roots = np.polynomial.polynomial.polyroots(new_p.coef)
print(roots)

find_correct_inters(p,inter,st,en)

plt.plot(t, p(t))
plt.plot([-3.4,2.5], [inter,inter])
plt.scatter(roots.real,[p(roots.real[0]),p(roots.real[1]),p(roots.real[2]),p(roots.real[3]),p(roots.real[4])])
plt.show()

def find_correct_inters(poly,val,start,end):
    moved_poly = poly-val
    roots = np.polynomial.polynomial.polyroots(moved_poly.coef)
    for root in roots:
        if start < root < end:
            return root.real


    

