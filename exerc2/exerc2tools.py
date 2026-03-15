def somar(num1, num2):
    return num1 + num2

def subtrair(num1, num2):
    return num1 - num2

def multiplicar(num1, num2):
    return num1 * num2

def dividir(num1, num2):
    try:
        return num1 / num2
    except ZeroDivisionError:
        return "Erro: divisão por zero"


