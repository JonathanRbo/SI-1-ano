print("programa para calcular areas\n")

chave_de_digitacao = True
while chave_de_digitacao:
    try:
        lado = float(input("digite em cm do lado do quadrado: "))
    except ValueError:
        print("Por favor, digite um número válido. tente novamente!")
    else:
        if lado <= 0:
            print("O lado do quadrado deve ser um número positivo. tente novamente!")
        else:
            chave_de_digitacao = False
            area = lado ** 2
            print(f"A área do quadrado é: {area} cm²")

resposta = input("Deseja calcular outra area ou repetir? (s/n): ").lower()

while resposta != "s" and resposta != "n":
    print("resposta inválida. tente novamente!")
    resposta = input("Deseja calcular outra area ou repetir? (s/n): ").lower()

if resposta == "s":
    print("reiniciando o programa...")
    exec(open(__file__).read())

if resposta == "n":
    print("programa encerrado")