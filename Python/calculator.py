number1 = int(input("Enter a number"))
number2 = int(input("Enter a number"))
op = input("Enter an operator")
if op == '+':
    print(number1 + number2)
elif op == '-':
    print(number1 - number2)
elif op == '*':
    print(number1 * number2)
elif op == '/':
    print(number1 / number2)
else:
    print("Give an actual operator")

