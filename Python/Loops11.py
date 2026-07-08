word = input("Enter a word!")
i = 0
count= 0
while i < len(word):
    if word[i] in "aeiou":
        count = count + 1
    i = i + 1
print(count)