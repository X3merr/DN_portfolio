def chatbot():
    print("Hello! Welcome to the Umbrella Corporation. How can I assist you today?")
    print("1. I need assistance with side effects of body enhancement treatment.")
    print("2. I want to book an appointment at the clinic to enhance my health.")

    choice1 = input("Enter your choice (1 or 2): ")

    if choice1 == "1":
        print("\nSure, I can help with your issue! What kind of side effect are you experiencing?")
        print("1. My body is mutating in unexpected ways.")
        print("2. I have a weird feeling, but no visible changes.")

        choice2 = input("Enter your choice (1 or 2): ")

        if choice2 == "1":
            print("\nEmergenci unit will arrive in 30 minits, please stand by on your location.")
        elif choice2 == "2":
            print("\nPlease monitor your symptoms closely and schedule a follow-up consultation. Use your stabilization medicine.")
        else:
            print("\nInvalid choice. Please restart the chatbot and try again.")

    elif choice1 == "2":
        print("\nWe offer health enhancement treatments. What kind of enhancement are you looking for?")
        print("1. Longer lifespan and durability.")
        print("2. Enhancement for combat.")

        choice2 = input("Enter your choice (1 or 2): ")

        if choice2 == "1":
            print("\nGreat choice! Our longevity and durability treatment is finest on the market. Use this link to book your consultation: [link].")
        elif choice2 == "2":
            print("\nOur combat unit enhancements are top-tier, designed for peak performance. Visit this link to schedule a session: [link].")
        else:
            print("\nInvalid choice. Please restart the chatbot and try again.")

    else:
        print("\nInvalid choice. Please restart the chatbot and try again.")

# Run the chatbot
chatbot()
