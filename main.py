from helper import crt, measure_time, read_cn_values
from meet_in_the_midle_attack import meet_in_the_middle
from small_exp_attack import small_exponent_attack


def main():
    choose = int(input(f'Choose the attack:\n1. Small exponent attack\n2. meet in the middle attack\n'))
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
            C_values, N_values, _ = read_cn_values('data/mitm_rsa_10.txt')

            print(f'==================== MEET IN THE MIDDLE ====================')
            res_meet_in_the_middle, res_meet_in_the_middle_time = measure_time(meet_in_the_middle, int(C_values[0]),
                                                                               int(N_values[0]), 65537, 20)
            print(f'Plaintext = {hex(res_meet_in_the_middle)}')
            print(f'Time taken for attack: {res_meet_in_the_middle_time} seconds')
            if pow(res_meet_in_the_middle, 65537, N_values[0]) == C_values[0]:
                print("Attack is successful!")
            else:
                print("Ups.. Attack is failed")
        case _:
            print(f'Incorrect value input! Try again')


if __name__ == '__main__':
    main()
