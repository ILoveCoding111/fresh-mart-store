marks = int(input("Enter your score!"))
if marks >= 90:
    if marks >= 95:
        print("Outstanding!")
    else:
        print("Excellent!");
elif marks >= 80 and marks <= 89:
    if marks >= 85 and marks <= 89:
        print("Very Good!")
    else:
        print("Good")
else:
    print("Needs improvement")        