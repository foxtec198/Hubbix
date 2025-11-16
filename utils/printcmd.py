# IGNORE
def print_cmd(texto): # Essa funções serve apenas para fazer um print formatado bonitinho no CMF
    txtl = len(texto) + 2
    total = 30
    total += txtl
    meio = int((total - txtl )/2)
    print('*' * total)
    print('*' * meio + f" {texto} " + '*' * meio)
    print('*' * total)