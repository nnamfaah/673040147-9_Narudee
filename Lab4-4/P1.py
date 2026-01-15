from room import Room, Bedroom, Kitchen

if __name__ == "__main__":
    print("- Bedroom -")
    bedroom = Bedroom(20, 25, "king size")
    print(bedroom.get_purpose())
    print(f"Bedroom recommended lighting setting : {bedroom.get_recommended_lighting()}")
    print(f"Bedroom area : {bedroom.calculate_area()}\n")

    print("- Kitchen (with Island) -")
    kitchen = Kitchen(30, 35, True)
    print(kitchen.get_purpose())
    print(f"Kitchen area : {kitchen.calculate_counter_space()}\n")
    
    print("- Kitchen (no Island) -")
    kitchen = Kitchen(30, 35, False)
    print(kitchen.get_purpose())
    print(f"Kitchen area : {kitchen.calculate_counter_space()}")
