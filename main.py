# Importamos las librerías necesarias
import tkinter as tk
from PIL import Image, ImageTk
from urllib.request import urlopen
import requests
from tkinter import Label
import json
from openai import OpenAI
from api_key_opeanai import APY_KEY

# Función para obtener los datos de un pokemon desde la API
def url_api(pokemon):
    url = f"https://pokeapi.co/api/v2/pokemon/{pokemon}"
    respuesta = requests.get(url)

    if respuesta.status_code != 200:
        print("Ha ocurrido un error, intenta nuevamente.")
        exit()

    datos = respuesta.json()

    return datos

# Función para obtener y mostrar la imagen del pokemon
def imagen():
    url_imagen_pokemon = datos["sprites"]["front_default"]
    imagen_pokemon = Image.open(urlopen(url_imagen_pokemon))
    imagen_redimensionada = imagen_pokemon.resize((250, 250))
    renderizado_imagen = ImageTk.PhotoImage(imagen_redimensionada)

    etiqueta_imagen_pokemon = Label(ventana, image=renderizado_imagen)
    etiqueta_imagen_pokemon.image = renderizado_imagen
    etiqueta_imagen_pokemon.place(relheight=.5, relwidth=1)
    etiqueta_imagen_pokemon.config(borderwidth=2, relief="solid",
                                   highlightthickness=10, highlightcolor='#E1D601',
                                   bg="light goldenrod")
    
    boton = tk.Button(ventana, text=" i ", command=dato_curioso)
    boton.config(bg='gold')
    boton.place(x=290, y=18)
    
    return url_imagen_pokemon

# Función para obtener y mostrar los datos del pokemon
def datos_pokemon():
    url_nombre = datos['name']
    altura = datos['height']
    peso = datos['weight']
    num_movimientos = len(datos['moves'])

    nombre_habilidades = []
    for i in range(len(datos['abilities'])):
        habilidades = datos['abilities'][i]['ability']['name']
        nombre_habilidades.append(habilidades)

    nombre_tipos = []
    for i in range(len(datos['types'])):
        tipos = datos['types'][i]['type']['name']
        nombre_tipos.append(tipos)
    
    mensaje = tk.Text(ventana, background="white", width=37, height=12)
    mensaje.place(x=12.5, y=229)
    mensaje.insert(tk.INSERT, f"Nombre: {url_nombre}\n")
    mensaje.insert(tk.INSERT, f"\nAltura: {altura}\n")
    mensaje.insert(tk.INSERT, f"\nPeso: {peso}\n")
    mensaje.insert(tk.INSERT, f"\nNumero de movimientos: {num_movimientos}\n")
    mensaje.insert(tk.INSERT, f"\nHabilidades: {nombre_habilidades}\n")
    mensaje.insert(tk.INSERT, f"\nTipos: {nombre_tipos}")

    return url_nombre, altura, peso, num_movimientos, nombre_habilidades, nombre_tipos

# Función para obtener un dato curioso del pokemon usando OpenAI
def dato_curioso():
    ventana_top = tk.Toplevel(ventana)
    ventana_top.title("Dato curioso")
    ventana_top.geometry("250x200")
    ventana_top.resizable(False, False)
    ventana_top.config(bg="gold")

    url_nombre, altura, peso, num_movimientos, nombre_habilidades, nombre_tipos = datos_pokemon()

    client = OpenAI(api_key = APY_KEY)

    modelo = 'gpt-3.5-turbo-0125'
    prompt = f"Dame un dato curioso de {url_nombre}"

    mensajes = [
        {'role': 'system', 'content': 'dame una respusta corta'},
        {'role': 'user', 'content': prompt}
    ]

    respuesta = client.chat.completions.create(
        model = modelo,
        messages = mensajes,
        max_tokens = 1000
    )

    dato = tk.Text(ventana_top, background="light yellow", width=28, height=11)
    dato.place(x=10, y=10)
    dato.insert(tk.INSERT, f"Dato Curioso: \n\n{respuesta.choices[0].message.content}")

# Función para guardar los datos del pokemon en un archivo JSON
def archivo_jason():
    url_nombre, altura, peso, num_movimientos, nombre_habilidades, nombre_tipos = datos_pokemon()
    url_imagen_pokemon = imagen()

    informacion = {}
    informacion['pokemons'] = []
    informacion['pokemons'].append({
        'nombre': url_nombre,
        'altura': altura,
        'peso': peso,
        'movimientos': num_movimientos,
        'habilidades': nombre_habilidades,
        'tipos': nombre_tipos,
        'imagen': url_imagen_pokemon
    })

    with open(f'pokedex/informacion_{url_nombre}.json', 'w') as file:
        json.dump(informacion, file, indent=4)

# Solicitamos al usuario el nombre del pokemon
datos = url_api(input("Ingrese el nombre del pokemon: "))

# Configuramos la ventana principal
ventana = tk.Tk()
icono = tk.PhotoImage(file="icon/R.png")
ventana.iconphoto(True, icono)
ventana.title("Pokedex")
ventana.geometry("350x460")
ventana.resizable(False, False)
ventana.config(borderwidth=2, relief="solid", highlightthickness=10, highlightcolor='#E1D601', bg="#E9A04D")

# Llamamos a las funciones para mostrar la imagen, los datos y guardarlos en un archivo JSON
imagen()
datos_pokemon()
archivo_jason()

# Iniciamos el bucle principal de la ventana
ventana.mainloop()