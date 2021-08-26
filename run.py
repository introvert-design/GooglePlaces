import json

from distance_matrix import distance
from place_details import places


def save(data):
    try:
        save_file = input("Do you want to save the result to a file (Yes/No)? ").lower()
        if save_file == "yes":
            filename = input("Enter filename: ")
            with open(filename + ".json", "w") as outfile:
                json.dump(data, outfile, indent=3)
            return True
        return False
    except IOError:
        return False


def main():
    run = True
    while run:
        print("Options: \n 1. Place Details \n 2. Distance Matrix \n 3. Nearby Places \n 4. Exit")
        try:
            choice = int(input("Enter your choice (1, 2, 3 or 4): "))
            if choice == 1:
                place_details = places()
                print(place_details)
                save_file = save(place_details)
                if save_file:
                    print("Place details saved")
                else:
                    print("Place Details not saved.")
            elif choice == 2:
                dist_matrix = distance()
                print(dist_matrix)
                save_file = save(dist_matrix)
                if save_file:
                    print("Distance matrix saved")
                else:
                    print("Distance matrix not saved.")
            elif choice == 3:
                pass
            elif choice == 4:
                run = False
            else:
                print("Not a valid option.")
        except ValueError:
            print("Invalid entry! Enter a valid option.")
        except KeyboardInterrupt:
            run = False


if __name__ == '__main__':
    main()
