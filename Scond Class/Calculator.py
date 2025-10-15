a = int(input("Enter The First Value : "))
b = int(input("Enter The Scond Value : "))

print(" Choose The Choice ")
print("1. ADD ")
print("2. SUB ")
print("3. DIVISION ")
print("4. MULTIPLICATION ")
print("5. POWER OF A ")
print("6. POWER OF B ")

c = int(input("Enter The Choice : "))

if c == 1:
 print(f"A+B : {a+b}")
elif c == 2:
 print(f"A-B : {a-b}") 
elif c == 3:
 print(f"A/B : {a/b}") 
elif c == 4:
 print(f"A*B : {a*b}") 
elif c == 5:
 print(f"A*A: {a*a}") 
elif c == 6:
 print(f"B*B: {b*b}") 


