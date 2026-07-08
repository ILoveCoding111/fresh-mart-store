hi = input("Enter a sentence!")
count = 1
for i in hi:
    if i == " ":
        count = count + 1
print(count)