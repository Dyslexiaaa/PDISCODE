# importamos librerías necesarias
import sys
import time

# funcion para buscar palabras en el diccionario


def retrieve_word(words):

    # abrimos el diccionario en modo lectura y codificación utf-8
    with open('docs/dictionary.txt', 'r', encoding='utf-8') as f:
        # leemos el diccionario y lo guardamos en una lista, separando por los dos puntos
        dictionary = [line.split(":")[0] for line in f.read().splitlines()]

    # abrimos el archivo posting en modo lectura y codificación utf-8
    with open('docs/documents.txt', 'r', encoding='utf-8') as f:
        # leemos los documentos y los guardamos en una lista, separando por saltos de línea
        documents = f.read().splitlines()

    # abrimos el archivo posting en modo lectura y codificación utf-8
    with open('docs/posting.txt', 'r', encoding='utf-8') as f:
        # leemos los postings y los guardamos en una lista, separando por saltos de línea
        postings = f.read().splitlines()

    # creamos una lista con las palabras que no se encontraron en el diccionario
    words_not_found = [word for word in words if word not in dictionary]
    # si la lista no está vacía, imprimimos las palabras que no se encontraron en el diccionario
    if words_not_found:
        # imprimimos las palabras que no se encontraron en el diccionario
        print(f'The words {words_not_found} are not in the dictionary.')
        return

    # creamos una lista con los índices de las palabras en el diccionario
    word_indices = [dictionary.index(word) for word in words]
    # creamos un conjunto con los índices de los documentos que contienen las palabras buscadas
    doc_indices = set(int(p.split(':')[
                      0]) for word_index in word_indices for p in postings[word_index].split(','))
    # LOGICA DEL TOP 10
    # Creamos un diccionario para almacenar la frecuencia de los documentos que contienen las palabras buscadas
    doc_frequency = {}

    # Iteramos sobre las palabras buscadas
    for word in words:
        # Obtenemos el índice de la palabra en el diccionario
        word_index = dictionary.index(word)
        # Obtenemos los documentos que contienen la palabra
        docs_containing_word = postings[word_index].split(',')
        # Actualizamos la frecuencia de cada documento
        for doc_info in docs_containing_word:
            doc_index, frequency = doc_info.split(':')
            doc_index = int(doc_index)
            frequency = int(frequency)
            doc_frequency[doc_index] = doc_frequency.get(
                doc_index, 0) + frequency

    # Ordenamos los documentos por frecuencia de mayor a menor
    sorted_docs = sorted(doc_frequency.items(),
                         key=lambda x: x[1], reverse=True)

    # Mostramos los 10 documentos más frecuentes
    print(f'Top 10 documents where the words {words} are found:')
    for doc_index, frequency in sorted_docs[:10]:
        print(
            f'Document: {documents[doc_index]} (Frequency: {frequency})')


# si el script se ejecuta directamente, se ejecuta la función retrieve_word, pasando como argumento las palabras ingresadas por el usuario
if __name__ == "__main__":

    # si no se ingresan palabras, se imprime un mensaje de uso y se sale del script (parecido a un try catch)
    if len(sys.argv) < 2:
        print('Usage: python find_word.py <word> [<word> ...]')
        sys.exit(1)

    # se toma el tiempo de inicio
    start_time = time.time()
    retrieve_word(sys.argv[1:])
    end_time = time.time()

    # se calcula el tiempo transcurrido
    elapsed_time = end_time - start_time

    # se escribe el tiempo transcurrido en un archivo de texto ya existente o se crea uno nuevo
    with open('docs/a13_2758861.txt', 'w') as f:
        f.write(f'Time taken: {elapsed_time} seconds\n')
