
def parse_trip(text):
    if not isinstance(text, str) or ':' not in text:
        raise ValueError("Invalid trip format")

    parts = text.split(':')
    if len(parts) != 2 or not parts[0].strip() or not parts[1].strip():
        raise ValueError("Invalid trip format")

    try:
        km = float(parts[1])
        if km <= 0:
            raise ValueError("Distance must be positive")
    except ValueError:
        raise ValueError("Invalid distance")

    return parts[0].strip().title(), km


def fare_average(fares_csv):
    if not isinstance(fares_csv, str) or not fares_csv.strip():
        raise ValueError("Invalid fare list")

    try:
        values = [int(r.strip()) for r in fares_csv.split(',')]
        if not values or any(v < 0 for v in values):
            raise ValueError("Invalid fares")
    except ValueError:
        raise ValueError("Invalid fare list")

    return sum(values) // len(values)


def payable_fare(text):
    if not isinstance(text, str) or '|' not in text:
        raise ValueError("Invalid fare format")

    parts = text.split('|')
    if len(parts) != 2:
        raise ValueError("Invalid fare format")

    try:
        fare = float(parts[0])
        promo = float(parts[1])

        if fare < 0 or promo < 0:
            raise ValueError("Fare and promo cannot be negative")
    except ValueError:
        raise ValueError("Invalid fare or promo")

    total = fare * 1.18 - promo
    return max(total, 0)


def main():
    print("==== Running parse_trip ====")
    user_input = input("Enter cab:distance in km (e.g. sedan:12): ")
    try:
        result = parse_trip(user_input)
        print("Cab and Distance:", result)
    except ValueError as e:
        print("Error:", e)

    print("\n==== Running fare_average ====")
    user_input = input("Enter fares as CSV (e.g. 120,95,210): ")
    try:
        result = fare_average(user_input)
        print("Average Fare:", result)
    except ValueError as e:
        print("Error:", e)

    print("\n==== Running payable_fare ====")
    user_input = input("Enter fare|promo (e.g. 250|30): ")
    try:
        result = payable_fare(user_input)
        print("Payable Fare:", result)
    except ValueError as e:
        print("Error:", e)


if __name__ == "__main__":
    main()
