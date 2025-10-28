def extended_gcd(num1, num2):
    if num1 == 0:
        return num2, 0, 1
    gcd, x1, y1 = extended_gcd(num2 % num1, num1)

    x = y1 - (num2 // num1) * x1
    y = x1

    return gcd, x, y


def crt(a_values, mod_values):
    N_mod = 1
    for mod in mod_values:
        N_mod *= mod

    x = 0
    for a, mod in zip(a_values, mod_values):
        M_i = N_mod // mod

        g, inv, _ = extended_gcd(M_i, mod)
        if g != 1:
            raise ValueError("Inverse doesn't exist! The module must be mutually simple in pairs")

        N_i = inv % mod

        x += a * M_i * N_i

    return x % N_mod

