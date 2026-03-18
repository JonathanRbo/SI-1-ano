print("Equação do 2º grau: ax² + bx + c = 0")

try:
    a = float(input("Digite a: "))
    b = float(input("Digite b: "))
    c = float(input("Digite c: "))

    if a == 0:
        print("Isso não é uma equação do 2º grau (a não pode ser 0).")
    else:
        delta = b**2 - 4*a*c

        if delta < 0:
            print("A equação não possui raízes reais.")
        elif delta == 0:
            x = -b / (2*a)
            print("A equação possui uma única raiz:", x)
        else:
            x1 = (-b + delta**0.5) / (2*a)
            x2 = (-b - delta**0.5) / (2*a)
            print("A equação possui duas raízes:")
            print("x1 =", x1)
            print("x2 =", x2)

except ValueError:
    print("Por favor digite apenas números.")


print("Programa encerrado")