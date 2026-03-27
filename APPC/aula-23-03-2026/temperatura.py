print("Conversor de Temperatura")

print("1 - Celsius para Fahrenheit")
print("2 - Fahrenheit para Celsius")
print("3 - Celsius para Kelvin")
print("4 - Kelvin para Celsius")
print("5 - Celsius para Rankine")
print("6 - Celsius para Réaumur")
print("7 - Fahrenheit para Celsius")
print("8 - Fahrenheit para Kelvin")
print("9 - Fahrenheit para Rankine")
print("10 - Fahrenheit para Réaumur")
print("11 - Kelvin para Celsius")
print("12 - Kelvin para Fahrenheit")
print("13 - Kelvin para Rankine")
print("14 - Kelvin para Réaumur")
print("15 - Rankine para Celsius")
print("16 - Rankine para Fahrenheit")
print("17 - Rankine para Kelvin")
print("18 - Rankine para Réaumur")
print("19 - Réaumur para Celsius")
print("20 - Réaumur para Fahrenheit")
print("21 - Réaumur para Kelvin")
print("22 - Réaumur para Rankine")
print("23 - Réaumur para Réaumur")
print("0 - Sair")

opcao = int(input("Escolha uma opção: "))

if opcao == 0:
    print("Programa encerrado")
elif opcao == 1:
    celsius = float(input("Digite a temperatura em Celsius: "))
    fahrenheit = (celsius * 9/5) + 32
    print(f"{celsius}°C é igual a {fahrenheit}°F")
elif opcao == 2:
    fahrenheit = float(input("Digite a temperatura em Fahrenheit: "))
    celsius = (fahrenheit - 32) * 5/9
    print(f"{fahrenheit}°F é igual a {celsius}°C")
elif opcao == 3:
    celsius = float(input("Digite a temperatura em Celsius: "))
    kelvin = celsius + 273.15
    print(f"{celsius}°C é igual a {kelvin}K")
elif opcao == 4:
    kelvin = float(input("Digite a temperatura em Kelvin: "))
    celsius = kelvin - 273.15
    print(f"{kelvin}K é igual a {celsius}°C")
elif opcao == 5:
    celsius = float(input("Digite a temperatura em Celsius: "))
    rankine = (celsius + 273.15) * 9/5
    print(f"{celsius}°C é igual a {rankine}°R")
elif opcao == 6:
    celsius = float(input("Digite a temperatura em Celsius: "))
    reaumur = celsius * 4/5
    print(f"{celsius}°C é igual a {reaumur}°Ré")
elif opcao == 7:
    fahrenheit = float(input("Digite a temperatura em Fahrenheit: "))
    celsius = (fahrenheit - 32) * 5/9
    print(f"{fahrenheit}°F é igual a {celsius}°C")
elif opcao == 8:
    fahrenheit = float(input("Digite a temperatura em Fahrenheit: "))
    kelvin = (fahrenheit - 32) * 5/9 + 273.15
    print(f"{fahrenheit}°F é igual a {kelvin}K")
elif opcao == 9:
    fahrenheit = float(input("Digite a temperatura em Fahrenheit: "))
    rankine = fahrenheit + 459.67
    print(f"{fahrenheit}°F é igual a {rankine}°R")
elif opcao == 10:
    fahrenheit = float(input("Digite a temperatura em Fahrenheit: "))
    reaumur = (fahrenheit - 32) * 4/9
    print(f"{fahrenheit}°F é igual a {reaumur}°Ré")
elif opcao == 11:
    kelvin = float(input("Digite a temperatura em Kelvin: "))
    celsius = kelvin - 273.15
    print(f"{kelvin}K é igual a {celsius}°C")
elif opcao == 12:
    kelvin = float(input("Digite a temperatura em Kelvin: "))
    fahrenheit = (kelvin - 273.15) * 9/5 + 32
    print(f"{kelvin}K é igual a {fahrenheit}°F")
elif opcao == 13:
    kelvin = float(input("Digite a temperatura em Kelvin: "))
    rankine = kelvin * 9/5
    print(f"{kelvin}K é igual a {rankine}°R")
elif opcao == 14:
    kelvin = float(input("Digite a temperatura em Kelvin: "))
    reaumur = (kelvin - 273.15) * 4/5
    print(f"{kelvin}K é igual a {reaumur}°Ré")
elif opcao == 15:
    rankine = float(input("Digite a temperatura em Rankine: "))
    celsius = (rankine - 491.67) * 5/9
    print(f"{rankine}°R é igual a {celsius}°C")
elif opcao == 16:
    rankine = float(input("Digite a temperatura em Rankine: "))
    fahrenheit = rankine - 459.67
    print(f"{rankine}°R é igual a {fahrenheit}°F")
elif opcao == 17:
    rankine = float(input("Digite a temperatura em Rankine: "))
    kelvin = rankine * 5/9
    print(f"{rankine}°R é igual a {kelvin}K")
elif opcao == 18:
    rankine = float(input("Digite a temperatura em Rankine: "))
    reaumur = (rankine - 491.67) * 4/9
    print(f"{rankine}°R é igual a {reaumur}°Ré")
elif opcao == 19:
    reaumur = float(input("Digite a temperatura em Réaumur: "))
    celsius = reaumur * 5/4
    print(f"{reaumur}°Ré é igual a {celsius}°C")
elif opcao == 20:
    reaumur = float(input("Digite a temperatura em Réaumur: "))
    fahrenheit = (reaumur * 9/4) + 32
    print(f"{reaumur}°Ré é igual a {fahrenheit}°F")
elif opcao == 21:
    reaumur = float(input("Digite a temperatura em Réaumur: "))
    kelvin = (reaumur * 5/4) + 273.15
    print(f"{reaumur}°Ré é igual a {kelvin}K")
elif opcao == 22:
    reaumur = float(input("Digite a temperatura em Réaumur: "))
    rankine = (reaumur * 9/4) + 491.67
    print(f"{reaumur}°Ré é igual a {rankine}°R")
elif opcao == 23:
    reaumur = float(input("Digite a temperatura em Réaumur: "))
    print(f"{reaumur}°Ré é igual a {reaumur}°Ré")
else:    
    print("Opção inválida")

print("Programa encerrado")