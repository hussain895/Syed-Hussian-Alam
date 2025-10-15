a = float(input("Enter a First Number : "))
b = float(input("Enter a Second Number : "))

print("------------------------------ Choose The Option ------------------------------ ")
print("1. ADD")
print("2. SUB")
print("3. DIVIDE")
print("4. MULTIPLY")
print("5. POWER OF A")
print("6. POWER OF B")
print("7. CUBE OF A")
print("8. CUBE OF B")

c = int(input(" Enter A Option : "))

if c==1:
    print(f" Addition = {a+b}")
elif c == 2:
    print(f" Subtraction = {a-b}")
elif c == 3:
    print(f" Division = {a/b}")
elif c == 4:
    print(f" Multiplication = {a*b}")
elif c == 5:
    print(f" Power Of A is = {a*a}")
elif c == 6:
    print(f" Power Of B is = {b*b}")
elif c == 7:
    print(f" Cube Of A is = {a*a*a}")
elif c == 8:
    print(f" Cube Of B is = {b*b*b}")
