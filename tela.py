import tkinter as tk
from tkinter import messagebox
from sdes_project import SDES


def validate_binary_input(binary_string, length):
    if len(binary_string) != length:
        raise ValueError(f"A entrada deve ter exatamente {length} bits.")
    if not all(c in '01' for c in binary_string):
        raise ValueError("A entrada deve conter apenas '0' e '1'.")
    return [int(bit) for bit in binary_string]  # Conversão correta


def encrypt():
    try:
        key_input = key_entry.get().strip()
        block_input = block_entry.get().strip()

        key = validate_binary_input(key_input, 10)
        block = validate_binary_input(block_input, 8)

        sdes = SDES(key)
        ciphertext = sdes.encrypt_block(block)

        result_label.config(text=f"Texto Cifrado: {''.join(map(str, ciphertext))}")
    except ValueError as e:
        messagebox.showerror("Erro", str(e))


def decrypt():
    try:
        # Obtenção dos dados de entrada
        key_input = key_entry.get().strip()
        block_input = block_entry.get().strip()

        # Validação e conversão
        key = validate_binary_input(key_input, 10)
        block = validate_binary_input(block_input, 8)

        # Exibição dos dados processados para depuração
        print(f"Chave: {key}")  # Deve ser [1, 0, 1, 0, 0, 0, 0, 0, 1, 0]
        print(f"Bloco: {block}")  # Deve ser [0, 1, 1, 1, 0, 0, 1, 0]

        # Instanciação do SDES e descriptografia
        sdes = SDES(key)
        plaintext = sdes.decrypt_block(block)

        # Exibição do texto decifrado no terminal para depuração
        print(f"Texto Decifrado: {plaintext}")  # Deve ser [0, 1, 1, 1, 0, 0, 1, 0]

        # Atualização da interface com o resultado correto
        result_label.config(text=f"Texto Decifrado: {''.join(map(str, plaintext))}")
    except ValueError as e:
        messagebox.showerror("Erro", str(e))


def start_app():
    result_label.config(text="")


# Configuração da interface gráfica
root = tk.Tk()
root.title("S-DES Encryptor/Decryptor")

frame = tk.Frame(root, padx=10, pady=10)
frame.pack(pady=20)

key_label = tk.Label(frame, text="Chave (10 bits):")
key_label.grid(row=0, column=0, sticky="e")

key_entry = tk.Entry(frame, width=15)
key_entry.grid(row=0, column=1, pady=5)

block_label = tk.Label(frame, text="Bloco de Dados (8 bits):")
block_label.grid(row=1, column=0, sticky="e")

block_entry = tk.Entry(frame, width=15)
block_entry.grid(row=1, column=1, pady=5)

result_label = tk.Label(root, text="", font=("Arial", 12), fg="blue")
result_label.pack(pady=10)

encrypt_button = tk.Button(root, text="Encriptar", command=encrypt, width=15)
encrypt_button.pack(side="left", padx=10)

decrypt_button = tk.Button(root, text="Decriptar", command=decrypt, width=15)
decrypt_button.pack(side="right", padx=10)

start_button = tk.Button(root, text="Iniciar", command=start_app, width=15)
start_button.pack(pady=20)

root.mainloop()
