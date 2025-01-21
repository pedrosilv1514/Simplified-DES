class SDES:
    def __init__(self, key):
        self.key = key
        self.K1, self.K2 = self.generate_subkeys()

    def permute(self, input_bits, permutation):
        return [input_bits[p - 1] for p in permutation]

    def left_shift(self, bits, shifts):
        return bits[shifts:] + bits[:shifts]

    def generate_subkeys(self):
        P10 = [3, 5, 2, 7, 4, 10, 1, 9, 8, 6]
        P8 = [6, 3, 7, 4, 8, 5, 10, 9]

        key = self.permute(self.key, P10)
        left, right = key[:5], key[5:]

        left = self.left_shift(left, 1)
        right = self.left_shift(right, 1)
        K1 = self.permute(left + right, P8)

        left = self.left_shift(left, 2)
        right = self.left_shift(right, 2)
        K2 = self.permute(left + right, P8)

        return K1, K2

    def f(self, right, subkey):
        EP = [4, 1, 2, 3, 2, 3, 4, 1]
        S0 = [[1, 0, 3, 2], [3, 2, 1, 0], [0, 2, 1, 3], [3, 1, 3, 2]]
        S1 = [[0, 1, 2, 3], [2, 0, 1, 3], [3, 0, 1, 0], [2, 1, 0, 3]]
        P4 = [2, 4, 3, 1]

        expanded = self.permute(right, EP)
        xor_with_key = [bit ^ sk for bit, sk in zip(expanded, subkey)]

        left, right = xor_with_key[:4], xor_with_key[4:]
        row = int(f"{left[0]}{left[3]}", 2)
        col = int(f"{left[1]}{left[2]}", 2)
        left_sbox = S0[row][col]

        row = int(f"{right[0]}{right[3]}", 2)
        col = int(f"{right[1]}{right[2]}", 2)
        right_sbox = S1[row][col]

        sbox_output = [int(x) for x in f"{left_sbox:02b}{right_sbox:02b}"]
        return self.permute(sbox_output, P4)

    def encrypt_block(self, block):
        IP = [2, 6, 3, 1, 4, 8, 5, 7]
        IP_INV = [4, 1, 3, 5, 7, 2, 8, 6]

        permuted = self.permute(block, IP)
        left, right = permuted[:4], permuted[4:]

        # Rodada 1
        f_output = self.f(right, self.K1)
        left = [l ^ f for l, f in zip(left, f_output)]

        # Troca
        left, right = right, left

        # Rodada 2
        f_output = self.f(right, self.K2)
        left = [l ^ f for l, f in zip(left, f_output)]

        combined = left + right
        return self.permute(combined, IP_INV)

    def decrypt_block(self, block):
        """Descriptografa um bloco de 8 bits."""
        IP = [2, 6, 3, 1, 4, 8, 5, 7]
        IP_INV = [4, 1, 3, 5, 7, 2, 8, 6]

        # Permutação inicial
        permuted = self.permute(block, IP)
        left, right = permuted[:4], permuted[4:]

        # Rodada 1 (com K2)
        f_output = self.f(right, self.K2)
        left = [l ^ f for l, f in zip(left, f_output)]

        # Troca
        left, right = right, left

        # Rodada 2 (com K1)
        f_output = self.f(right, self.K1)
        left = [l ^ f for l, f in zip(left, f_output)]

        # Combinação e permutação final
        combined = left + right
        return self.permute(combined, IP_INV)


if __name__ == "__main__":
    key = [1, 0, 1, 0, 0, 0, 0, 0, 1, 0]  # Chave de 10 bits
    plaintext = [0, 1, 1, 1, 0, 0, 1, 0]  # Bloco de dados de 8 bits

    sdes = SDES(key)

    # Criptografia
    ciphertext = sdes.encrypt_block(plaintext)
    print("Ciphertext:", ciphertext)

    # Descriptografia
    decrypted = sdes.decrypt_block(ciphertext)
    print("Decrypted:", decrypted)

    # Validação
    assert decrypted == plaintext, "Erro: o bloco decifrado não corresponde ao original."
