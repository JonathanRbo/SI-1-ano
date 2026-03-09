print("Programa para classificar triangulo com base nos lados")

lado1_como_texto = input("Digite quanto mede em cm o 1° lado: ")
lado1 = float(lado1_como_texto)

lado2 = float(input("Digite quanto mede em cm o 2° lado: "))

print("Digite quanto mede em cm o 3° lado")
lado3 = float(input())

if lado1 == lado2 and lado1 == lado3:
    print("Seu triangulo e um equilatero")

elif lado1 == lado2 or lado1 == lado3 or lado2 == lado3:
    print("Seu triangulo e um isosceles")

else:
    print("Seu triangulo e um escaleno")

print("Programa encerrado")


'''
Estilos e formatos:
"teste1_com_stilo" = "Snake case"
"teste2ComStilo" = "Camel case"
'''
