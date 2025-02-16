# BSD

from abc import ABC, abstractmethod

class Shape(ABC):
  @abstractmethod
  def area():
    pass

class Rectangle(Shape):
  def __init__(self, width, height):
    self.width = width
    self.height = height

  def area(self):
    return self.width * self.height
  
class Circle(Shape):
  def __init__(self, width, height):
    self.width = width
    self.height = height

  def area(self):
    return self.width * 3.141592653897936462
  

class PaymentProcessor(ABC):
  @abstractmethod
  def process_payment(amount):
    pass

class creditCardProcessor(PaymentProcessor):
  def process_payment(amount):
    print(f'payed with credit card {amount}')


class payPalCardProcessor(PaymentProcessor):
  def process_payment(amount):
    print(f'payed with payPal {amount}')


  
class Animal (ABC):
  @abstractmethod
  def speak():
    pass

  @abstractmethod
  def move():
    pass

class Dog(Animal):
  def speak():
    print("Bark!")
  def move():
    print("run")
class Bird(Animal):
  def speak():
    print("chirp!")
  def move():
    print("fly")



class Logger(ABC):
  @abstractmethod
  def write(self, data):
    pass

class FileWrite(Logger):
  def write(self, data):
    with open("log.txt", "a") as f:
      f.write(data + "\n")
 
class consoleWrite(Logger):
  def write(self, data):
    print(data)

    
