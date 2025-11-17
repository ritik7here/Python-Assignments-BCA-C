# Name: YOUR NAME
# Roll No: YOUR ROLL
# Course: BCA
# Semester: 1st
# Subject: Problem Solving with Python
# Assignment: Unit-1 Mini Project
# Title: Student Profile Console App
# Date: DD/MM/YYYY

print("--------------------------------------------------")
print("     Welcome to the Student Profile CLI Tool")
print("--------------------------------------------------\n")

# ---------------------- Task 2: Inputs ----------------------

full_name = input("Enter your full name: ")
roll_no = input("Enter your roll number: ")
program = input("Enter your program (e.g., BCA): ")
university = input("Enter your university name: ")
city = input("Enter your city: ")
age = int(input("Enter your age: "))
hobby = input("Enter your hobby: ")

# ---------------------- Task 3: Operators Demo ----------------------

print("\n--- Operator Demonstration ---")
num1 = int(input("Enter first number: "))
num2 = int(input("Enter second number: "))

# Arithmetic
print("\nArithmetic Operators:")
print(f"{num1} + {num2} = {num1 + num2}")
print(f"{num1} - {num2} = {num1 - num2}")
print(f"{num1} * {num2} = {num1 * num2}")
print(f"{num1} / {num2} = {num1 / num2}")
print(f"{num1} % {num2} = {num1 % num2}")
print(f"{num1} ** {num2} = {num1 ** num2}")
print(f"{num1} // {num2} = {num1 // num2}")

# Assignment
print("\nAssignment Operators:")
x = num1
x += num2
print("x += num2:", x)
x -= num2
print("x -= num2:", x)

# Comparison
print("\nComparison Operators:")
print(num1, ">", num2, "=", num1 > num2)
print(num1, "<", num2, "=", num1 < num2)
print(num1, "==", num2, "=", num1 == num2)

# Logical
print("\nLogical Operators:")
print(num1 > 5 and num2 > 5)
print(num1 > 5 or num2 > 5)
print(not(num1 > num2))

# Identity
print("\nIdentity Operators:")
print(num1 is num2)
print(num1 is not num2)

# Membership
print("\nMembership Operators:")
text = "python programming"
print("'p' in text =", 'p' in text)
print("'z' not in text =", 'z' not in text)

# ---------------------- Task 4: String Operations ----------------------

print("\n--- String Operations ---")
print("Upper:", full_name.upper())
print("Lower:", full_name.lower())
print("Title:", full_name.title())
print("Replace:", full_name.replace("a", "@"))
print("Count of 'a':", full_name.count("a"))

# ---------------------- Task 5: Final Profile Card ----------------------

print("\n----------------------------------------")
print("         STUDENT PROFILE SYSTEM")
print("----------------------------------------")

print(f"Name:\t\t {full_name}")
print(f"Roll No:\t {roll_no}")
print(f"Course:\t\t {program}")
print(f"University:\t {university}")
print(f"City:\t\t {city}")
print(f"Age:\t\t {age}")
print(f"Hobby:\t\t {hobby}")

print("----------------------------------------")
print("Welcome to Python Programming!")
print("----------------------------------------")

# ---------------------- Task 6: Bonus Task ----------------------

save = input("\nDo you want to save your profile? (yes/no): ")

if save.lower() == "yes":
    with open("student_profile.txt", "w") as file:
        file.write("STUDENT PROFILE\n")
        file.write(f"Name: {full_name}\n")
        file.write(f"Roll No: {roll_no}\n")
        file.write(f"Course: {program}\n")
        file.write(f"University: {university}\n")
        file.write(f"City: {city}\n")
        file.write(f"Age: {age}\n")
        file.write(f"Hobby: {hobby}\n")

    print("Profile saved successfully as student_profile.txt!")
