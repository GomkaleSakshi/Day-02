"""Examples of conditions and loops."""

score = 76
if score >= 90:
    grade = "A"
elif score >= 70:
    grade = "B"
else:
    grade = "C"
print("Grade:", grade)

print("Numbers from 1 to 5:")
for number in range(1, 6):
    print(number)

remaining = 3
while remaining > 0:
    print("Countdown:", remaining)
    remaining -= 1