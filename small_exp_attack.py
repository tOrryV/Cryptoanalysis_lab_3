from helper import crt, integer_nth_root_binary


def small_exponent_attack(ciphertexts, modules, exp):
    """
    Recovers a plaintext encrypted under the same small public exponent using the broadcast attack (Håstad's CRT attack).

    - Uses the Chinese Remainder Theorem (CRT) to combine multiple ciphertexts {C_i} computed under different moduli {N_i}
      into a single value Ct ≡ C (mod ∏ N_i).
    - Computes the integer e-th root of Ct. If the same plaintext was encrypted with exponent e and the product of moduli
      is larger than the plaintext^e, the exact e-th root is the original plaintext.
    - Note: This function performs the algebraic steps but does not itself verify that the returned root is an exact match;
      the caller should validate that pow(Pt, exp, product_of_moduli) == Ct (or that pow(Pt, exp, N_i) == C_i for each i).

    Assumptions / requirements:
    - All moduli in `modules` must be pairwise coprime (CRT requires this). The `crt` helper will raise ValueError if not.
    - All ciphertexts must correspond to the same plaintext encrypted with the same exponent `exp`.
    - There must be enough ciphertexts (and sufficiently large product of moduli) so that plaintext^exp < product(moduli);
      otherwise the root will not equal the original plaintext.

    :param ciphertexts: Iterable or list of integers representing ciphertexts C_i (typically as integers).
    :param modules: Iterable or list of integers representing the corresponding RSA moduli N_i.
    :param exp: Integer public exponent e (e.g., 3, 5, 65537).
    :return: Integer Pt — the computed integer e-th root of the CRT-combined ciphertext. This is the candidate plaintext;
             the caller should verify correctness (e.g., with pow(Pt, exp, N_i) == C_i or pow(Pt, exp, product_of_moduli) == Ct).
    :raises ValueError: If the moduli are not pairwise coprime (raised by the crt function).
    """

    Ct = crt(ciphertexts, modules)
    Pt = integer_nth_root_binary(Ct, exp)

    return Pt
