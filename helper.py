import time
from tqdm import tqdm


def read_cn_values(file_path):
    """
    Reads ciphertext (C) and modulus (N) values from a text file and returns them as integer lists.

    - Each line in the file should contain either 'C = <hex_value>' or 'N = <hex_value>'.
    - The function automatically strips whitespace and ignores lines without '='.
    - Hexadecimal values are converted to integers.
    - Returns the lists of C and N values, along with the count of ciphertexts found.

    :param file_path: Path to the text file containing RSA ciphertexts and moduli.
    :return: Tuple (C_values, N_values, count), where:
             - C_values: list of integers representing ciphertexts.
             - N_values: list of integers representing RSA moduli.
             - count: integer, number of ciphertexts found in the file.
    """

    C_values = []
    N_values = []

    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if '=' not in line:
                continue

            left, right = line.split('=', 1)
            value = int(right.strip(), 16)

            if left.strip().startswith('C'):
                C_values.append(value)
            elif left.strip().startswith('N'):
                N_values.append(value)

    return C_values, N_values, len(C_values)


def extended_gcd_iter(num1, num2):
    """
    Computes the greatest common divisor (GCD) of two integers using the iterative Extended Euclidean Algorithm.

    - Returns not only the GCD but also the coefficients (x, y) satisfying Bézout's identity:
      num1 * x + num2 * y = gcd(num1, num2).
    - This iterative version avoids recursion, making it efficient for large integers.

    :param num1: First integer (a).
    :param num2: Second integer (b).
    :return: Tuple (gcd, x, y), where:
             - gcd: the greatest common divisor of num1 and num2.
             - x, y: integers satisfying Bézout’s identity.
    """

    x0, x1, y0, y1 = 1, 0, 0, 1
    while num2 != 0:
        q, num1, num2 = num1 // num2, num2, num1 % num2
        x0, x1 = x1, x0 - q*x1
        y0, y1 = y1, y0 - q*y1
    return num1, x0, y0


def crt(a_values, mod_values):
    """
    Solves a system of congruences using the Chinese Remainder Theorem (CRT).

    - Finds an integer x that satisfies:
        x ≡ a_i (mod m_i)  for all i
    - Assumes that all moduli are pairwise coprime (mutually prime).
    - Raises an error if the modular inverses do not exist (i.e., moduli are not coprime).

    :param a_values: List of remainders (a_i) in the congruences.
    :param mod_values: List of moduli (m_i) corresponding to each remainder.
    :return: The smallest non-negative integer x that satisfies all congruences (x mod N_mod),
             where N_mod is the product of all moduli.
    :raises ValueError: If any two moduli are not coprime and modular inverse cannot be computed.
    """

    N_mod = 1
    for mod in mod_values:
        N_mod *= mod

    x = 0
    for a, mod in zip(a_values, mod_values):
        M_i = N_mod // mod

        g, inv, _ = extended_gcd_iter(M_i, mod)
        if g != 1:
            raise ValueError("Inverse doesn't exist! The module must be mutually simple in pairs")

        N_i = inv % mod

        x += a * M_i * N_i

    return x % N_mod


def integer_nth_root_binary(num, deg):
    """
    Computes the integer n-th root of a given number using the binary search method.

    - Finds the largest integer r such that r ** deg <= num.
    - Uses bit-length estimation to set the initial upper bound efficiently.
    - Works well for large integers and arbitrary degrees.

    :param num: The integer whose n-th root is to be computed.
    :param deg: The degree of the root (n).
    :return: The largest integer r such that r ** deg <= num.
    """

    low_bound, high_bound = 1, 1 << ((num.bit_length() + deg - 1) // deg + 1)
    while low_bound < high_bound:
        mid = (low_bound + high_bound) // 2
        p = pow(mid, deg)
        if p == num:
            return mid
        if p < num:
            low_bound = mid + 1
        else:
            high_bound = mid
    return low_bound - 1


def measure_time(func, *args, index=None):
    """
    Measures the execution time of a given function.

    - Calls the specified function with provided arguments.
    - Returns both the function result and the elapsed time in seconds.
    - Optionally extracts a specific element from the result if `index` is provided.

    :param func: The function to be executed and measured.
    :param *args: Positional arguments to pass to the target function.
    :param index: Optional index to extract a specific element from the result.
    :return: Tuple (result, execution_time), where:
             - result: Output of the executed function (or element at `index` if specified).
             - execution_time: Time in seconds taken to execute the function.
    """

    start_time = time.time()
    result = func(*args)
    end_time = time.time()
    execution_time = end_time - start_time
    if index is not None:
        result = result[index]
    return result, execution_time


def brute_force(ciphertext, modulus, exp, l):
    """
    Performs a brute-force search to recover the plaintext from an RSA ciphertext.

    - Iterates through all possible plaintext values in the range [1, 2^l).
    - For each candidate M, computes M^exp mod modulus and compares it to the ciphertext.
    - Returns the first matching plaintext value if found.
    - Displays a progress bar using tqdm for visual feedback.

    :param ciphertext: The RSA ciphertext to be decrypted (integer).
    :param modulus: The RSA modulus n (integer).
    :param exp: The RSA public exponent e (integer).
    :param l: A bit length of the plaintext search space.
    :return: The recovered plaintext as an integer, or None if not found.
    """

    target = int(ciphertext) % int(modulus)
    upper = 1 << l

    for M in tqdm(range(1, upper), desc="Brute-forcing", unit="it"):
        if pow(M, exp, modulus) == target:
            return M
    return None

