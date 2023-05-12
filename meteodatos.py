#! /usr/bin/env-python
# -*- coding: utf-8 -*-

# meteodatos - librería para la consulta de datos meteorológicos obtenidos desde
# las bases de datos disponibles en https://climatologia.meteochile.gob.cl/application/index/menuTematicoEmas
# versión: 0.1
# fecha: abril de 2023
# github: cmoralesd/aprendiendo-python


def leer_archivo(nombre_archivo):
    # nombre_archivo: un archivo csv obtenido desde https://climatologia.meteochile.gob.cl/application/index/menuTematicoEmas
    # retorna: el contenido del archivo como una lista, cuyos elementos son las
    #          líneas del archivo original, sin el caracter final '\n'
    contenido = []
    try:
        with open(nombre_archivo) as archivo:
            for linea in archivo:
                contenido.append(linea[:-1])
        print(f'El archivo fue leido correctamente: {nombre_archivo}')
    except:
        print(f'ERROR: No se pudo abrir el archivo: {nombre_archivo}')
    return contenido  
    

def datos_registrados(datos):
    # parametros:
    #   datos[], es una lista con una fila de encabezado
    # retorna:
    #   una lista con los nombres encontrados en la fila de cabecera
    datos_encontrados = []
    for dato in datos[0].split(';'):
        datos_encontrados.append(dato)
    return datos_encontrados


def filtrar_cabecera(datos, filtro):
    # datos: la lista con los datos leidos desde el archivo csv
    # filtro: una variable 'str' con el nombre de cabecera que se desea filtrar
    # retorna: una lista con todas las filas de 'datos', pero conteniendo únicamente los datos bajo el nombre 'filtro'.
    #          Los datos que representan números están en formato numérico correspondiente (int o float)

    # identificamos el índice de columna para 'filtro'
    index = datos[0].split(';').index(filtro)
    datos_filtrados = []
    for fila in datos:
        valor = fila.split(';')[index]
        if valor.isnumeric():
            valor = int(valor)
        else:
            try:
                valor = float(valor)
            except:
                pass
        datos_filtrados.append(valor)     
    return datos_filtrados
        
 
def filtrar_dia(datos, dia):
    # datos: una lista cuyas filas contienen los datos agrupados como una cadena de texto
    # dia:   el día que se desea filtrar, en formato 'AAAA-MM-DD', ejemplo: '2023-03-01'
    # retorna: la misma lista 'datos', pero conteniendo únicamente las filas
    #          que coinciden con 'dia' y manteniendo la cabecera
    
    filtrados = []
    for fila in datos:
        # separamos los datos en cada fila para verificar la fecha ingresada en 'dia' está en 'momento'
        # (la fecha podría aparecer en otro campo, pero solo nos interesa 'momento')
        if dia in fila.split(';')[3]:
            filtrados.append(fila)
    # se agrega la fila de cabecera
    filtrados.insert(0, datos[0])
    return filtrados


def estadisticas_dia(datos, dia):
    # datos: una lista con datos leidos desde la base de datos meteorológicos,
    #        mediante la función 'leer_archivo()'
    # dia:   el día que se desea reportar, en formato 'AAAA-MM-DD', ejemplo: '2023-03-01'
    # retorna: tmax, tmin, tmedia, la temperatura máxima, mínima y promedio para el día.
    
    tmax = tmin = tmedia = 0
    # primero eliminamos todas las filas que no correspondan a 'dia'
    filtro_dia = filtrar_dia(datos, dia)
    # luego filtramos para dejar solo la columna 'ts'
    filtro_t = filtrar_cabecera(filtro_dia, 'ts')
    # finalmente eliminamos la cabecera y calculamos las estadisticas
    t = filtro_t[1:]
    tmax = max(t)
    tmin = min(t)
    tmedia = round(sum(t)/len(t), 1)
    
    return tmax, tmin, tmedia
    
  
