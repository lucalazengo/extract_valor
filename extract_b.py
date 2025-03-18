import re
import spacy
import nltk
from nltk.tokenize import sent_tokenize

nltk.download('punkt')

# Carregar modelo spaCy
try:
    nlp = spacy.load("pt_core_news_sm")
except OSError:
    print("Modelo spaCy não encontrado. Baixe com 'python -m spacy download pt_core_news_sm'.")

def limpar_texto(texto):
    texto = texto.replace("\n", " ")
    texto = re.sub(r"\s+", " ", texto).strip()
    return texto

def extrair_contexto_proximo(sentenca, valor, janela=5):
    palavras = sentenca.split()
    valor_tokens = valor.replace('R$', '').strip().split()
    idx = None

    # Encontrar o índice do valor no texto
    for i, palavra in enumerate(palavras):
        if valor_tokens[0] in palavra:
            idx = i
            break

    if idx is None:
        return sentenca  # fallback se não achar o índice exato

    inicio = max(0, idx - janela)
    fim = min(len(palavras), idx + janela + 1)
    contexto = " ".join(palavras[inicio:fim])

    return contexto

def entidades_nomeadas(sentenca):
    doc = nlp(sentenca)
    return [(ent.text, ent.label_) for ent in doc.ents]

def limpar_texto(texto):
    texto = re.sub(r'\s+', ' ', texto.replace('\n', ' ').strip())
    return texto

def extrair_valores_e_contexto(texto, janela=8):
    texto_limpo = limpar_texto(texto)

    padrao_valor = r"[rR]\$ ?\d{1,3}(?:\.\d{3})*(?:,\d{2})?(?=\W|$)"
    valores = set(re.findall(padrao_valor, texto_limpo, re.IGNORECASE))

    sentencas = [sent.text for sent in nlp(texto_limpo).sents]

    resultados = []
    valores_adicionados = set()

    for valor in valores:
        encontrado = False
        for sentenca in sentencas:
            if valor.lower() in sentenca.lower():
                contexto = extrair_contexto_proximo(sentenca, valor, janela=7)
                entidades = entidades_nomeadas(sentenca)
                chave_unica = (valor, contexto)

                if chave_unica not in resultados:
                    resultados.append({
                        "Valor": valor,
                        "Contexto": contexto,
                        "Entidades": entidades
                    })
                break  # Encontrou contexto, sai do loop interno

    # Tratamento extra para valores possivelmente em tabelas não identificados pelo spaCy
    valores_encontrados = {item["Valor"] for item in resultados}
    valores_faltantes = valores - valores.intersection(val["Valor"] for val in resultados)

    if valores_adicionais := valores - set([item["Valor"] for item in resultados]):
        linhas = texto.splitlines()
        for valor in valores_adicionais:
            for linha in linhas:
                if valor.lower() in linha.lower():
                    contexto = linha.strip()
                    entidades = entidades_nomeadas(contexto)
                    chave_unica = (valor, contexto)

                    if chave_unica not in resultados:
                        resultados.append({
                            "Valor": valor,
                            "Contexto": contexto,
                            "Entidades": entidades
                        })
                    break

    return resultados
