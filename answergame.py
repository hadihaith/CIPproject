import random
import string
import re
import sqlite3
import sys
import cowsay

db1 = sqlite3.connect('data.db')
db = db1.cursor()
score = 0
asked = {
    1: False,
    2: False,
    3: False,
    4: False,
    5: False,
    6: False,
    7: False,
    8: False,
    9: False,
    10: False }

def main():
    sqlstarter()
    print("Welcome to the programming language questions game, implemented by Hadi Haidar, ", end="")
    while True:
        username = input("Enter your name to continue: ")
        username = username.strip()
        if any(letter.isdigit() for letter in username):
            print("Your name cannot contain numbers. ", end="")
        elif isspecial(username):
            print("Your name cannot contain special characters. ", end="")
        else:
            break
    password = input("Choose a password and you really should remember this!!: ")
    db.execute('INSERT INTO userdata (username, password) VALUES (?, ?)', (username, password))
    db1.commit()
    while True:
        try:
            while True:
                qsnum = int(input("How many Questions would you like to be asked in this game? "))
                if qsnum <= 10:
                    break
                else:
                    print("There are only 10 questions in this game!")
                    pass
            bonusqs = input("For best experience, please maximize your terminal! Would you be interested in a bonus question after the game is over? ")
            pattern = r"(.*)?\b(yes|yeah|yep|yup|sure|ok|okay|affirmative|positive|indeed|absolutely)\b(.*)?"
            matches = re.findall(pattern, bonusqs, re.IGNORECASE)
            if matches:
                print("Thank you!")
                boolbonus = True
            else:
                boolbonus = False
            break
        except (ValueError, EOFError):
            print("Not a valid input(Enter a positive integer)")
            pass
    gamestarter(qsnum)
    print("Remember that password you inputted at the beginning of the game? inputting it again will be the only way you see your score!")
    inpw = input(f"Well {username}, enter your password: ")
    db.execute('SELECT password FROM userdata WHERE username = ?', (username,))
    pw = db.fetchone()
    if inpw == pw[0]:
        print(f"Your score is {score}/{qsnum}, thank you so much for playing")
        moooo = input("Would you like to see a cow? ")
        pattern1 = r"(.*)?\b(yes|yeah|yep|yup|sure|ok|okay|affirmative|positive|indeed|absolutely)\b(.*)?"
        matches = re.findall(pattern1, moooo, re.IGNORECASE)
        if matches:
            if bonusasker(boolbonus) == True:
                cowsay.cow("You answered the bonus correctly!!")
            elif bonusasker(boolbonus) == False:
                cowsay.cow("You did not answer the bonus correctly :(")
            else:
                cowsay.cow("You did not even choose to answer\n the bonus question >:(")
        else:
            if bonusasker(boolbonus) == True:
                print("You answered the bonus correctly!!")
            elif bonusasker(boolbonus) == False:
                print("You did not answer the bonus correctly :(")
            print("Have a good day! ")


    else:
        sys.exit("Your password is wrong, game ending..")


def gamestarter(nq):
    global score
    answers = {
    1: 'A',
    2: 'A',
    3: 'B',
    4: 'B',
    5: 'A',
    6: 'B',
    7: 'A',
    8: 'B',
    9: 'C',
    10: 'A'
    }
    n = 0
    while n != nq:
        n += 1
        qn, qd, c = getrandomqs()
        print(qd)
        for i in c:
            print(i)
        while True:
            ans = input("Answer: ")
            if ans.upper() in ['A', 'B', 'C', 'D']:
                break
            else:
                print("Answer must be one letter chosen from A, B, C, D")
                pass
        if ans.upper() == answers[qn]:
            score += 1
            print("Correct Answer!")
        else:
            print("Wrong Answer!")
            continue



def getrandomqs():
    global asked
    questions = {
    1: "Which of the following is the correct way to convert a string to an integer in Python?",
    2: "What is the result of the expression `5 / 2` in Python?",
    3: "Which of the following is an example of a floating-point number in Python?",
    4: "What is the output of the following code snippet in Python?\nx = 7\ny = 2\nprint(x // y)",
    5: "Which of the following Python functions can be used to calculate the absolute value of a number?",
    6: "What is the result of the expression `2 ** 3` in Python?",
    7: "Which of the following is the correct way to round a floating-point number to the nearest integer in Python?",
    8: "What is the result of the expression `10 % 3` in Python?",
    9: "Which of the following is the correct way to convert an integer to a string in Python?",
    10: "What is the output of the following code snippet in Python?\nx = 5\ny = 2\nprint(x / y)",
    }
    choices = {
    1: ["A) int('10')", "B) str(10)", "C) integer('10')", "D) parse_int('10')"],
    2: ["A) 2.5", "B) 2", "C) 2.0", "D) Error"],
    3: ["A) 10", "B) 3.14", "C) '5.6'", "D) 7.8"],
    4: ["A) 3.5", "B) 3", "C) 3.0", "D) 3.5"],
    5: ["A) abs()", "B) fabs()", "C) absolute()", "D) absolute_value()"],
    6: ["A) 6", "B) 8", "C) 9", "D) 16"],
    7: ["A) round(3.14)", "B) round(3.14, 1)", "C) int(3.14)", "D) floor(3.14)"],
    8: ["A) 3", "B) 1", "C) 0", "D) 2"],
    9: ["A) string(10)", "B) int_to_string(10)", "C) str(10)", "D) convert_string(10)"],
    10: ["A) 2.5", "B) 2", "C) 2.0", "D) 2.5"]
    }
    while True:
        qn = random.randint(1,10)
        if asked[qn] == True:
            continue
        else:
            break
    asked[qn] = True
    qd = questions[qn]
    c = choices[qn]
    return qn, qd, c

def bonusasker(b):
    global score
    if b == False:
        return None
    else:
        print("First let's answer the bonus question! This is a question of brain calculation ability, input a number then input the result of it's factorial!")
        #showcasing that i know recursion :)
        while True:
            try:
                n = int(input("What is the number? "))
                break
            except ValueError:
                print("Enter a Positive Integer, ", end="")
                pass
        fact = factorial(n)
        while True:
            try:
                ans = int(input("Enter what you think is the factorial: "))
                break
            except ValueError:
                print("Enter a Positive Integer, ", end="")
                pass
        if ans == fact:
            print("Congratulations for being so amazing")
            return True
        else:
            print("That is not correct")
            return False

def factorial(num):
    if num <= 1:
        return 1
    return num * factorial(num - 1)

def isspecial(word):
    special = string.punctuation
    x = word
    for letter in x:
        if letter in special:
            return True
    return False

def sqlstarter():
    db.execute('CREATE TABLE IF NOT EXISTS userdata (user_id INTEGER PRIMARY KEY, username TEXT NOT NULL, password TEXT NOT NULL);')

if __name__ == "__main__":
    db.execute('DROP TABLE IF EXISTS userdata')
    db1.commit()
    main()
