def check_field(**kwargs):
    faltando = [campo for campo, valor in kwargs.items() if not valor]

    if faltando:
        return False, f"Faltam os campos: {', '.join(faltando)}"

    return True, None