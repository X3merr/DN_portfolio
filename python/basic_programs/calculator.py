def add(x, y):
    return x + y

def subtract(x, y):  
    return x - y  

def multiply(x, y):
    return x * y

def divide(x, y):
    if y == 0:
        return "Error! Division by zero."
    return x / y

def calculator():  
    print("Select option:")
    print("1. Function add")
    print("2. Function subtract")  
    print("3. Function multiply")  
    print("4. Function divide")
    
    choice = input("Enter choice (1/2/3/4): ")  
    
    try:
        num1 = float(input("Enter first number: "))  
        num2 = float(input("Enter second number: "))
    except ValueError:
        print("Invalid input. Please enter numeric values.")
        return
    
    if choice == '1':
        print(f"Result: {add(num1, num2)}")
    elif choice == '2':
        print(f"Result: {subtract(num1, num2)}")
    elif choice == '3':
        print(f"Result: {multiply(num1, num2)}")
    elif choice == '4':
        print(f"Result: {divide(num1, num2)}")
    else:
        print("Invalid input")

if __name__ == "__main__":
    calculator()
