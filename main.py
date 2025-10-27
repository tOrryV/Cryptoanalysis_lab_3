def read_cn_values(file_path):
    C_values = []
    N_values = []

    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if line.startswith('C'):
                value = line.split('=')[1].strip()
                C_values.append(value)
            elif line.startswith('N'):
                value = line.split('=')[1].strip()
                N_values.append(value)

    return C_values, N_values, len(C_values)


def main():
    C_values, N_values, exp = read_cn_values('data/se_rsa_10_test.txt')


if __name__ == '__main__':
    main()
