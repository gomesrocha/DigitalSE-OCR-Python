import re


def clean_and_tokenize(text):
    # Remover espaços e símbolos indesejados usando expressão regular
    cleaned_text = re.sub(r'[^\w\s]', '', text)
    # Dividir o texto em tokens usando espaços como delimitador
    tokens = cleaned_text.split()
    return tokens
