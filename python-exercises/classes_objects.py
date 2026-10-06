"""Examples of classes, objects, inheritance, and encapsulation."""


class Person:
    def __init__(self, name, age):
        self.name = name
        self._age = age

    @property
    def age(self):
        return self._age

    def describe(self):
        return f"{self.name} is {self.age} years old."


class Student(Person):
    def __init__(self, name, age, course):
        super().__init__(name, age)
        self.course = course

    def describe(self):
        return f"{super().describe()} Course: {self.course}."


student = Student("Asha", 20, "Python")
print(student.describe())