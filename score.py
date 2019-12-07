def main():
    score = int(input())
    if score < 50:
        print("Grade 0")
    elif score > 50 and score <= 59:
        print("Grade 1")
    elif score > 59 and score <= 69:
        print("Grade 2")
    elif score > 69 and score <= 79:
        print("Grade 3")       
    else:
        print("Grade 4")

if __name__ == "__main__":
    main()