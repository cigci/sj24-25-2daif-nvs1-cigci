for i in range(1, 2001):
    if i % 3 == 0 and i % 5 == 0:
        print("FizzBuzz")
    elif i % 3 == 0:
        print("Fizz")
    elif i % 5 == 0:
        print("Buzz")
    elif i % 7 == 0:
        print("Whizz")
    elif i % 11 == 0:
        print("Bang")
    else:
        print(i)
