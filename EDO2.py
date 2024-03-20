# Génère une équation différentielle vérifiée par le déterminant d'une base de solution à l'aide de Sympy

from sympy import *
from sympy.parsing.sympy_parser import parse_expr
import tkinter as tk
from PIL import ImageTk, Image

class Application:
    def __init__(self):
        self.l = tk.Label(fenetre, text="Entrez les deux fonctions (notation python) : ")
        self.equationimg = ImageTk.PhotoImage(Image.new('1', (0, 0)))
        self.resultat = tk.Label(fenetre, image = self.equationimg)
        self.resultat.grid(row=3, column=1)
        self.f1 = tk.Entry(fenetre, textvariable=tk.StringVar())
        self.f1.insert(0, "exp(x*2)")
        self.f2 = tk.Entry(fenetre, textvariable=tk.StringVar())
        self.f2.insert(0, "sin(x)")
        self.b = tk.Button(text="Générer !", command=self.resoudre)
        self.l.grid(row=1, column=1)
        self.f1.grid(row=2, column=1)
        self.f2.grid(row=2, column=2)
        self.b.grid(row=2, column=3)
    def resoudre(self):
        self.equation = equadiff([self.f1.get(), self.f2.get()])
        preview(self.equation, viewer='file', filename="out.png", dvioptions=['-D','100'], euler=False,)
        self.equationimg = ImageTk.PhotoImage(Image.open("out.png"))
        self.resultat.configure(image=self.equationimg)
        
       
def equadiff(F):
    x = symbols('x')
    ordre = 2
    y = [symbols('y'+'\''*i) for i in range(ordre+1)]
    expr = F
    f = [parse_expr(i) for i in expr]
    fp = [diff(i, x) for i in f]
    fpp = [diff(i, x) for i in fp]
    M = zeros(2, 3)
    for i in range(ordre):
        for j in range(ordre+1):
            M[i,j] = (fpp, fp, f)[j][i]
    M = M.row_insert(2, Matrix([[y[i] for i in range(ordre, -1, -1)]]))
    eq = M.det()
    coefs = []
    for i in range(ordre+1):
        coefs.append(simplify(collect(expand(eq), y[i]).coeff(y[i])))
    for i in range(ordre+1):
        coefs[i] = coefs[i]/coefs[2]
        coefs[i] = simplify(coefs[i])
    eq = Add(*[y[i] * coefs[i] for i in range(ordre+1)])
    return Eq(eq, 0)

fenetre = tk.Tk()
fenetre.geometry("800x450")
fenetre.title("EDO2")
App = Application()
fenetre.mainloop()