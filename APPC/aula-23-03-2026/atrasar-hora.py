print("Programa para atrasar a hora")

try :
    hora = int(input("Digite a hora: "))
    minuto = int(input("Digite o minuto: "))
    segundo = int(input("Digite o segundo: "))

    if (hora < 0 or hora > 23) or (minuto < 0 or minuto > 59) or (segundo < 0 or segundo > 59):
        print("Hora, minuto ou segundo inválidos. Por favor, digite valores válidos.")
    
    else:
        quantidade_de_segundos = hora * 3600 + minuto * 60 + segundo

        print("Horario fornecido", hora, ":", minuto, ":", segundo)

        print("A quantidade de segundos ate o inicio do dia e: ", quantidade_de_segundos)

        print("Horario que faltam: ", quantidade_de_segundos /
        3600, ":", quantidade_de_segundos /
        60 % 60, ":", quantidade_de_segundos % 60)
    
except ValueError:

    print("Por favor digite apenas numeros inteiros.")

    print("quer atrasar a hora?")
    resposta = input("Digite 'sim' para atrasar a hora ou 'nao' para encerrar o programa: ").lower()

    if resposta == 'sim':
        try:
            horas_para_atrasar = int(input("Digite quantas horas deseja atrasar: "))
            minutos_para_atrasar = int(input("Digite quantos minutos deseja atrasar: "))
            segundos_para_atrasar = int(input("Digite quantos segundos deseja atrasar: "))

            total_segundos_para_atrasar = horas_para_atrasar * 3600 + minutos_para_atrasar * 60 + segundos_para_atrasar

            nova_quantidade_de_segundos = (quantidade_de_segundos - total_segundos_para_atrasar) % (24 * 3600)

            nova_hora = nova_quantidade_de_segundos // 3600
            nova_minuto = (nova_quantidade_de_segundos % 3600) // 60
            nova_segundo = nova_quantidade_de_segundos % 60

            print("Novo horário após atrasar: ", nova_hora, ":", nova_minuto, ":", nova_segundo)

        except ValueError:
            print("Por favor digite apenas numeros inteiros.")
    elif resposta == 'nao':
        print("Programa encerrado")

