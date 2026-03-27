print("Programa para calcular a quantidade de segundos ate o final do dia")

try :
    hora = int(input("Digite a hora: "))
    minuto = int(input("Digite o minuto: "))
    segundo = int(input("Digite o segundo: "))

    if (hora < 0 or hora > 23) or (minuto < 0 or minuto > 59) or (segundo < 0 or segundo > 59):
        print("Hora, minuto ou segundo inválidos. Por favor, digite valores válidos.")
    
    else:
        quantidade_de_segundos = hora * 3600 + minuto * 60 + segundo

        print("Horario fornecido", hora, ":", minuto, ":", segundo)

        print("A quantidade de segundos ate o final do dia e: ", 24 * 3600 - quantidade_de_segundos)

        print("Horario que faltam: ", (24 * 3600 - quantidade_de_segundos) /
        3600, ":", (24 * 3600 - quantidade_de_segundos) /
        60 % 60, ":", (24 * 3600 - quantidade_de_segundos) % 60)

except ValueError:
    print("Por favor digite apenas numeros inteiros.")


print("Programa encerrado")

