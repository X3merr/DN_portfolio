import random

def roll_dice_advanced():
    sides = int(input("Enter the number of sides on the dice: "))
    rolls = int(input("Enter the number of times to roll: "))

    results = []
    print("\nRolling the dice...\n")
    
    for i in range(rolls):
        result = random.randint(1, sides)
        results.append(result)
        print(f"Roll {i+1}: 🎲 {result}")

    print("\n📊 Roll Statistics:")
    print(f"🎯 Highest Roll: {max(results)}")
    print(f"🐢 Lowest Roll: {min(results)}")
    print(f"📉 Average Roll: {sum(results) / len(results):.2f}")

roll_dice_advanced()