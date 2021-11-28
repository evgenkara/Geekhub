"""
Написати функцію < prime_list >, яка прийматиме 2 аргументи - початок і кінець діапазона, і вертатиме список простих чисел всередині цього діапазона.
"""

def is_prime(num):
    if num < 2:
        return False
    elif num == 2:
        return True
    for n in range(2, num):
        if num % n == 0:
            return False
    return True

def prime_list(start, end):
    primes = []
    for num in range(start, end + 1):
        if is_prime(num):
            primes.append(num)
    return primes

number_1 = int(input("Enter 1st number: "))
number_2 = int(input("Enter 2nd number: "))
print(prime_list(number_1, number_2))