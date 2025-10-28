from helper import crt
from small_exp_attack import small_exponent_attack


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

def main():
    C_values, N_values, exp = read_cn_values('data/se_rsa_10.txt')
    res_small_exp_attack = small_exponent_attack(C_values, N_values, exp)

    C = crt(C_values, N_values)
    if pow(res_small_exp_attack, exp) == C:
        print("Success! Exact root: M^e == C")
    else:
        print("Ups.. Not exact: floor root was returned or insufficient data")


if __name__ == '__main__':
    main()
