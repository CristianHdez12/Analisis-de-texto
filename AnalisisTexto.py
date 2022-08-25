import math
from tkinter import *
from tkinter.scrolledtext import ScrolledText
from tkinter.ttk import *
from tkinter.filedialog import askopenfile
from tabulate import tabulate
import numpy as np
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class Programa:
    
    def __init__(self) -> None:
        self.root = Tk()
        self.root.title("Programa de análisis de texto")        
        self.miFrame=Frame(self.root, width=1000, height=650)
        self.miFrame.pack()

        self.lblTexto=Label(self.miFrame, text="Texto a analizar: ", font=18)
        self.lblTexto.grid(row=1, column=0, padx=5, pady=5)
        self.txtContenido = ScrolledText(self.miFrame,width=80, height=15, wrap=WORD)
        self.txtContenido.grid(row=2, column=0, columnspan=5, padx=10, pady=10)

        self.lblResultado=Label(self.miFrame, text="Texto analizado: ", font=18)
        self.lblResultado.grid(row=3, column=0, padx=5, pady=5)
        self.txtTabla = ScrolledText(self.miFrame,width=80, height=15)
        self.txtTabla.grid(row=4, column=0,columnspan=5, padx=10, pady=10)

        self.lblEntropia = Label(self.miFrame, text = "Gráfica de cantidad de información", font=18)
        self.lblEntropia.grid(row=1, column=5, padx = 5, pady = 5) 

        self.lblEntropia = Label(self.miFrame, text = "Gráfica de entropía", font=18)
        self.lblEntropia.grid(row=3, column=5, padx = 5, pady = 5)    
        #----------------Botón Seleccionar archivo
        botonArchivo=Button(self.miFrame, text="Seleccionar archivo", command=self.seleccionarArchivo)
        botonArchivo.grid(row=0, column=1, padx=10, pady=10)
        #----------------Botón Analizar------------------------
        botonAnalizar=Button(self.miFrame, text="Analizar", command=self.mostrarDatos)
        botonAnalizar.grid(row=0, column=2, padx=10, pady=10)
        #---------------Botón Limpiar texto
        botonLimpiar=Button(self.miFrame, text="Limpiar", command=self.limpiar)
        botonLimpiar.grid(row=0, column=3, padx=10, pady=10)

        self.root.mainloop()

    #---------------------Función para obtener los caracteres del texto
    def obtenerCaracteres(self):
        texto = self.txtContenido.get("1.0", "end-1c")
        caracteres = []
        cantidad = []
        probabilidad = []
        tamanio = len(texto)
        existe = False

        for i in texto:
            if caracteres:
                for j in caracteres:
                    if(i == j):
                        existe = True
                        break
                    else:
                        existe = False
                if existe == False:
                    caracteres.append(i)
            else:
                caracteres.append(i)


        for i in caracteres:
            c = texto.count(i)
            cantidad.append(c)
            probabilidad.append(c/tamanio)
            
        return caracteres, cantidad, probabilidad
    
    #------------Función para mostrar la tabla---------------------
    def mostrarDatos(self):
        caracteres, cantidad, probabilidad = self.obtenerCaracteres()
        self.txtTabla.delete("1.0", "end")
        tablaDatos = [ [0 for columna in range(4)] for fila in range (len(caracteres))]
        entropia = []
        info = []

        for i in range(len(caracteres)):
            tablaDatos[i][0] = caracteres[i]
            tablaDatos[i][1] = str(cantidad[i]) + "/" + str(sum(cantidad))
            c = round(float(math.log((1/probabilidad[i]),2)),2)
            info.append(c)
            tablaDatos[i][2] = info[i]
            c = round(float(probabilidad[i]*math.log((1/probabilidad[i]),2)),2)
            entropia.append(c)
            tablaDatos[i][3] = entropia[i]

        self.graficar(caracteres, info, 2, 5) #Graficando la cantidad de información
        self.graficar(caracteres, entropia, 4, 5) #Graficando la entropia

        self.txtTabla.insert("1.0", tabulate(tablaDatos, headers=["Simbolo","Probabilidad", "Cantidad de información", "Entropía"], tablefmt="pretty"))

    #-------------Función para abrir un archivo-------------------
    def seleccionarArchivo(self):
        archivo = askopenfile(mode='r', filetypes=[('Archivo de texto', '*.txt')])
        
        if archivo is not None:
            contenido = archivo.read()
            self.txtContenido.insert("1.0", contenido)
    
    #-----------------Función para graficar los datos
    def graficar(self, caracteres, valor, fila, columna):
        fig = Figure(figsize=(5, 2.5), dpi = 100)
        t = np.arange(0, 3, 0.1)
        fig.add_subplot(111).plot(caracteres,valor)
        canvas = FigureCanvasTkAgg(fig, master = self.miFrame)
        canvas.draw()
        canvas.get_tk_widget().grid(row=fila, column = columna, padx = 5, pady = 5)

    #-------------Función para limpiar los datos------------------
    def limpiar(self):
        self.txtContenido.delete("1.0","end")
        self.txtTabla.delete("1.0", "end")

programa = Programa()