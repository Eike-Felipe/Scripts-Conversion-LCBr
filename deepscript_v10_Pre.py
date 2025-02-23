import json
import os
import re
from collections import OrderedDict
import sys  # para imprimir na mesma linha

# Diretórios
localization_dir = "Localize"  # Diretório de entrada
output_dir = "pt-BR"          # Diretório de saída para os arquivos convertidos

def fix_newline_tags(text):
    """Corrige tags de quebra de linha."""
    if not isinstance(text, str):
        return text
    text = text.replace('\\\\n', '\\n')
    text = re.sub(r'\s*\\n', '\\n', text)
    return text.strip()

# Contar o total de arquivos JSON
total_files = 0
for root, dirs, files in os.walk(localization_dir):
    for f in files:
        if f.endswith(".json"):
            total_files += 1

processed_files = 0  # Contador de arquivos processados

# Percorrer todos os arquivos na pasta Localize
for dirpath, dirnames, filenames in os.walk(localization_dir):
    for filename in filenames:
        if filename.endswith(".json"):
            loc_path = os.path.join(dirpath, filename)
            rel_path = os.path.relpath(loc_path, localization_dir)
            output_path = os.path.join(output_dir, rel_path)
            
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            
            grouped_items = OrderedDict()  # Agrupa por ID, mantendo a ordem
            current_group = None  # Rastreia o grupo -1 atual
            
            with open(loc_path, encoding="utf-8") as loc_file:
                localization_list = json.load(loc_file)
                
                for item in localization_list:
                    original_key = item["key"]
                    key_parts = original_key.split("-", 1)
                    if len(key_parts) != 2:
                        continue
                    item_id, field_key = key_parts
                        
                    
                    # Tentar converter o ID para inteiro se for um número
                    try:
                        item_id = int(item_id)
                    except ValueError:
                        pass  # Mantém como string se não for um número
                    
                    if item_id not in grouped_items:
                        grouped_items[item_id] = {"id": item_id}
                    target_group = grouped_items[item_id]
                        
                    
                    # Processar texto traduzido
                    translated_text = item.get("translation") or item.get("original", "")
                    translated_text = fix_newline_tags(translated_text)
                    target_group[field_key] = translated_text
            
            # Converter para lista e ordenar
            output_list = []
            for key in grouped_items:
                if isinstance(key, int) or (isinstance(key, str)):
                    output_list.append(grouped_items[key])
            
            # Salvar o arquivo
            with open(output_path, "w", encoding="utf-8") as output_file:
                json.dump({"dataList": output_list}, output_file, ensure_ascii=False, indent=4)
            
            # Atualizar contador e exibir barra de progresso
            processed_files += 1
            progress = processed_files / total_files
            bar_length = 40
            filled_length = int(bar_length * progress)
            bar = '█' * filled_length + '-' * (bar_length - filled_length)
            sys.stdout.write(f'\rProgresso: |{bar}| {processed_files}/{total_files}')
            sys.stdout.flush()

# Garantir pular para nova linha ao final
print()