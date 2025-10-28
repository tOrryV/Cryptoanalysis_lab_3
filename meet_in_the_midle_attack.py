from helper import extended_gcd_iter


def meet_in_the_middle(ciphertext, module, exp, l):
    """
    Performs a Meet-in-the-Middle (MITM) attack on RSA encryption with small plaintext space.

    - Splits the plaintext M into two halves: M = T * S.
    - Precomputes and stores (T^e mod n) values for all possible T in a dictionary.
    - For each possible S, computes the modular inverse of S^e and checks if it matches any stored value.
    - If a match is found, reconstructs and returns the candidate plaintext.
    - This attack exploits small plaintext spaces where exhaustive search is feasible.

    :param ciphertext: The RSA ciphertext to be attacked (integer).
    :param module: The RSA modulus n (integer).
    :param exp: The RSA public exponent e (integer).
    :param l: A bit length of the plaintext.
    :return: The recovered plaintext as an integer, or None if the plaintext could not be found.
    """

    high_boundary = 1 << (l // 2)
    X = {}
    for T in range(1, high_boundary):
        T_e = pow(T, exp, module)
        if T_e not in X:
            X[T_e] = T

    for S in range(1, high_boundary):
        S_e = pow(S, exp, module)

        g, inv, _ = extended_gcd_iter(S_e, module)
        C_s = (ciphertext * inv) % module
        T = X.get(C_s)
        if T is not None:
            plaintext_candidate = T * S
            if plaintext_candidate < (1 << l):
                return plaintext_candidate
    return None
