#!/usr/bin/env python3
import os
import shutil
import json
from openai import OpenAI
from time import time

# Configuración de x.AI usando el módulo de openai
XAI_API_KEY = "API_KEY"
client = OpenAI(
    api_key=XAI_API_KEY,
    base_url="https://api.x.ai/v1",
)

api_queries = 0
tokens_consumed = 0

def load_instructions():
    try:
        with open('file_instructions.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        print("No se encontró el archivo 'file_instructions.json'.")
        return {}
    except json.JSONDecodeError:
        print("Error al decodificar JSON.")
        return {}

def query_xai(prompt):
    global api_queries, tokens_consumed
    completion = client.chat.completions.create(
        model="grok-2-1212",
        messages=[
            {"role": "system", "content": "Eres un asistente que clasifica archivos y sugiere su ubicación basada en directorios existentes y en instrucciones específicas para tipos de archivos. Devuelve un objeto JSON en texto plano, sin markdown, donde cada archivo tiene su 'oldname' y 'newpath'."},
            {"role": "user", "content": prompt}
        ]
    )
    api_queries += 1
    tokens_consumed += completion.usage.total_tokens
    return completion.choices[0].message.content

def process_files_in_batches(source_dir, destination_dir, additional_instructions, file_instructions, batch_size=10, max_retries=10):
    global api_queries, tokens_consumed
    files = []
    for root, _, filenames in os.walk(source_dir):
        for filename in filenames:
            relative_path = os.path.relpath(os.path.join(root, filename), source_dir)
            files.append(relative_path)

    total_files = len(files)
    processed_files = 0
    total_retries = 0

    start_time = time()
    
    api_queries = 0
    tokens_consumed = 0

    def update_progress_bar():
        percentage = (processed_files / total_files) * 100 if total_files else 100
        bar_length = 50 
        filled_length = int(bar_length * percentage // 100)
        bar = '=' * filled_length + '-' * (bar_length - filled_length)
        print(f'\rProgreso: [{bar}] {percentage:.1f}% ({processed_files}/{total_files}) archivos restantes: {total_files - processed_files}', end='', flush=True)

    def process_file_batch(batch):
        nonlocal processed_files, total_retries
        instructions_str = json.dumps(file_instructions)
        prompt = f"Lista de archivos a clasificar del directorio '{source_dir}': {batch}. Directorios disponibles en el directorio destino '{destination_dir}': {os.listdir(destination_dir)}. Instrucciones para tipos de archivos: {instructions_str}. Consideraciones adicionales: {additional_instructions}. Devuelve un objeto JSON estricto en texto plano donde cada archivo tenga una clave con su 'oldname' y 'newpath' (ruta completa en el directorio destino). Si el directorio de destino no existe, debe crearse. Solo usa directorios que existen en el destino o que se deben crear basados en los archivos. y solo envía estrictamente el objeto sin ningún otro texto que rompa el JSON, no uses markdown para la respuesta solo el objeto JSON"

        response = query_xai(prompt)
        try:
            start = response.find('{')
            end = response.rfind('}') + 1
            if start != -1 and end != 0:
                json_response = json.loads(response[start:end])
            else:
                print("La respuesta de la IA no contiene JSON válido.")
                return batch 

            failed_batch = []
            for oldname, file_info in json_response.items():
                if 'newpath' in file_info:
                    oldname_full = os.path.join(source_dir, oldname)
                    newpath = os.path.join(destination_dir, file_info['newpath'])
                    
                    try:
                        os.makedirs(os.path.dirname(newpath), exist_ok=True)
                        shutil.move(oldname_full, newpath)
                        processed_files += 1
                        update_progress_bar()
                    except Exception as e:
                        print(f"Ocurrió un error al mover {oldname}: {e}")
                        failed_batch.append(oldname)
                else:
                    print(f"Archivo {oldname} no tiene 'newpath' correctamente definido.")
                    failed_batch.append(oldname)
            return failed_batch
        except json.JSONDecodeError:
            return batch 

    failed_files = []
    retry_count = {file: 0 for file in files}

    update_progress_bar()
    while files or failed_files:
        if files:
            batch = files[:batch_size]
            files = files[batch_size:]
        else:
            batch = failed_files[:batch_size]
            failed_files = failed_files[batch_size:]

        failed_batch = process_file_batch(batch)
        
        for file in failed_batch:
            if retry_count[file] < max_retries:
                retry_count[file] += 1
                total_retries += 1
                failed_files.append(file)
            else:
                print(f"Archivo {file} excedió el número máximo de reintentos.")
        
        if not files and not failed_files:
            print("\nProceso completado.")
            print()  
            break

    total_time = time() - start_time
    print(
    f"Tiempo total de ejecución: {total_time:.2f} segundos\n"
    f"Número total de reintentos: {total_retries}\n"
    f"Total de queries a la API: {api_queries}\n"
    f"Total de tokens consumidos: {tokens_consumed}")

if __name__ == "__main__":
    source_dir = input("Introduce la ruta del directorio de origen: ")
    destination_dir = input("Introduce la ruta del directorio de destino: ")
    additional_instructions = input("Introduce instrucciones adicionales para la clasificación(Entrar para dejar en blanco): ")
    
    file_instructions = load_instructions()

    if os.path.exists(source_dir) and os.path.exists(destination_dir):
        process_files_in_batches(source_dir, destination_dir, additional_instructions, file_instructions)
    else:
        if not os.path.exists(source_dir):
            print(f"El directorio de origen {source_dir} no existe.")
        if not os.path.exists(destination_dir):
            print(f"El directorio de destino {destination_dir} no existe.")