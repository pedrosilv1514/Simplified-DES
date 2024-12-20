import tkinter as tk
from tkinter import ttk, messagebox

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

        # Round 1
        f_output = self.f(right, self.K1)
        left = [l ^ f for l, f in zip(left, f_output)]

        # Swap
        left, right = right, left

        # Round 2
        f_output = self.f(right, self.K2)
        left = [l ^ f for l, f in zip(left, f_output)]

        combined = left + right
        return self.permute(combined, IP_INV)

    def decrypt_block(self, block):
        IP = [2, 6, 3, 1, 4, 8, 5, 7]
        IP_INV = [4, 1, 3, 5, 7, 2, 8, 6]

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

        combined = left + right
        return self.permute(combined, IP_INV)

class SDESInterface:
    def __init__(self, root):
        self.root = root
        self.root.title("S-DES Encryption/Decryption")
        self.root.geometry("500x400")
        
        # Criar frames
        input_frame = ttk.LabelFrame(root, text="Input", padding="10")
        input_frame.pack(fill="x", padx=10, pady=5)
        
        result_frame = ttk.LabelFrame(root, text="Result", padding="10")
        result_frame.pack(fill="x", padx=10, pady=5)
        
        # Input fields
        ttk.Label(input_frame, text="Bitstring (8 bits):").grid(row=0, column=0, sticky="w")
        self.bitstring_entry = ttk.Entry(input_frame)
        self.bitstring_entry.grid(row=0, column=1, padx=5, pady=5, sticky="we")
        self.bitstring_entry.insert(0, "01110010")
        
        ttk.Label(input_frame, text="Key (10 bits):").grid(row=1, column=0, sticky="w")
        self.key_entry = ttk.Entry(input_frame)
        self.key_entry.grid(row=1, column=1, padx=5, pady=5, sticky="we")
        self.key_entry.insert(0, "1010000010")
        
        # Operation selection
        self.operation = tk.StringVar(value="encrypt")
        ttk.Radiobutton(input_frame, text="Encrypt", variable=self.operation, 
                       value="encrypt").grid(row=2, column=0)
        ttk.Radiobutton(input_frame, text="Decrypt", variable=self.operation, 
                       value="decrypt").grid(row=2, column=1)
        
        # Process button
        ttk.Button(input_frame, text="Process", command=self.process).grid(row=3, 
                  column=0, columnspan=2, pady=10)
        
        # Result field
        ttk.Label(result_frame, text="Result:").grid(row=0, column=0, sticky="w")
        self.result_entry = ttk.Entry(result_frame, state='readonly')
        self.result_entry.grid(row=0, column=1, padx=5, pady=5, sticky="we")
        
        # Configure grid
        input_frame.columnconfigure(1, weight=1)
        result_frame.columnconfigure(1, weight=1)
        
        # Adicionar campo para mostrar verificação
        verify_frame = ttk.LabelFrame(root, text="Verification", padding="10")
        verify_frame.pack(fill="x", padx=10, pady=5)
        self.verify_text = tk.Text(verify_frame, height=4, width=50)
        self.verify_text.pack(fill="both", expand=True)
        
    def process(self):
        bitstring = self.bitstring_entry.get().strip()
        key = self.key_entry.get().strip()
        
        # Converter strings para listas de inteiros
        bitstring_list = [int(bit) for bit in bitstring]
        key_list = [int(bit) for bit in key]
        
        try:
            # Usar exatamente o mesmo processo do código original
            sdes = SDES(key_list)
            
            # Primeiro, fazer a encriptação
            ciphertext = sdes.encrypt_block(bitstring_list)
            # Depois, fazer a decriptação do resultado
            decrypted = sdes.decrypt_block(ciphertext)
            
            # Mostrar resultados de verificação
            self.verify_text.delete(1.0, tk.END)
            self.verify_text.insert(tk.END, f"Original: {bitstring}\n")
            self.verify_text.insert(tk.END, f"Encrypted: {''.join(str(b) for b in ciphertext)}\n")
            self.verify_text.insert(tk.END, f"Decrypted: {''.join(str(b) for b in decrypted)}\n")
            
            # Mostrar o resultado solicitado
            if self.operation.get() == "encrypt":
                result = ciphertext
            else:
                result = decrypted
            
            result_string = ''.join(str(bit) for bit in result)
            self.result_entry.configure(state='normal')
            self.result_entry.delete(0, tk.END)
            self.result_entry.insert(0, result_string)
            self.result_entry.configure(state='readonly')
            
        except Exception as e:
            messagebox.showerror("Error", f"Processing error: {str(e)}")

if __name__ == "__main__":
    root = tk.Tk()
    app = SDESInterface(root)
    root.mainloop()