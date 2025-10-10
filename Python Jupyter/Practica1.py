import sys

print(sys.version)

# Funciones para str

x = 23+23
print(x)

y = "Buenas"
print(y)

x = 2
print(x)

# This is a coment

w = True

if w:
    print((y[0]))
    print((y[-1]))
    print(y[0:3])
    print(y[3:])
    print(y[:3])
    print(len(y))

texto = "wejejeje \n hola"

print(texto)

first = "Jaime"
last = "gomez"
full = f"{first}{last}"
print(full)
print(full.upper())
print(full.lower())
print(full.title())
print(full.find("a"))
print(full.replace("a", "5"))
print(full)

# Funciones para num

x = 10
y = 3.2
z = 4+7j

print(type(x), type(y), type(z))
print(isinstance(x, int))
print(isinstance(y, int))
print(isinstance(z, complex))

print(x+y)
print(x*y)
print(x**y)
print(x/y)
print(x//y)
print(x-y)
print(x % y)  # Módulo
print(abs(-x))  # Valor absoluto
print(round(y))  # Redondedar
print(pow(x, y))  # Potencia
print(divmod(x, y))  # Cociente y resta

if x > y:
    print("x > y")
elif x == y:
    print("x = y")
else:
    print("x < y")

age = 22

if age >= 18 and age < 50:
    print("eres adulto")
elif age < 10:
    print("eres un niño")
else:
    print("carcamal")

print("Primer bucle")
for number in range(4):
    print(number)

print("Segundo bucle")
for number in range(1, 6):
    print(number)

print("Tercer bucle")
for number in range(1, 10, 3):
    print(number)

contador = 0
for x in range(5):
    for y in range(5):
        print(f"({x},{y})", end='')
        contador += 1
    print("\n")

print(contador)

number = 100

while number > 0:
    print(number)
    number //= 2

comand = " "
while comand.lower() != "salir":
    comand = input("Escribe 'salir' para salir:")
print("Has salido")

comand = ""

while True:
    comand = input("Escribe 'caracol' para salir:")
    if comand.lower() == "caracol":
        break
print("Has salido")


def greet():
    print("Hola como estas me llamo abraham :)")
    x = 12 ** 2

    print(f"\n y tengo {x} años")


greet()


def greet_with_name(name):
    print(f"Hola {name}")


greet_with_name("abragham")


def greet_frist_and_last_name(first_name, last_name=None):
    if last_name:
        print(f"Hola, me llamo {first_name} {last_name}")
    else:
        print(f"Hola, me llamo {first_name}")

    print("¿Y tu como te llamas?")


greet_frist_and_last_name("Abraham", "Chicaiza")
greet_frist_and_last_name("Juan")


def add(n1, n2):
    return n1+n2


result = add(2, 43)
print(result)


def multiply(*nums):
    total = 1
    print("multiplying")
    for num in nums:
        total *= num
        print(num, " ")
    return total


result = multiply(23, 423, 234, 5, 34)

print("= ", result)

# Lista
numeros = [1, 2, 3]
numeros.append(4)
print(numeros)

# Tupla
coordenada = (10, 20)
# coordenada[0] = 3 no funciona
print(coordenada)
