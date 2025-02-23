from collections import OrderedDict
import json
import os
import sys

# Diretórios
en_dir = "EN"
cn_dir = "CN"
jp_dir = "JP"
kr_dir = "KR"
es_dir = "ES"
localization_dir = "Localize"

# Contador para IDs -1
eikefelipe_counter = 1

def replace_negative_id(key, eikefelipe_counter, last_idx=0):
    """
    Substitui o ID -1 por eikefelipeN, onde N é um número sequencial.
    Remove completamente o -1 do key.
    """
    if "-0001-" in key:
        # Substitui -1 por eikefelipeN e remove o -1 restante
        new_key = f"{last_idx:0000}eikefelipe{eikefelipe_counter}-{key.split('-0001-', 1)[1]}"
        eikefelipe_counter += 1
        return new_key, eikefelipe_counter
    return key, eikefelipe_counter

# Adicionar função para exibir a barra de progresso sem bibliotecas
def print_progress(current, total, bar_length=40):
    percent = current / total if total else 0
    filled_length = int(round(bar_length * percent))
    bar = '=' * filled_length + '-' * (bar_length - filled_length)
    sys.stdout.write(f'\rProgresso: |{bar}| {int(percent*100)}%')
    sys.stdout.flush()
 
# Configurar barra de progresso: contar total de arquivos JSON na pasta EN
total_files = sum(
    1 for root, _, files in os.walk(en_dir) for file in files if file.endswith(".json")
)
file_counter = 0

# Percorrer recursivamente todos os arquivos na pasta EN
for dirpath, dirnames, filenames in os.walk(en_dir):
    for filename in filenames:
        if filename.endswith(".json"):
            en_path = os.path.join(dirpath, filename)
            # Obter caminho relativo a partir da pasta EN
            rel_path = os.path.relpath(en_path, en_dir)
            cn_path = os.path.join(cn_dir, rel_path)
            jp_path = os.path.join(jp_dir, rel_path)
            kr_path = os.path.join(kr_dir, rel_path)
            es_path = os.path.join(es_dir, rel_path)
            loc_path = os.path.join(localization_dir, rel_path)

            # Criar diretório de saída se não existir
            os.makedirs(os.path.dirname(loc_path), exist_ok=True)

            # Inicializar listas de dados
            en_list = []
            cn_list = []
            jp_list = []
            kr_list = []
            es_list = []

            # Ler o arquivo EN
            if os.path.exists(en_path):
                with open(en_path, encoding="utf-8") as en_file:
                    en_data = json.load(en_file)
                    en_list = en_data.get("dataList", [])
            else:
                print(f"Arquivo {en_path} não encontrado.")
                continue  # Sem o arquivo EN, não faz sentido continuar

            # Ler o arquivo CN se existir
            if os.path.exists(cn_path):
                with open(cn_path, encoding="utf-8") as cn_file:
                    cn_data = json.load(cn_file)
                    cn_list = cn_data.get("dataList", [])

            # Ler o arquivo JP se existir
            if os.path.exists(jp_path):
                with open(jp_path, encoding="utf-8") as jp_file:
                    jp_data = json.load(jp_file)
                    jp_list = jp_data.get("dataList", [])

            # Ler o arquivo KR se existir
            if os.path.exists(kr_path):
                with open(kr_path, encoding="utf-8") as kr_file:
                    kr_data = json.load(kr_file)
                    kr_list = kr_data.get("dataList", [])

            # Ler o arquivo ES se existir
            if os.path.exists(es_path):
                with open(es_path, encoding="utf-8") as es_file:
                    es_data = json.load(es_file)
                    es_list = es_data.get("dataList", [])

            # Criar dicionários por ID para acesso rápido
            
            cn_dict = {i: item for i, item in enumerate(cn_list)}
            jp_dict = {i: item for i, item in enumerate(jp_list)}
            kr_dict = {i: item for i, item in enumerate(kr_list)}
            es_dict = {i: item for i, item in enumerate(es_list)}

            localization_list = []

            for i, en_item in enumerate(en_list):
                cn_item = cn_dict.get(i, {})
                jp_item = jp_dict.get(i, {})
                kr_item = kr_dict.get(i, {})
                es_item = es_dict.get(i, {})

                for key in en_item:
                    if key == "id":
                        continue
                    full_key = f"{i:04d}-{key}"
                    
                    original_value = en_item.get(key, "")

                    context = (
                        f"KR : \n{kr_item.get(key, '')}\n\n"
                        f"JP : \n{jp_item.get(key, '')}\n\n"
                        f"CN : \n{cn_item.get(key, '')}\n\n"
                        f"ES : \n{es_item.get(key, '')}"
                    )

                    localization_item = {
                        "key": full_key,
                        "original": original_value,
                        "context": context,
                    }

                    localization_list.append(localization_item)

            # Salvar o resultado em Localization
            with open(loc_path, "w", encoding="utf-8") as loc_file:
                json.dump(
                    localization_list,
                    loc_file,
                    ensure_ascii=False,
                    indent=4,
                )
            # Atualizar barra de progresso
            file_counter += 1
            print_progress(file_counter, total_files)
# Linha em branco para finalizar a barra de progresso
print()