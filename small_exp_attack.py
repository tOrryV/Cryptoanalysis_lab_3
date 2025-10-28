from helper import crt, integer_nth_root_binary


def small_exponent_attack(ciphertexts, modules, exp):
    Ct = crt(ciphertexts, modules)
    Pt = integer_nth_root_binary(Ct, exp)

    return Pt