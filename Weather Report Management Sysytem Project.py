import csv
import math
import os
import re
import matplotlib
matplotlib.use("Agg")  # Safe for environments without GUI display
import matplotlib.pyplot as plt


FILE_NAME = "cities_data.csv"

# ----------------------------------------------------------------------
# INPUT CONSTRAINTS
# ----------------------------------------------------------------------
MAX_ATTEMPTS = 5            # wrong attempts allowed per field before returning to menu
NAME_MIN_LEN = 2            # City / State minimum length
NAME_MAX_LEN = 50           # City / State maximum length
PINCODE_LENGTH = 6          # Indian pincode = exactly 6 digits, cannot start with 0
MAX_RAINFALL = 15000.0      # upper sanity limit (mm)

# Letters separated by single spaces only (no digits, no symbols)
NAME_PATTERN = re.compile(r"[A-Za-z]+(?: [A-Za-z]+)*")
# Digits with optional single decimal point (no sign, no exponent, no nan/inf)
NUMBER_PATTERN = re.compile(r"\d+(?:\.\d+)?")

SMALL_WORDS = {"and", "of"}

# List of sample Indian cities with states, pincodes and rainfall
CITY_DATA = [
    ("Hyderabad", "Telangana", 500001, 42),
    ("Secunderabad", "Telangana", 500003, 38),
    ("Warangal", "Telangana", 506001, 55),
    ("Nizamabad", "Telangana", 503001, 48),
    ("Khammam", "Telangana", 507001, 60),
    ("Karimnagar", "Telangana", 505001, 52),
    ("Ramagundam", "Telangana", 505208, 58),
    ("Vijayawada", "Andhra Pradesh", 520001, 66),
    ("Visakhapatnam", "Andhra Pradesh", 530001, 72),
    ("Guntur", "Andhra Pradesh", 522001, 61),
    ("Rajahmundry", "Andhra Pradesh", 533101, 68),
    ("Tirupati", "Andhra Pradesh", 517501, 46),
    ("Kurnool", "Andhra Pradesh", 518001, 40),
    ("Anantapur", "Andhra Pradesh", 515001, 35),
    ("Bengaluru", "Karnataka", 560001, 45),
    ("Mysuru", "Karnataka", 570001, 48),
    ("Mangaluru", "Karnataka", 575001, 76),
    ("Hubballi", "Karnataka", 580020, 52),
    ("Belagavi", "Karnataka", 590001, 63),
    ("Shivamogga", "Karnataka", 577201, 57),
    ("Chennai", "Tamil Nadu", 600001, 44),
    ("Coimbatore", "Tamil Nadu", 641001, 51),
    ("Madurai", "Tamil Nadu", 625001, 49),
    ("Tiruchirappalli", "Tamil Nadu", 620001, 38),
    ("Salem", "Tamil Nadu", 636001, 41),
    ("Vellore", "Tamil Nadu", 632001, 43),
    ("Kochi", "Kerala", 682001, 85),
    ("Thiruvananthapuram", "Kerala", 695001, 90),
    ("Kozhikode", "Kerala", 673001, 75),
    ("Thrissur", "Kerala", 680001, 82),
    ("Kannur", "Kerala", 670001, 79),
    ("Kollam", "Kerala", 691001, 88),
    ("Mumbai", "Maharashtra", 400001, 62),
    ("Pune", "Maharashtra", 411001, 51),
    ("Nagpur", "Maharashtra", 440001, 49),
    ("Nashik", "Maharashtra", 422001, 54),
    ("Aurangabad", "Maharashtra", 431001, 42),
    ("Kolhapur", "Maharashtra", 416001, 56),
    ("Jaipur", "Rajasthan", 302001, 31),
    ("Jodhpur", "Rajasthan", 342001, 19),
    ("Kota", "Rajasthan", 324001, 28),
    ("Udaipur", "Rajasthan", 313001, 26),
    ("Ajmer", "Rajasthan", 305001, 30),
    ("Bikaner", "Rajasthan", 334001, 22),
    ("Delhi", "Delhi", 110001, 36),
    ("Noida", "Uttar Pradesh", 201301, 34),
    ("Lucknow", "Uttar Pradesh", 226001, 33),
    ("Kanpur", "Uttar Pradesh", 208001, 30),
    ("Varanasi", "Uttar Pradesh", 221001, 29),
    ("Agra", "Uttar Pradesh", 282001, 31),
    ("Prayagraj", "Uttar Pradesh", 211001, 32),
    ("Patna", "Bihar", 800001, 38),
    ("Gaya", "Bihar", 823001, 41),
    ("Muzaffarpur", "Bihar", 842001, 40),
    ("Bhagalpur", "Bihar", 812001, 44),
    ("Darbhanga", "Bihar", 846004, 42),
    ("Ranchi", "Jharkhand", 834001, 52),
    ("Jamshedpur", "Jharkhand", 831001, 46),
    ("Dhanbad", "Jharkhand", 826001, 48),
    ("Bhubaneswar", "Odisha", 751001, 74),
    ("Cuttack", "Odisha", 753001, 67),
    ("Rourkela", "Odisha", 769001, 61),
    ("Puri", "Odisha", 752001, 80),
    ("Sambalpur", "Odisha", 768001, 64),
    ("Raipur", "Chhattisgarh", 492001, 58),
    ("Bilaspur", "Chhattisgarh", 495001, 50),
    ("Durg", "Chhattisgarh", 491001, 54),
    ("Bhopal", "Madhya Pradesh", 462001, 41),
    ("Indore", "Madhya Pradesh", 452001, 39),
    ("Jabalpur", "Madhya Pradesh", 482001, 44),
    ("Gwalior", "Madhya Pradesh", 474001, 36),
    ("Ujjain", "Madhya Pradesh", 456001, 33),
    ("Ahmedabad", "Gujarat", 380001, 27),
    ("Surat", "Gujarat", 395001, 34),
    ("Vadodara", "Gujarat", 390001, 31),
    ("Rajkot", "Gujarat", 360001, 28),
    ("Gandhinagar", "Gujarat", 382010, 29),
    ("Bhavnagar", "Gujarat", 364001, 30),
    ("Amritsar", "Punjab", 143001, 25),
    ("Ludhiana", "Punjab", 141001, 28),
    ("Chandigarh", "Chandigarh", 160001, 27),
    ("Jalandhar", "Punjab", 144001, 29),
    ("Patiala", "Punjab", 147001, 26),
    ("Dehradun", "Uttarakhand", 248001, 41),
    ("Haridwar", "Uttarakhand", 249401, 43),
    ("Nainital", "Uttarakhand", 263002, 52),
    ("Shimla", "Himachal Pradesh", 171001, 59),
    ("Manali", "Himachal Pradesh", 175131, 73),
    ("Srinagar", "Jammu and Kashmir", 190001, 68),
    ("Jammu", "Jammu and Kashmir", 180001, 35),
    ("Guwahati", "Assam", 781001, 78),
    ("Silchar", "Assam", 788001, 75),
    ("Dibrugarh", "Assam", 786001, 81),
    ("Agartala", "Tripura", 799001, 68),
    ("Imphal", "Manipur", 795001, 62),
    ("Aizawl", "Mizoram", 796001, 69),
    ("Shillong", "Meghalaya", 793001, 74),
    ("Itanagar", "Arunachal Pradesh", 791111, 66),
    ("Kohima", "Nagaland", 797001, 65),
    ("Gangtok", "Sikkim", 737101, 70),
    ("Port Blair", "Andaman and Nicobar", 744101, 79),
    ("Panaji", "Goa", 403001, 63),
    ("Kolkata", "West Bengal", 700001, 71),
    ("Durgapur", "West Bengal", 713001, 58),
    ("Asansol", "West Bengal", 713301, 55),
    ("Siliguri", "West Bengal", 734001, 61),
    ("Howrah", "West Bengal", 711101, 69),
    ("Bardhaman", "West Bengal", 713101, 57),
    ("Haldwani", "Uttarakhand", 263139, 42),
    ("Aligarh", "Uttar Pradesh", 202001, 32),
    ("Bareilly", "Uttar Pradesh", 243001, 35),
    ("Moradabad", "Uttar Pradesh", 244001, 33),
    ("Meerut", "Uttar Pradesh", 250001, 31),
    ("Ghaziabad", "Uttar Pradesh", 201001, 30),
    ("Faridabad", "Haryana", 121001, 34),
    ("Gurugram", "Haryana", 122001, 35),
    ("Hisar", "Haryana", 125001, 28),
    ("Rohtak", "Haryana", 124001, 31),
    ("Karnal", "Haryana", 132001, 30),
    ("Bhilai", "Chhattisgarh", 490001, 53),
    ("Bilaspur", "Chhattisgarh", 495001, 50),   # same pincode as above -> skipped automatically
    ("Raigarh", "Chhattisgarh", 496001, 52),
    ("Nashik", "Maharashtra", 422005, 54),
    ("Satara", "Maharashtra", 415001, 46),
    ("Solapur", "Maharashtra", 413001, 45),
    ("Kolhapur", "Maharashtra", 416002, 56)
]


# ======================================================================
# VALIDATION FUNCTIONS
# Every validator returns (value, None) when valid, or (None, "error message")
# ======================================================================
def format_name(text):
    """Capitalise each word: 'port   blair' -> 'Port Blair' ('and'/'of' stay lowercase)."""
    words = text.lower().split()
    result = []
    for i, word in enumerate(words):
        if i > 0 and word in SMALL_WORDS:
            result.append(word)
        else:
            result.append(word.capitalize())
    return " ".join(result)


def validate_name(text, label):
    """City / State: alphabets and single spaces only, 2-50 characters."""
    text = " ".join(text.split())   # trim + collapse repeated spaces/tabs
    if not text:
        return None, f"{label} cannot be empty."
    if not NAME_PATTERN.fullmatch(text):
        return None, f"{label} must contain only alphabets (A-Z) and spaces. No digits or symbols."
    if len(text) < NAME_MIN_LEN:
        return None, f"{label} must have at least {NAME_MIN_LEN} letters."
    if len(text) > NAME_MAX_LEN:
        return None, f"{label} cannot be longer than {NAME_MAX_LEN} characters."
    return format_name(text), None


def validate_city_name(text):
    return validate_name(text, "City name")


def validate_state_name(text):
    return validate_name(text, "State name")


def validate_pincode(text):
    """Pincode: exactly 6 ASCII digits, first digit not 0."""
    text = text.strip()
    if not text:
        return None, "Pincode cannot be empty."
    if not (text.isascii() and text.isdigit()):
        return None, "Pincode must contain digits only (no letters, spaces, signs or symbols)."
    if len(text) != PINCODE_LENGTH:
        return None, f"Pincode must be exactly {PINCODE_LENGTH} digits."
    if text[0] == "0":
        return None, "Pincode cannot start with 0."
    return int(text), None


def validate_rainfall(text):
    """Rainfall: non-negative plain number (e.g. 45 or 45.5) up to MAX_RAINFALL."""
    text = text.strip()
    if not text:
        return None, "Rainfall cannot be empty."
    if text.startswith("-"):
        return None, "Rainfall cannot be negative."
    if not NUMBER_PATTERN.fullmatch(text):
        return None, "Rainfall must be a plain number like 45 or 45.5 (no letters or symbols)."
    value = float(text)
    if math.isnan(value) or math.isinf(value):
        return None, "Rainfall must be a finite number."
    if value > MAX_RAINFALL:
        return None, f"Rainfall cannot be more than {MAX_RAINFALL:.0f} mm."
    return value, None


def make_choice_validator(low, high):
    """Menu choice: whole number between low and high."""
    def validator(text):
        text = text.strip()
        if text.isascii() and text.isdigit() and low <= int(text) <= high:
            return int(text), None
        return None, f"Invalid choice. Please enter a number from {low} to {high}."
    return validator


def read_valid(prompt, validator):
    """
    Keep asking until the validator accepts the input.
    After MAX_ATTEMPTS wrong tries returns None (caller goes back to the menu).
    """
    for attempt in range(1, MAX_ATTEMPTS + 1):
        value, error = validator(input(prompt))
        if error is None:
            return value
        print(f"  Error: {error}")
        left = MAX_ATTEMPTS - attempt
        if left > 0:
            print(f"  Please try again ({left} attempt(s) left).")
    print("  Too many invalid attempts. Returning to menu.")
    return None


# ======================================================================
# DATA FUNCTIONS
# ======================================================================
def generate_default_cities():
    """Generate the default city list (duplicate pincodes are skipped)."""
    cities = []
    seen_pincodes = set()
    for city, state, pincode, rainfall in CITY_DATA:
        if pincode in seen_pincodes:
            continue
        seen_pincodes.add(pincode)
        cities.append({"city": city, "state": state, "pincode": pincode, "rainfall": rainfall})
    return cities


def load_cities():
    """Load cities from CSV. If not exists, create default city data."""
    if not os.path.exists(FILE_NAME):
        default_data = generate_default_cities()
        save_cities(default_data)
        return default_data

    cities = []
    try:
        with open(FILE_NAME, "r", newline="", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            for row in reader:
                try:
                    cities.append({
                        "city": row["city"].strip(),
                        "state": row["state"].strip(),
                        "pincode": int(row["pincode"]),
                        "rainfall": float(row["rainfall"])
                    })
                except Exception:
                    continue
    except FileNotFoundError:
        cities = generate_default_cities()
        save_cities(cities)

    if not cities:
        cities = generate_default_cities()
        save_cities(cities)

    return cities


def save_cities(cities):
    """Save city data to CSV file."""
    with open(FILE_NAME, "w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=["city", "state", "pincode", "rainfall"])
        writer.writeheader()
        for city in cities:
            writer.writerow({
                "city": city["city"],
                "state": city["state"],
                "pincode": city["pincode"],
                "rainfall": city["rainfall"]
            })


def pincode_exists(cities, pincode, ignore=None):
    return any(c["pincode"] == pincode and c is not ignore for c in cities)


# ======================================================================
# MENU OPERATIONS
# ======================================================================
def add_city(cities):
    """Add a new city (every field is validated)."""
    print("\n===== Add City =====")
    print("Rules: City/State = alphabets & spaces only | Pincode = 6 digits | Rainfall = number >= 0")

    city = read_valid("Enter City Name: ", validate_city_name)
    if city is None:
        return

    state = read_valid("Enter State Name: ", validate_state_name)
    if state is None:
        return

    pincode = read_valid("Enter Pincode (6 digits): ", validate_pincode)
    if pincode is None:
        return

    # Check duplicate pincode
    if pincode_exists(cities, pincode):
        print(f"City with pincode {pincode} already exists.")
        return

    rainfall = read_valid("Enter Rainfall (mm): ", validate_rainfall)
    if rainfall is None:
        return

    cities.append({
        "city": city,
        "state": state,
        "pincode": pincode,
        "rainfall": rainfall
    })

    save_cities(cities)
    print(f"City '{city}' added successfully.")
    print(f"Total cities now: {len(cities)}")


def display_all_cities(cities):
    """Display all cities in a table format."""
    print("\n===== All Cities =====")
    if not cities:
        print("No city records found.")
        return

    print("-" * 100)
    print(f"{'City':<25} {'State':<20} {'Pincode':<10} {'Rainfall (mm)':<15}")
    print("-" * 100)
    for city in cities:
        print(f"{city['city']:<25} {city['state']:<20} {city['pincode']:<10} {city['rainfall']:<15.2f}")
    print("-" * 100)


def display_city_by_pincode(cities):
    """Display city by pincode."""
    print("\n===== Search City by Pincode =====")
    pincode_val = read_valid("Enter Pincode (6 digits): ", validate_pincode)
    if pincode_val is None:
        return

    found = False
    print("-" * 80)
    print(f"{'City':<25} {'State':<20} {'Pincode':<10} {'Rainfall (mm)':<15}")
    print("-" * 80)
    for city in cities:
        if city["pincode"] == pincode_val:
            print(f"{city['city']:<25} {city['state']:<20} {city['pincode']:<10} {city['rainfall']:<15.2f}")
            found = True
    print("-" * 80)

    if not found:
        print(f"No city found for pincode {pincode_val}.")


def update_rainfall(cities):
    """Update rainfall for a city by pincode."""
    print("\n===== Update City Rainfall =====")
    pincode_val = read_valid("Enter City Pincode (6 digits): ", validate_pincode)
    if pincode_val is None:
        return

    for city in cities:
        if city["pincode"] == pincode_val:
            rain_val = read_valid("Enter new rainfall (mm): ", validate_rainfall)
            if rain_val is None:
                return
            city["rainfall"] = rain_val
            save_cities(cities)
            print(f"Rainfall updated for {city['city']}.")
            print(f"New rainfall: {city['rainfall']:.2f} mm")
            return

    print(f"No city found for pincode {pincode_val}.")


def edit_city(cities):
    """Edit city details and rainfall."""
    print("\n===== Edit City Details =====")
    pincode_val = read_valid("Enter Pincode of city to edit (6 digits): ", validate_pincode)
    if pincode_val is None:
        return

    city = next((c for c in cities if c["pincode"] == pincode_val), None)
    if city is None:
        print(f"No city found with pincode {pincode_val}.")
        return

    print(f"\nCurrent City: {city['city']}")
    print(f"Current State: {city['state']}")
    print(f"Current Pincode: {city['pincode']}")
    print(f"Current Rainfall: {city['rainfall']:.2f} mm")

    print("\nChoose what to edit:")
    print("1. City Name")
    print("2. State")
    print("3. Pincode")
    print("4. Rainfall")
    print("5. Cancel")

    choice = read_valid("Enter your choice: ", make_choice_validator(1, 5))
    if choice is None:
        return

    if choice == 1:
        new_name = read_valid("Enter new city name: ", validate_city_name)
        if new_name is not None:
            city["city"] = new_name
            save_cities(cities)
            print("City name updated successfully.")

    elif choice == 2:
        new_state = read_valid("Enter new state: ", validate_state_name)
        if new_state is not None:
            city["state"] = new_state
            save_cities(cities)
            print("State updated successfully.")

    elif choice == 3:
        def validate_new_pincode(text):
            value, error = validate_pincode(text)
            if error:
                return None, error
            if pincode_exists(cities, value, ignore=city):
                return None, "This pincode is already in use by another city."
            return value, None

        new_pincode = read_valid("Enter new pincode (6 digits): ", validate_new_pincode)
        if new_pincode is not None:
            city["pincode"] = new_pincode
            save_cities(cities)
            print("Pincode updated successfully.")

    elif choice == 4:
        new_rainfall = read_valid("Enter new rainfall (mm): ", validate_rainfall)
        if new_rainfall is not None:
            city["rainfall"] = new_rainfall
            save_cities(cities)
            print(f"Rainfall updated to {city['rainfall']:.2f} mm.")

    else:
        print("Edit cancelled.")


def plot_rainfall_graph(cities):
    """Generate graph using matplotlib."""
    print("\n===== Rainfall Graph =====")

    if not cities:
        print("No city data available to plot.")
        return

    # Sort by rainfall descending for better graph
    sorted_cities = sorted(cities, key=lambda x: x["rainfall"], reverse=True)

    names = [c["city"] for c in sorted_cities[:15]]
    rainfall = [c["rainfall"] for c in sorted_cities[:15]]

    plt.figure(figsize=(12, 7))
    plt.bar(names, rainfall, color="skyblue", edgecolor="black")
    plt.title("Top 15 Cities by Rainfall (mm)")
    plt.xlabel("City")
    plt.ylabel("Rainfall (mm)")
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()

    output_file = "city_rainfall_chart.png"
    try:
        plt.savefig(output_file)
        print(f"Graph saved successfully as '{output_file}'")
    except Exception as e:
        print(f"Error while saving graph: {e}")

    # Fallback: if GUI available, show it, else skip
    try:
        plt.show()
    except Exception:
        pass

    plt.close()


def show_menu():
    print("\n========================================")
    print("       CITY RAINFALL MANAGEMENT")
    print("========================================")
    print("1. Add City")
    print("2. Display All Cities")
    print("3. Update City Rainfall")
    print("4. Search City by Pincode")
    print("5. Edit City Details")
    print("6. Show Rainfall Graph")
    print("7. Exit")
    print("========================================")


def main():
    cities = load_cities()
    print("Welcome to City Rainfall Management System.")
    print("Data is stored in file: cities_data.csv")
    print(f"Currently {len(cities)} cities are loaded.")

    menu_validator = make_choice_validator(1, 7)

    try:
        while True:
            show_menu()
            choice, error = menu_validator(input("Enter your choice: "))
            if error:
                print(error)
                continue

            if choice == 1:
                add_city(cities)
            elif choice == 2:
                display_all_cities(cities)
            elif choice == 3:
                update_rainfall(cities)
            elif choice == 4:
                display_city_by_pincode(cities)
            elif choice == 5:
                edit_city(cities)
            elif choice == 6:
                plot_rainfall_graph(cities)
            elif choice == 7:
                print("Thank you! Exiting City Rainfall Management System.")
                break
    except (EOFError, KeyboardInterrupt):
        print("\nInput closed. Exiting City Rainfall Management System.")


if __name__ == "__main__":
    main()
