from flask import Flask, request, jsonify
import requests
import math
import json

# Initialize the Flask application
app = Flask(__name__)

# Function to check if a number is an Armstrong number
def check_armstrong(num):
    try:
        num = float(num)
    except ValueError:
        return False
    if not num.is_integer():
        return False  # Armstrong is defined for integers only
    num_str = str(abs(int(num)))  # Use absolute value for digit operations
    length = len(num_str)
    total = sum(int(digit) ** length for digit in num_str)
    return total == abs(int(num))

# Function to identify properties of a given number
def identify_number_properties(num):
    attributes = []
    if check_armstrong(num):
        attributes.append("armstrong")
    if int(abs(num)) % 2 != 0:
        attributes.append("odd")
    else:
        attributes.append("even")
    digit_total = sum(int(digit) for digit in str(abs(int(num)))) if float(num).is_integer() else 0
    return attributes, digit_total

# Function to determine if a number is perfect
def check_perfect_number(num):
    try:
        num = float(num)
        if not num.is_integer() or num < 1:
            return False  # Perfect numbers are positive integers only
        num = int(num)
    except ValueError:
        return False
    divisor_sum = sum(i for i in range(1, num) if num % i == 0)
    return divisor_sum == num

# Function to verify if a number is prime
def verify_prime(num):
    try:
        num = float(num)
        if not num.is_integer() or num < 2:
            return False  # Primes are positive integers greater than 1
        num = int(num)
    except ValueError:
        return False
    if num == 2 or num == 3:
        return True
    if num % 2 == 0 or num % 3 == 0:
        return False
    for i in range(5, int(math.isqrt(num)) + 1, 6):
        if num % i == 0 or num % (i + 2) == 0:
            return False
    return True

# Function to retrieve a fun fact about a number from the Numbers API
def fetch_fun_fact(num):
    try:
        num = float(num)
        if not num.is_integer():
            return "Fun facts are available for integers only."
        response = requests.get(f"http://numbersapi.com/{int(abs(num))}/math?json")
        response.raise_for_status()
        data = response.json()
        return data.get('text')
    except (ValueError, requests.exceptions.RequestException) as error:
        return f"Could not retrieve fun fact: {error}"

# API endpoint to classify a number
@app.route('/api/classify-number', methods=['GET'])
def classify_given_number():
    num = request.args.get('number')

    # Validation for missing number
    if num is None:
        return jsonify({"error": True, "message": "Missing 'number' parameter"}), 400

    try:
        num = float(num)  # Allow negative and floating-point numbers
        properties, digit_sum = identify_number_properties(num)
        fun_fact = fetch_fun_fact(num)
        prime_status = verify_prime(num)
        perfect_status = check_perfect_number(num)

        # Response data construction
        response_data = {
            "number": num,
            "is_prime": prime_status,
            "is_perfect": perfect_status,
            "properties": properties,
            "digit_sum": digit_sum,
            "fun_fact": fun_fact
        }
        return jsonify(response_data), 200
    except ValueError:
        return jsonify({"error": True, "message": "Invalid input. Please provide a valid number."}), 400
    except Exception as error:
        return jsonify({"error": True, "message": f"Error processing number: {error}"}), 500


   # Running the Flask application
   if __name__ == '__main__':
       app.run(debug=False, host='0.0.0.0', port=5001)
