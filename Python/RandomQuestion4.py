word = input("Enter a word!")
vowel = 0
for i in word:
    if i in "aeiou":
        vowel = vowel + 1
print(f"{word} has {vowel} vowels")