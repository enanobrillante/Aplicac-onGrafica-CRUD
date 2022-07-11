from tkinter import * #libreria para graficos
from tkinter import messagebox # libreria para mensajes emergentes al usuario
import sqlite3 #para trabajar con bases de datos

#---------------------FUNCIONES--------------------------

def conexionBBDD(): #asosiar esta funcion en el menu correspondiente
	miConexion=sqlite3.connect("Usuarios")

	miCursor=miConexion.cursor()

	try: #al querer volver a crear una base de datos, no entra al try y va a l except ya que la base de datos ya habia sido creada
  
		miCursor.execute('''
			CREATE TABLE DATOS_USUARIOS (
			ID INTEGER PRIMARY KEY AUTOINCREMENT,
			NOMBRE_USUARIO VARCHAR(50),
			PASSWORD VARCHAR(50),
			APELLIDO VARCHAR(15),
			DIRECCION VARCHAR (50),
			COMENTARIOS VARCHAR(100)) 
			''')
	    
		messagebox.showinfo("BBDD","BBDD creada con éxito") #titulo de la ventana y texto interno
    
	except:
        
		messagebox.showwarning("Atención","¡La base de datos ya existe!")

def salirAplicacion():

	valor=messagebox.askquestion("Salir","¿Desea salir de la aplicación?")
	if valor=="yes": #evaluamos si el usuario ha pulsado "si"
		root.destroy() #destruye el programa


def limpiaCampos():

	miNombre.set("") #se setean en blanco los entry,, que fueron asignados a variables
	miID.set("")
	miApellido.set("")
	miPassword.set("")
	miDireccion.set("")
	#se utiliza el metodo delete para borrar el contenido de un cuadro de texto
	textoComentario.delete(1.0,END) #borra desde punto de partida 1.0 ,desde el primer caracter hasta el final

def crear():

	miConexion=sqlite3.connect("Usuarios") #el nombre de la BBDD será Usuarios

	miCursor=miConexion.cursor()
	#la instruccion sql guardará lo que haya en cada entry

	#Se toman los valores introducidos en los cuadros de texto
	#El primer dato de la tabla en NULL para que sea AUTOINCREMENT

	"""miCursor.execute("INSERT INTO DATOS_USUARIOS VALUES(NULL,'" + miNombre.get()+ "',
		'" + miPassword.get()+ "',
		'" + miApellido.get()+ "',
		'" + miDireccion.get()+"',
		'" + textoComentario.get("1.0",END)+"')" )"""
	


	#se reemplaza la consulta anterior, por una consulta paramétrica
	#Las consultas parametricas evitan la INYECCION SQL !!!


	datos=miNombre.get(),miPassword.get(),miApellido.get(),miDireccion.get(),textoComentario.get("1.0",END)
	#se almacena toda la info de esos campos en la variable datos

	miCursor.execute("INSERT INTO DATOS_USUARIOS VALUES(NULL,?,?,?,?,?)",(datos)) #el primero es null por que es el id que es primary key autoincrementable
	#el segundo parametro pasado a execute es "datos" que es la variable doode se almacenan todos los datos


	miConexion.commit() #para que ejecute la instruccion inster into

	messagebox.showinfo("BBDD","Registro agregado con éxito")


def LeerRegistros():

	textoComentario.delete("1.0",END)
	
	miConexion=sqlite3.connect("Usuarios") #creamos la conexion con la BBDD

	miCursor=miConexion.cursor() #creamos el puntero

	miCursor.execute("SELECT * FROM DATOS_USUARIOS WHERE ID = " + miID.get())


	#extraer la informacion de esta consulta
	elUsuario=miCursor.fetchall() #devuelve array con el registro, de toda la fila.
	#debe recorrerse ese array por posiciones, ya que en cada posicion se encuentra cada valor de la respectiva columna de la tabla
	if elUsuario==[]:
		messagebox.showinfo("Atención","El Registro no existe en la BBDD")
	else:	
		for usuario in elUsuario: #el posicion 0=ID, 1=Nombre, 2=Password, 3=Apellido, 4=Comentarios

			miID.set(usuario[0]) #se va rescatando por posicion del array
			miNombre.set(usuario[1])
			miPassword.set(usuario[2]) # el password deberia ser informacion encriptada, el creador no tendria que verlo ni desde la base de datos
			miApellido.set(usuario[3])
			miDireccion.set(usuario[4])
			textoComentario.insert(1.0,usuario[5]) #insert por que es un texto

	miConexion.commit() #para que se ejecute todo


def Actualizar():

	miConexion=sqlite3.connect("Usuarios")

	miCursor=miConexion.cursor()
	#la instruccion sql guardará lo que haya en cada entry

	"""miCursor.execute("UPDATE DATOS_USUARIOS SET NOMBRE_USUARIO='"+ miNombre.get() +
		"',PASSWORD='" + miPassword.get()+
		"',APELLIDO='" + miApellido.get()+
		"',DIRECCION='" + miDireccion.get()+
		"',COMENTARIOS='" + textoComentario.get("1.0",END)+
		"'WHERE ID=" + miID.get())"""

	#Utilizando una consulta paramétrica

	datos=miNombre.get(),miPassword.get(),miDireccion.get(),miApellido.get(),textoComentario.get("1.0",END)

	miCursor.execute("UPDATE DATOS_USUARIOS SET NOMBRE_USUARIO=?,PASSWORD=?,APELLIDO=?,DIRECCION=?,COMENTARIOS=?" +
		"WHERE ID="+ miID.get(),(datos))

	miConexion.commit() #para que ejecute la instruccion inster into

	messagebox.showinfo("BBDD","Registro actualizado con éxito")


def EliminarRegistro ():

	miConexion=sqlite3.connect("Usuarios")

	miCursor=miConexion.cursor()

	miCursor.execute("DELETE FROM DATOS_USUARIOS WHERE ID=" + miID.get())

	miConexion.commit()

	limpiaCampos()

	messagebox.showinfo("BBDD","Registro eliminado con éxito")


#---------------------------------------------------------

root=Tk() #llamamos a la clase TK
root.title("Gestión Base de datos")


#------------------CONSTRUCCION BARRA MENU----------------

barraMenu=Menu(root)#menu que cuelga de la raiz
barraMenu.config(bg="blue")
root.config(menu=barraMenu,width=450,height=600) #configuracion del menu
#root.config(bg="coral")
root.resizable(0,0)

#ahora se incluyen los elementos de la barra menu
BBDDmenu=Menu(barraMenu, tearoff=0) #estara dentro de la barra menu y tearoff para quitar lineas en la barra menu#elementos de BBDDmenu
BBDDmenu.add_command(label="Conectar",command=conexionBBDD)#para crear y conectar la base de datos
BBDDmenu.add_command(label="Salir",command=salirAplicacion)#para salir

borrarmenu=Menu(barraMenu, tearoff=0)
borrarmenu.add_command(label="Borrar campos", command=limpiaCampos)

CRUDmenu=Menu(barraMenu, tearoff=0)
CRUDmenu.add_command(label="Crear",command=crear)
CRUDmenu.add_command(label="Leer",command=LeerRegistros)
CRUDmenu.add_command(label="Actualizar",command=Actualizar)
CRUDmenu.add_command(label="Borrar",command=EliminarRegistro)

ayudamenu=Menu(barraMenu, tearoff=0)
ayudamenu.add_command(label="Licencia")
ayudamenu.add_command(label="Acerca de...")

#Agregamos los 4 elementos a la barra de menu principal 

barraMenu.add_cascade(label="BBDD", menu=BBDDmenu) #nuestra barra menu tiene que agregar un menu con la etiqueta label 
barraMenu.add_cascade(label="Borrar", menu=borrarmenu)
barraMenu.add_cascade(label="CRUD", menu=CRUDmenu)
barraMenu.add_cascade(label="Ayuda", menu=ayudamenu)

#------------FRAME PARA construccion de Cuadros--------

miFrame=Frame(root) #el frame estara dentro de la raiz
miFrame.pack()



#usamos la funcion StringVar con todos los entry para poder obtener la cadena de caracteres de cada entry.
miID=StringVar() 
miNombre=StringVar()
miApellido=StringVar()
miPassword=StringVar()
miDireccion=StringVar()


cuadroID=Entry(miFrame,textvariable=miID) #con esto le decimos a la aplicacin que hay una cadena de caracteres en cada entry
cuadroID.grid(row=0,column=1,padx=10,pady=10)
#row es fila 0 y column 1...separacion entre elementos con padx y pady
cuadroNombre=Entry(miFrame,textvariable=miNombre) # textvariable, se le asigna miNombre que es StringVar,para luego poder extraer la informacion ingresada por el 
#ususario en el cuadro de texto
cuadroNombre.grid(row=1,column=1,padx=10,pady=10)
cuadroNombre.config(fg="red", justify="right") # cambiamos el color del texto y el alineado con justify


cuadroPassword=Entry(miFrame, textvariable=miPassword)
cuadroPassword.grid(row=2,column=1,padx=10,pady=10)
cuadroPassword.config(show="*") #cuando se escriba la contraseña apareceran los asteriscos

cuadroApellido=Entry(miFrame,textvariable=miApellido)
cuadroApellido.grid(row=3,column=1,padx=10,pady=10)

cuadroDireccion=Entry(miFrame,textvariable=miDireccion)
cuadroDireccion.grid(row=4,column=1,padx=10,pady=10)

textoComentario=Text(miFrame, width=16, height=5) #area de texto
textoComentario.grid(row=5,column=1,padx=10,pady=10)
scrollVert=Scrollbar(miFrame, command=textoComentario.yview)
#el command le da accion, y el yview desplaza en el eje vertical el texto
scrollVert.grid(row=5,column=2,sticky="nsew") #stiky es para ubicar el scroll mejor

textoComentario.config(yscrollcommand=scrollVert.set) #le decimos a textocomentario que la barra de dezplazamiento le pertenece

#----------------------------CONSTRUCCION DE LABELS--------------------


IDlabel=Label(miFrame,text="Id:")
IDlabel.grid(row=0,column=0,sticky="e", padx=10,pady=10) #sticky e (este)

Nombrelabel=Label(miFrame,text="Nombre:")
Nombrelabel.grid(row=1,column=0,sticky="e", padx=10,pady=10)

Passwordlabel=Label(miFrame,text="Password:")
Passwordlabel.grid(row=2,column=0,sticky="e", padx=10,pady=10)

Apellidolabel=Label(miFrame,text="Apellido:")
Apellidolabel.grid(row=3,column=0,sticky="e", padx=10,pady=10)

Direccionlabel=Label(miFrame,text="Dirección:")
Direccionlabel.grid(row=4,column=0,sticky="e", padx=10,pady=10)

Comentarioslabel=Label(miFrame,text="Comentarios:")
Comentarioslabel.grid(row=5,column=0,sticky="e", padx=10,pady=10)

#-----------------------BOTONES---------------------------

miFrame2=Frame(root)
miFrame2.pack()

botonCrear=Button(miFrame2, text="Create", command=crear)
botonCrear.grid(row=1, column=0,sticky="e", padx=10,pady=10)

botonLeer=Button(miFrame2, text="Read",command=LeerRegistros)
botonLeer.grid(row=1, column=1,sticky="e", padx=10,pady=10)

botonActualizar=Button(miFrame2, text="Update",command=Actualizar)
botonActualizar.grid(row=1, column=2,sticky="e", padx=10,pady=10)

botonBorrar=Button(miFrame2, text="Delete",command=EliminarRegistro)
botonBorrar.grid(row=1, column=3,sticky="e", padx=10,pady=10)








root.mainloop() #metodo mainloop mantiene la ventana abierta

