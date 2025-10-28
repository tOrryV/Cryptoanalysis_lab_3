import time


def read_cn_values(file_path):
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
    x0, x1, y0, y1 = 1, 0, 0, 1
    while num2 != 0:
        q, num1, num2 = num1 // num2, num2, num1 % num2
        x0, x1 = x1, x0 - q*x1
        y0, y1 = y1, y0 - q*y1
    return num1, x0, y0


def crt(a_values, mod_values):
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
    start_time = time.time()
    result = func(*args)
    end_time = time.time()
    execution_time = end_time - start_time
    if index is not None:
        result = result[index]
    return result, execution_time