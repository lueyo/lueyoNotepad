import tkinter as tk
from tkinter.filedialog import askopenfilename, asksaveasfilename
import tkinter.ttk as ttk
from pynput import keyboard
import threading as th
import os.path, sys, os
from sys import argv
import json
import wget
import shutil
import pygetwindow as gw




class editor():

    def __init__(self):
        #self.user=os.environ.get('USERNAME')
        
        self.currentdir=os.getcwd()
        self.selected=False
        self.estilosinicio()
        self.hilos()
        self.ventana()
        
        
        
        
        
    def hilos(self):
        
        hilos = list()
        self.ke = th.Thread(target=self.liskeys)
        hilos.append(self.ke)
        self.ke.start()
        self.stop = th.Event()
        
    def estilosinicio(self):
        self.user=os.environ.get('USERNAME')
        #print(self.user)
        self.config = {
            "fuente",
            "alturaactual",
            "anchuraactual",
            "fontsize",
        }

        try:
            self.config=json.load(open("C:/Users/"f"{(self.user)}/Downloads/configln.json","r"))

            if self.config=="":
                self.jsonabierto=open("C:/Users/"f"{(self.user)}/Downloads/configln.json","w")
                configdefecto={
                "fuente":"Calibri",
                "alturaactual":200,
                "anchuraactual":200,
                "fontsize":12
                                }
                self.jsonabierto.write(str(configdefecto).replace("'",'"'))

            #print(self.config)
                

        except FileNotFoundError:
            self.aplicardefecto
        except json.decoder.JSONDecodeError:
            self.aplicardefecto()
    
    def saveconfig(self):
        configactual={
            "fuente":self.fuente,
            "alturaactual":self.alturaactual,
            "anchuraactual":self.anchuraactual,
            "fontsize":self.fontsize
                                }
        self.jsonabierto=open("C:/Users/"f"{(self.user)}/Downloads/configln.json","w")
        #self.jsonabierto.write(str(configactual).replace())  
        self.jsonabierto.write(str(configactual).replace("'",'"'))

    def aplicardefecto(self):
        self.jsonabierto=open("C:/Users/"f"{(self.user)}/Downloads/configln.json","w")
        configdefecto={
        "fuente":"Calibri",
        "alturaactual":200,
        "anchuraactual":200,
        "fontsize":12
                            }
        self.jsonabierto.write(str(configdefecto).replace("'",'"'))


    def ventana(self):
        self.wn = tk.Tk()
        try:
            self.fontsize = self.config["fontsize"]
            self.fuente= self.config["fuente"]
        except TypeError:
            try:
                self.aplicardefecto()
                self.config=json.load(open("C:/Users/"f"{(self.user)}/Downloads/configln.json","r"))
                self.fontsize = self.config["fontsize"]
                self.fuente= self.config["fuente"]
            except json.decoder.JSONDecodeError:
                self.aplicardefecto()
                self.config=json.load(open("C:/Users/"f"{(self.user)}/Downloads/configln.json","r"))
                self.fontsize = self.config["fontsize"]
                self.fuente= self.config["fuente"]
        
        self.texto = tk.Text(self.wn)
        self.texto.configure(font=(self.fuente, self.fontsize, "normal"))
        self.wn.geometry("600x400")
        self.texto.pack()
        self.barramenu = tk.Menu(self.wn)
        self.Archivo = tk.Menu(self.barramenu, tearoff=0)
        self.estilo = tk.Menu(self.barramenu, tearoff=0)
        self.ayuda = tk.Menu(self.barramenu, tearoff=0)
        
        
        self.Archivo.add_command(label="Abrir", command=self.open)
        self.Archivo.add_command(label="Guardar", command=self.save)
        self.Archivo.add_command(label="Guardar como", command=self.saveas)
        self.Archivo.add_command(label="Salir", command=self.cerrarboton)
        self.estilo.add_command(label="Acercar", command=self.acercar)
        self.estilo.add_command(label="Alejar", command=self.alejar)
        self.estilo.add_command(label="Calibri", command=self.calibri)
        self.estilo.add_command(label="Consolas", command=self.console)
        self.estilo.add_command(label="Arial", command=self.arial)
        self.ayuda.add_command(label="Acerca de lueyoNotepad", command=self.help)
        self.barramenu.add_cascade(label="Archivo",menu=self.Archivo)
        self.barramenu.add_cascade(label="Estilo",menu=self.estilo)
        self.barramenu.add_cascade(label="Ayuda",menu=self.ayuda)
        self.wn.config(menu=self.barramenu)
        try:
            icono = tk.PhotoImage(file="C:/Users/"f"{(self.user)}/Downloads/icotext.png")
            self.wn.iconphoto(True, icono)
            self.wn.iconbitmap("C:/Users/"f"{(self.user)}/Downloads/icotext.ico")
        except tk.TclError:
            wget.download("https://i.imgur.com/moUHY8w.png")
            wget.download("https://images.uncyclomedia.co/inciclopedia/es/7/73/LueyoNotepad.ico")
            shutil.copy(f"{(self.currentdir)}/moUHY8w.png", "C:/Users/"f"{(self.user)}/Downloads/icotext.png")
            shutil.copy(f"{(self.currentdir)}/LueyoNotepad.ico", "C:/Users/"f"{(self.user)}/Downloads/icotext.ico")
            icono = tk.PhotoImage(file="C:/Users/"f"{(self.user)}/Downloads/icotext.png")
            self.wn.iconphoto(True, icono)
            self.wn.iconbitmap("C:/Users/"f"{(self.user)}/Downloads/icotext.ico")

        self.scrollbar = ttk.Scrollbar(self.wn,orient='vertical',command=self.texto.yview)
        #self.texto.grid(row=0, column=1)
        self.texto.pack( side = 'left', fill = 'both', expand=True)
        self.scrollbar.pack( side = 'right', fill = 'y' )
        self.scrollbar.config(command=self.texto.yview)
        self.texto.config(yscrollcommand=self.scrollbar)
        self.texto['yscrollcommand'] = self.scrollbar.set
        #self.scrollbar.grid(row=0, column=2, sticky='NS')
        self.wn.protocol("WM_DELETE_WINDOW",self.cerrar)
        self.abrircon()
        if len(argv)>1:
            self.wn.title("lueyoNotepad "+argv[1])
        else:            
            self.wn.title("lueyoNotepad")
        self.alturaactual=self.wn.winfo_reqheight()
        self.anchuraactual=self.wn.winfo_reqwidth()
        self.wn.mainloop()
    def save(self):
        files = [('All Files', '*.*'), 
                 ('Python Files', '*.py'),
                 ('Text Document', '*.txt')]
        
        if self.selected==False:
            self.ruta = asksaveasfilename(filetypes = files, defaultextension = files)
            #self.wn.title(self.ruta)
            #self.selected=True

        if not self.ruta:
            return
        else:
            self.wn.title("lueyoNotepad "+self.ruta)
            self.selected=True

        
        self.contenido = self.texto.get(1.0, tk.END)
        with open(str(self.ruta), 'wt', encoding='utf-8') as file1:
            file1.write(self.contenido)


    def calibri(self):
        
        self.fuente="Calibri"
        self.texto.configure(bd=0, font=(self.fuente))
        self.texto.pack( side = 'left', fill = 'both', expand=True)
        self.scrollbar.pack( side = 'right', fill = 'y' )
        self.texto['yscrollcommand'] = self.scrollbar.set

    def console(self):
        self.fuente="Consolas"
        self.texto.configure(bd=0, font=(self.fuente))
        self.texto.pack( side = 'left', fill = 'both', expand=True)
        self.scrollbar.pack( side = 'right', fill = 'y' )
        self.texto['yscrollcommand'] = self.scrollbar.set

    def arial(self):
        self.fuente="Arial"
        self.texto.configure(bd=0, font=(self.fuente))
        self.texto.pack( side = 'left', fill = 'both', expand=True)
        self.scrollbar.pack( side = 'right', fill = 'y' )
        self.texto['yscrollcommand'] = self.scrollbar.set
    
    def help(self):
        tk.messagebox.showinfo(title="versión 22.12.25", message="está usando la versión 22.12.25 de lueyoNotepad creado por lueyo")

    def acercar(self):
        #tk.messagebox.showinfo(title="En desarrollo", message="el vago de nuestro desarrollador se está tocando los huevos, vuelva el año que viene para usar esta opción")
        self.fontsize=self.fontsize+3
        self.alturaactual=self.wn.winfo_reqheight()
        self.anchuraactual=self.wn.winfo_reqwidth()
        self.texto.pack( side = 'left', fill = 'both', expand=True)
        self.scrollbar.pack( side = 'right', fill = 'y' )
        self.texto['yscrollcommand'] = self.scrollbar.set

        self.texto.configure(bd=0, font=(self.fuente, self.fontsize), width=self.anchuraactual, height=self.alturaactual)
        
    def alejar(self):
        #tk.messagebox.showinfo(title="En desarrollo", message="el vago de nuestro desarrollador se está tocando los huevos, vuelva el año que viene para usar esta opción")
        self.fontsize=self.fontsize-3
        self.alturaactual=self.wn.winfo_reqheight()
        self.anchuraactual=self.wn.winfo_reqwidth()
        self.texto.pack( side = 'left', fill = 'both', expand=True)
        self.scrollbar.pack( side = 'right', fill = 'y' )
        self.texto['yscrollcommand'] = self.scrollbar.set

        self.texto.configure(bd=0, font=(self.fuente, self.fontsize), width=self.anchuraactual, height=self.alturaactual)


    def cerrarboton(self):
        self.stop.set()
        self.saveconfig()
        self.wn.destroy()

    def cerrar(self):
        #print(self.texto.get(1.0, tk.END))
        
            

        self.respuestacerrar=tk.messagebox.askyesnocancel("¿Guardar?", "¿Quieres guardar antes de cerrar?", default="cancel")

        if self.respuestacerrar is True:
            self.save()
            if not self.ruta:
                pass
            else:
            
                self.stop.set()
                self.saveconfig()
                self.wn.destroy()
            #print("pilila")
                return self.stop.is_set()
        elif self.respuestacerrar is False:
            self.stop.set()
            self.saveconfig()
            self.wn.destroy()
            #print("pilila")
            return self.stop.is_set()
        elif self.respuestacerrar is None:
            pass
            
    def open(self):
        #print("abriendo")
        
        self.selected=False

        if self.selected==False:
            self.ruta = askopenfilename(filetypes=[('Archivo de texto', ('*.*'))])
            #self.wn.title(self.ruta)

        
            if not self.ruta:
                return
            else:
                self.selected=True
                self.wn.title("lueyoNotepad "+self.ruta)


        self.texto.delete(1.0, tk.END)

        with open(str(self.ruta), 'r', encoding='utf-8') as f:
            contenido = f.read()
            self.texto.insert(tk.END, contenido)


        #self.master.title(f'Editor de texto - {ruta2}')

        #self.contenido = self.texto.get(1.0, tk.END)

    def openarg(self):
        if self.selected==False:
            self.ruta = askopenfilename(filetypes=[('Archivo de texto', ('*.*'))])
            #self.wn.title(self.ruta)

        
            if not self.ruta:
                return
            else:
                self.selected=True
                self.wn.title("lueyoNotepad "+self.ruta)


        self.texto.delete(1.0, tk.END)

        with open(str(self.ruta), 'r', encoding='utf-8') as f:
            contenido = f.read()
            self.texto.insert(tk.END, contenido)


    def liskeys(self):

        hotkey = keyboard.HotKey(
        keyboard.HotKey.parse('<ctrl>+s'),
        self.teclas)

        
        
        with keyboard.Listener(on_press = self.teclas) as self.listener:
            
            
            
            self.listener.join()
                
            
            
    def abrircon(self):
        if len(argv)>1:
            #print(len(argv))
            self.ruta= argv[1]
            self.opened=True
            self.selected=True
            #print(self.ruta)
            self.openarg()
            

    def saveas(self):

        self.selected=False
        self.save()


        
    """ def presson(self,key):
        print(format(key)) """


    def teclas(self, key):
        #print(key)
        self.activewindow = gw.getActiveWindowTitle()
        #print(self.activewindow)
        

        if self.stop.is_set():
                    
            self.listener.stop()
            
        if "lueyoNotepad" in self.activewindow:

            if key == keyboard.KeyCode.from_char('\x13'):



                self.save()

            elif key == keyboard.KeyCode.from_char('\x0F'):


                self.open()

            elif key == keyboard.KeyCode.from_char('\x04'):

                #print("pilila")
                #self.selected=False
                self.saveas()

            elif key == keyboard.KeyCode.from_char('\x1d'):
            
            #print("pilila")
            #self.selected=False
                self.acercar
        
        """ elif key == keyboard.KeyCode.from_char('\x1d'):
            
            #print("pilila")
            self.fontsize= self.fontsize+1
            self.texto.configure(font=("Arial", self.fontsize, "normal"))

        elif key == keyboard.Key.ctrl_l and keyboard.KeyCode.from_char('-'):
            
            print("pilila")
            self.fontsize= self.fontsize-1
            self.texto.configure(font=("Arial", self.fontsize, "normal")) """

            

editor1=editor()
#editor1.ventana()
