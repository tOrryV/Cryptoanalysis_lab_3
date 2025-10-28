from helper import extended_gcd_iter


def meet_in_the_middle(ciphertext, module, exp, l):
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
