import os

def auditar_codigo_local():
    vulnerabilidades_encontradas = []
    extensoes_analisadas = (".py", ".json", ".env", ".js")
    padroes_perigosos = ["password =", "api_key =", "secret =", "token ="]

    for raiz, _, ficheiros in os.walk("."):
        if ".git" in raiz or "__pycache__" in raiz:
            continue
        for ficheiro in ficheiros:
            if ficheiro.endswith(extensoes_analisadas) and ficheiro != "agente.json":
                caminho_completo = os.path.join(raiz, ficheiro)
                try:
                    with open(caminho_completo, "r", encoding="utf-8", errors="ignore") as f:
                        for num_linha, linha in enumerate(f, 1):
                            linha_lower = linha.lower()
                            for padrao in padroes_perigosos:
                                if padrao in linha_lower and "#" not in linha:
                                    vulnerabilidades_encontradas.append({
                                        "ficheiro": caminho_completo,
                                        "linha": num_linha,
                                        "alerta": f"Possível exposição de credencial detetada ({padrao.strip()})"
                                    })
                except Exception:
                    pass
                    
    return vulnerabilidades_encontradas
