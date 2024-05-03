#importamos librerías necesarias
import sys
import time

#funcion para buscar palabras en el diccionario
def retrieve_word(words):

    #abrimos el diccionario en modo lectura y codificación utf-8
    with open('docs/dictionary.txt', 'r', encoding='utf-8') as f: 
        #leemos el diccionario y lo guardamos en una lista, separando por los dos puntos
        dictionary = [line.split(":")[0] for line in f.read().splitlines()] 

    #abrimos el archivo posting en modo lectura y codificación utf-8
    with open('docs/documents.txt', 'r', encoding='utf-8') as f:
        #leemos los documentos y los guardamos en una lista, separando por saltos de línea
        documents = f.read().splitlines()

    #abrimos el archivo posting en modo lectura y codificación utf-8
    with open('docs/posting.txt', 'r', encoding='utf-8') as f:
        #leemos los postings y los guardamos en una lista, separando por saltos de línea
        postings = f.read().splitlines()

    #creamos una lista con las palabras que no se encontraron en el diccionario
    words_not_found = [word for word in words if word not in dictionary]
    #si la lista no está vacía, imprimimos las palabras que no se encontraron en el diccionario
    if words_not_found:
        #imprimimos las palabras que no se encontraron en el diccionario
        print(f'The words {words_not_found} are not in the dictionary.')
        return

    #creamos una lista con los índices de las palabras en el diccionario
    word_indices = [dictionary.index(word) for word in words]
    #creamos un conjunto con los índices de los documentos que contienen las palabras buscadas
    doc_indices = set(int(p.split(':')[0]) for word_index in word_indices for p in postings[word_index].split(','))

    #imprimimos los documentos que contienen las palabras buscadas
    print(f'The words {words} are found in the following documents:')
    for i in doc_indices:
        print(documents[i])

#si el script se ejecuta directamente, se ejecuta la función retrieve_word, pasando como argumento las palabras ingresadas por el usuario
if __name__ == "__main__":
    
    #si no se ingresan palabras, se imprime un mensaje de uso y se sale del script (parecido a un try catch)
    if len(sys.argv) < 2:
        print('Usage: python find_word.py <word> [<word> ...]')
        sys.exit(1)

    #se toma el tiempo de inicio
    start_time = time.time()
    retrieve_word(sys.argv[1:])
    end_time = time.time()

    #se calcula el tiempo transcurrido
    elapsed_time = end_time - start_time

    #se escribe el tiempo transcurrido en un archivo de texto ya existente o se crea uno nuevo
    with open('docs/a12_2758861.txt', 'w') as f:
        f.write(f'Time taken: {elapsed_time} seconds\n')