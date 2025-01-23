def chatbot():
    print("Hello how can i help you?")
    print("1. I need assistance with my account.")
    print("2. I want more information about your product.")
    print("3. I want phone call with live assistant. ")

    choice1 = input("Enter your choice (1, 2, or 3): ")

    if choice1 == 1:
        print("/nAfcourse, please choise what help you need")
        print("1. I need new pasword ")
        print("2.I need to change personal data")
        Print("3. i require live assistance ")

        choice2= input("Enter your choice (1, 2, or 3): ")
    
        if choice2 == "1":
            print("\nWe will send you an email to reset your password.")
        elif choice2 == "2":
            print("\nYou can update your personal data in the account settings.")
        elif choice2 == "3":
            print("\nA live assistant will contact you shortly.")
        else:
            print("\nInvalid choice. Please restart the chatbot and try again.")

    elif choice2 = input("Enter your choice (1, 2, or 3): ")   
    print("1. Tell me more about your mobile phones.")
    print("2. Tell me more about your television.")
    print("3. tell me more about sowtvare instalation. ")


chatbot()
