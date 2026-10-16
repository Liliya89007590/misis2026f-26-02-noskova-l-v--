print ("введите числа")
a = int(input())
b = int(input())
print("что сделать?")
c = input()
if c == "+":
    print(a+b)
elif c == "-":
    print(a-b)
elif c == "*":
    print(a*b)
elif c == "/":
    print(a/b)
else:
        print("такой команды нет")
