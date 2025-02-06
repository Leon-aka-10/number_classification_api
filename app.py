from flask import Flask, request, jsonify
import requests
import math
import json

# Initialize the Flask application
app = Flask(__name__)

# Function to check if a number is an Armstrong number
def check_armstrong(number):
    num_str = str(number)
    length = len(num_str)
    total = sum(int(digit) ** length for digit in num_str)
    return total == number

# Function to identify properties of a given number
def identify_number_properties(number):
    attributes = []
    if check_armstrong(number):
        attributes.append("armstrong")
    attributes.append("odd" if number % 2 != 0 else "even")
    digit_total = sum(int(digit) for digit in str(number))
    return attributes, digit_total

# Function to determine if a number is perfect
def check_perfect_number(number):
    if number <= 1:
        return False
    divisor_sum = 0
    for i in range(1, int(math.isqrt(number)) + 1):
        if number % i == 0:
            divisor_sum += i
            if i * i != number:
                divisor_sum += number // i
    return divisor_sum - number == number

# Function to verify if a number is prime
def verify_prime(number):
    if number <= 1:
        return False
    if number <= 3:
        return True
    if number % 2 == 0 or number % 3 == 0:
        return False
    i = 5
    while i * i <= number:
        if number % i == 0 or number % (i + 2) == 0:
            return False
        i += 6
    return True

# Function to retrieve a fun fact about a number from the Numbers API
def fetch_fun_fact(number):
    try:
        response = requests.get(f"http://numbersapi.com/{number}/math?json")
        response.raise_for_status()
        data = response.json()
        return data.get('text')
    except requests.exceptions.RequestException as error:
        return f"Could not retrieve fun fact: {error}"

# API endpoint to classify a number
@app.route('/api/classify-number', methods=['GET'])
def classify_given_number():
    number = request.args.get('number')

    # Validation for missing or invalid number
    if number is None:
        return jsonify({"error": True, "message": "Missing 'number' parameter"}), 400
    if not number.isdigit():
        return jsonify({"number": number, "error": True, "message": "Invalid input"}), 400

    try:
        number = int(number)
        properties, digit_sum = identify_number_properties(number)
        fun_fact = fetch_fun_fact(number)
        prime_status = verify_prime(number)
        perfect_status = check_perfect_number(number)

        # Response data construction
        response_data = {
            "number": number,
            "is_prime": prime_status,
            "is_perfect": perfect_status,
            "properties": properties,
            "digit_sum": digit_sum,
            "fun_fact": fun_fact
        }
        return jsonify(response_data), 200
    except Exception as error:
        return jsonify({"error": True, "message": f"Error processing number: {error}"}), 500

# Running the Flask application
if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=5001)