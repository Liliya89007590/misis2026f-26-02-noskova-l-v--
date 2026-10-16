def f():
     text_1 = "пРиВет МИР"
     print (text_1.upper())
     print (text_1.lower())
     print (text_1.capitalize())
     x = str(input())
     if x == "upper":
         print (text_1.upper())
     elif x == "lower":
         print (text_1.lower())
     elif x == "capitalize":
         print (text_1.capitalize())
print (f())
