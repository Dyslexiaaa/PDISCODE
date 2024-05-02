import time
import os

files_path = "./docs/"
documents_files = os.path.join(files_path, "documents.txt")
dictionary_files = os.path.join(files_path, "dictionary.txt")
posting_files = os.path.join(files_path, "posting.txt")
posting_weight_files = os.path.join(files_path, "posting_weight.txt")

# Funcion para preguntar al usuario y buscar conforme los archivos los resultados que da


def game_search():

    enter = input("Inserta una palabra que quieras buscar: ")

    while not enter.strip():
        enter = input("Tienes que insertar una palabra: ")

    print(f"El valor insertado del usuario es {enter}")


game_search()
