from helper import crt, measure_time, read_cn_values, brute_force
from meet_in_the_midle_attack import meet_in_the_middle
from small_exp_attack import small_exponent_attack


def main():
    """
    Interactive entry point to choose and run one of the implemented RSA attacks.

    - Presents a simple menu to the user and reads a numeric choice from standard input.
    - Option 1: Runs the Small Exponent attack:
        * Reads ciphertexts and moduli from 'data/se_rsa_10.txt' via read_cn_values.
        * Runs small_exponent_attack and measures execution time using measure_time.
        * Validates the found plaintext against the combined CRT ciphertext and prints results.
    - Option 2: Runs the Meet-in-the-Middle attack (and compares with brute force):
        * Reads a single ciphertext and modulus from 'data/mitm_rsa_10.txt'.
        * Runs meet_in_the_middle and measures execution time using measure_time.
        * Validates the found plaintext and prints results.
        * Additionally runs the brute_force search and prints/validates its result and timing.
    - Any other input prints an error message and exits.

    Notes / side effects:
    - This function performs console I/O (prompts, prints) and reads files from the 'data' directory.
    - It relies on helper functions defined elsewhere in the module (read_cn_values, small_exponent_attack,
      meet_in_the_middle, brute_force, measure_time, crt).
    - The function prints human-readable results (hex-formatted plaintext and timings) to stdout.

    :return: None
    :raises ValueError: If the user's input cannot be parsed as an integer.
    :raises OSError / IOError: If required data files are missing or unreadable.
    """

    choose = int(input(f'Choose the attack:\n1. Small exponent attack\n2. Meet in the middle attack\n'))
    match choose:
        case 1:
            C_values, N_values, exp = read_cn_values('data/se_rsa_10.txt')

            print(f'==================== SMALL EXPONENT ATTACK ====================')
            res_small_exp_attack, res_small_exp_attack_time = measure_time(small_exponent_attack, C_values, N_values, exp)
            print(f'Plaintext = {hex(res_small_exp_attack)}')
            print(f'Time taken for attack: {res_small_exp_attack_time} seconds')
            C = crt(C_values, N_values)
            if pow(res_small_exp_attack, exp) == C:
                print("Attack is successful!")
            else:
                print("Ups.. Attack is failed")
        case 2:
            C_value, N_value, _ = read_cn_values('data/mitm_rsa_10.txt')

            print(f'==================== MEET IN THE MIDDLE ====================')
            res_meet_in_the_middle, res_meet_in_the_middle_time = measure_time(meet_in_the_middle, int(C_value[0]),
                                                                               int(N_value[0]), 65537, 20)
            print(f'Plaintext = {hex(res_meet_in_the_middle)}')
            print(f'Time taken for attack: {res_meet_in_the_middle_time} seconds')
            if pow(res_meet_in_the_middle, 65537, N_value[0]) == C_value[0]:
                print("Attack is successful!")
            else:
                print("Ups.. Attack is failed")

            print(f'==================== BRUTE FORCE ====================')
            bf, bf_time = measure_time(brute_force, int(C_value[0]), int(N_value[0]), 65537, 20)
            print(f'Plaintext = {hex(bf)}')
            print(f'Time taken for attack by brute force: {bf_time} seconds')
            if pow(bf, 65537, N_value[0]) == C_value[0]:
                print("Attack is successful!")
            else:
                print("Ups.. Attack is failed")
        case _:
            print(f'Incorrect value input! Try again')


if __name__ == '__main__':
    main()
