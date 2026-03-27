print("Programa para adiantar a hora")

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

    print("quer adiantar a hora?")
    resposta = input("Digite 'sim' para adiantar a hora ou 'nao' para encerrar o programa: ").lower()

    if resposta == 'sim':
        try:
            horas_para_adiantar = int(input("Digite quantas horas deseja adiantar: "))
            minutos_para_adiantar = int(input("Digite quantos minutos deseja adiantar: "))
            segundos_para_adiantar = int(input("Digite quantos segundos deseja adiantar: "))

            total_segundos_para_adiantar = horas_para_adiantar * 3600 + minutos_para_adiantar * 60 + segundos_para_adiantar

            nova_quantidade_de_segundos = (quantidade_de_segundos + total_segundos_para_adiantar) % (24 * 3600)

            nova_hora = nova_quantidade_de_segundos // 3600
            nova_minuto = (nova_quantidade_de_segundos % 3600) // 60
            nova_segundo = nova_quantidade_de_segundos % 60

            print("Novo horário após adiantar: ", nova_hora, ":", nova_minuto, ":", nova_segundo)

        except ValueError:
            print("Por favor digite apenas numeros inteiros.")
    elif resposta == 'nao':
        print("Programa encerrado")
