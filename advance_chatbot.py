def chatbot():
    print("Hello! How can I help you?")
    print("1. I need assistance with my account.")
    print("2. I want more information about your product.")
    print("3. I want a phone call with a live assistant.")

    choice1 = input("Enter your choice (1, 2, or 3): ")

    if choice1 == "1":
        print("\nOf course, please choose what help you need:")
        print("1. I need a new password.")
        print("2. I need to change personal data.")
        print("3. I require live assistance.")

        choice2 = input("Enter your choice (1, 2, or 3): ")

        if choice2 == "1":
            print("\nWe will send you an email to reset your password.")
        elif choice2 == "2":
            print("\nYou can update your personal data in the account settings.")
        elif choice2 == "3":
            print("\nA live assistant will contact you shortly.")
        else:
            print("\nInvalid choice. Please restart the chatbot and try again.")

    elif choice1 == "2":
        print("\nWhat would you like to know about our products?")
        print("1. Tell me more about your mobile phones.")
        print("2. Tell me more about your televisions.")
        print("3. Tell me more about software installation.")

        choice2 = input("Enter your choice (1, 2, or 3): ")

        if choice2 == "1":
            print("\nOur mobile phones feature cutting-edge technology and sleek designs. Do you want more information via call from our assitant?.")
        elif choice2 == "2":
            print("\nOur televisions offer stunning visuals and advanced smart features. Do you want more information via call from our assitant?.")
        elif choice2 == "3":
            print("\nWe provide guides for software installation also we are providing paid servise when our assistan will install all programs what you need, Do you want more information via call from our assitant?.")
        else:
            print("\nInvalid choice. Please restart the chatbot and try again.")


    elif choice1 == "3":
        print("\nA live assistant will call you shortly. Please ensure your phone is available.")

    else:
        print("\nInvalid choice. Please restart the chatbot and select a valid option.")

# Run the chatbot
chatbot()