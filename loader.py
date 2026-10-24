import json
import os

def carregar_configuracao_agente():
    caminho_ficheiro = "agente.json"
    if os.path.exists(caminho_ficheiro):
        with open(caminho_ficheiro, "r", encoding="utf-8") as f:
            return json.load(f)
    return None

def obter_system_prompt():
    config = carregar_configuracao_agente()
    if config and "system_prompt" in config:
        sp = config["system_prompt"]
        return f"""
        Papel: {sp.get('role')}
        Objetivo: {sp.get('objective')}
        Áreas de Especialização: {', '.join(sp.get('areas_of_expertise', []))}
        Diretrizes Comportamentais: {', '.join(sp.get('behavioral_guidelines', []))}
        """
    return "És um assistente de cibersegurança."
