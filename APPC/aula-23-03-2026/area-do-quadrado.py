print("Programa para calcular a area em centimetros quadrados de um quadrado")

try:
    lado_como_texto = input("Digite quanto mede em cm o lado do quadrado: ")
    lado = float(lado_como_texto)

    if lado < 0:
        print("Valor do lado invalido. Por favor, digite um valor positivo.")
    else:
        area = lado * lado
        print("A area do quadrado e: ", area, "cm²")

except ValueError:
    print("Por favor digite apenas numeros.")

print("Programa encerrado")