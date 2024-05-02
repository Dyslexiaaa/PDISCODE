import os
import re
import time
# Definimos el comienzo del proceso general
original_start = time.time()
# Definimos todas las rutas que el programa va a usar
path_files_words = "./HtmlFilesWithArangedWords/"
path_tokens = "./TokenizedOutputFiles/consolidated_tokens.html"
general_path_docs = "../WeightTokens/docs/"

# Creamos rutas compuestas más compuestas para que el programa las
# pueda usar
time_file = os.path.join(general_path_docs, "a11_2967915.txt")
file_posting = os.path.join(general_path_docs, "posting.txt")
files_dictionary = os.path.join(general_path_docs, "dictionary.txt")
file_documents = os.path.join(general_path_docs, "documents.txt")
# Agregamos este archivo que va a almacenar la lista de las palabras despues
# del filtrado
stop_file = os.path.join(general_path_docs, "stop_list.txt")
posting_weight = os.path.join(general_path_docs, "posting_weight.txt")
results = {}
# Esta es solamante para que cada que se ejecute, en vez de crear siempre los archivos
# solamente eliminar el posting y el dicionario en caso de que sean creados


def isPostingandDictionaryCreated(file_posting, files_dictionary, stop_file, posting_weight):

    if os.path.exists(file_posting):
        os.remove(file_posting)
    if os.path.exists(files_dictionary):
        os.remove(files_dictionary)
    if os.path.exists(stop_file):
        os.remove(stop_file)
    if os.path.exists(posting_weight):
        os.remove(posting_weight)
    if os.path.exists(file_documents):
        os.remove(file_documents)

    with open(file_posting, "w"):
        pass

    with open(files_dictionary, "w"):
        pass

    with open(stop_file, "w"):
        pass

    with open(posting_weight, "w"):
        pass

    with open(file_documents, 'w'):
        pass

# Aqui nos encargamos de que el archivo de diccionario se cree
# CAMBIO, aqui tambien vamos a agregar el proceso de filtrado
# que tendra el archivo stop_file confome desarollamos el archivo
# se explicara donde se hace esta parte


def dictionary(pos):
    # Primero nos cersioramos de refrescar los archivos que se tienen
    isPostingandDictionaryCreated(
        file_posting, files_dictionary, stop_file, posting_weight)
    # Hacemos la lectura del archivo importante para filtrar las palabras
    stop_list_path = os.path.join(general_path_docs, 'StopListWords.txt')
    # Lo abrimos y almacenamos las palabras en un objeto
    with open(stop_list_path, "r") as stop_list_file:
        stop_list_words = set(word.strip() for word in stop_list_file)
    # Declaramos una variable que sera una estructura de datos similar
    # a una lista
    not_found_tokens = set()

    # Definimos la frecuencia minima de las palabras a filtrar,
    # en este caso queremos que sea 5
    min_frequency = 5
    # Definimos la hashtable donde guardaremos los tokens para procesarlos
    tokens_dict = {}
    # Abrimos el diccionario de palabras que teniamos desde la actividad 6
    with open(path_tokens, "r", encoding='utf-8') as dictionaryInit:
        with open(files_dictionary, "w", encoding='utf-8') as dictionaryFinal:
            # Por cada linea del diccionario
            for line in dictionaryInit:
                # Que mantenga esta estructura, re es una libreria que sirve
                # para encontrar patrones dentro de cadenas de caracteres
                match = re.search(r"(.*): \d+ \| (\d+)", line)
                # Si tenemos una linea con esta estructura de separacion
                if match:
                    # Obtenemos sus partes, que es el token, la cantidad de
                    # archivos en los que se encuentra.
                    token = match.group(1).strip()
                    files_cant = match.group(2).strip()
                    # Escribimos esto en el archivo final asi como su posicion
                    dictionaryFinal.write(f"{token}: {files_cant}: {pos}\n")
                    # Y le sumamos a la posicion la cantidad de archivos en las
                    # que se encuentra este token
                    pos += int(files_cant)
                    # Tambien almacenamos toda esta informacion en un diccionario
                    # para su procesamiento en la funcion posting
                    tokens_dict[token] = {
                        'files_cant': int(files_cant), 'pos': pos}
                    # CAMBIO: Aqui ocurre el filtrado, donde se indica que si el
                    # token no se encuentra en alguna de la lista de filtrado,
                    # tiene una longitud mayor a 1 letra y su frecuencia es minimo
                    # 5 entonces se almacenara en la lista que definimos anterior
                    # mente.
                    if token not in stop_list_words and int(files_cant) > min_frequency and len(token) > 1:
                        not_found_tokens.add(token)
    # Almacenamos todos estos tokens filtrados en el archivo que definimos
    # desde el inicio del programa.
    with open(stop_file, 'w') as stopfile:
        for token in not_found_tokens:
            stopfile.write(f"{token} \n")
    return tokens_dict

# Agregamos esta funcion para poder hacer el output de documentos.
# se hace el proceso de indexación para los documentos


def documents():
    id_file = 1
    html_files = [f for f in os.listdir(
        path_files_words) if f.endswith('.html')]
    with open(file_documents, 'w') as fd:
        for file in html_files:
            fd.write(f"{id_file} {file}\n")
            id_file += 1


# Aqui definimos y procesamos los datos para encontrar sus frecuencias
# en los archivos.path_files_words


def posting(tokens_dict, directory_path):
    # Definimos un objeto de resultados en los cuales
    # los procesamientos definidos
    results = {token: {} for token in tokens_dict}
    # Construir el mapeo de IDs
    mapeo_ids = {}
    with open(file_documents, 'r') as ad:
        for line in ad:
            id, name = line.strip().split()
            mapeo_ids[name] = id
    # Recorremos el directorio general de los archivos
    for root, dirs, files in os.walk(directory_path):
        # Por cada archivo en los archivos
        for file_name in files:
            # Si el archivo es un HTML
            if file_name.endswith('.html'):
                # Definimos el file_path del archivo para imprimirlo
                # en el tiempo
                file_path = os.path.join(root, file_name)
                # Iniciamos el cronometro del procesamiento
                start = time.time()
                # Abrimos el HTML
                with open(os.path.join(root, file_name), 'r', encoding='utf-8') as file:
                    # Por cada linea en el HTML
                    for line in file:
                        # Separamos las lineas por palabras
                        words = line.strip().split()
                        # Por cada palabra en nuestra lista de palabras del
                        # archivo
                        for word in words:
                            # Si la palabra se encuentra en el diccionario que
                            # procesamos
                            if word in tokens_dict:
                                # Lo relacionamos con el archivo que tiene
                                # la palabra, si tiene más se le sumará
                                # si la frecuencia es solamante uno entonces
                                # muy probablemente solamente se encuentra
                                # en un archivo
                                if file_name in results[word]:
                                    results[word][file_name] += 1
                                else:
                                    results[word][file_name] = 1
                # Finalizamos el cronometro
                end = time.time()
                # Definimos el tiempo que tardo en procesar todos los archivos
                elapsed_time = end - start
                # Abrimos el archivo donde imprimiremos los tiempos
                with open(time_file, 'a') as f:
                    f.write(f"{file_path}                {elapsed_time} \n")

    # Ordenar los tokens basados en el valor de posición en el diccionario
    ordered_tokens = sorted(
        tokens_dict.keys(), key=lambda x: tokens_dict[x]['pos'])

    # Dentro del file posting registramos los resultados que tenemos guardados
    with open(file_posting, 'w') as f:
        for token in ordered_tokens:
            files_data = results[token]
            if files_data:  # Verificar si hay al menos una ocurrencia en los archivos
                for file_name, frequency in files_data.items():
                    # Actualizar el ID según el mapeo
                    id_actualizado = mapeo_ids.get(file_name, file_name)
                    f.write(f"{id_actualizado}: {frequency}\n")

    # Crear un nuevo metodo posting2.txt que contenga el tf-idf (Actividad 10)
    with open(posting_weight, 'w') as f:
        for token in ordered_tokens:
            files_data = results[token]
            if files_data:  # Verificar si hay al menos una ocurrencia en los archivos
                for file_name, frequency in files_data.items():
                    total_tokens = sum(files_data.values())
                    tf_idf = (frequency * 100) / total_tokens
                    # Actualizar el ID según el mapeo
                    id_actualizado = mapeo_ids.get(file_name, file_name)
                    f.write(f"{id_actualizado} : {tf_idf}\n")


# Esta seccion es la ejecucion de todas las funciones y la finalizacion del
# cronometro para poder registrar el tiempo que se tardo todo el proceso.
tokens_dict = dictionary(0)
documents()
posting(tokens_dict, path_files_words)
ending_time = time.time()

with open(time_file, 'a') as f:
    f.write(
        f"El tiempo total que se tardo en ejecutar todo el proceso es de: {float(ending_time - original_start)}")
