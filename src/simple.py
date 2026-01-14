from my_module import msg

n = int(input())

if n < 0:
    print("Error")
else:
    total = 0
    for idx in range(1, n + 1):
        total += idx
    print(total)
    msg()
