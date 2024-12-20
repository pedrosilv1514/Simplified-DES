import tkinter as tk
from tkinter import ttk, messagebox
from sdes_project import SDES

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
        
        ttk.Label(input_frame, text="Key (10 bits):").grid(row=1, column=0, sticky="w")
        self.key_entry = ttk.Entry(input_frame)
        self.key_entry.grid(row=1, column=1, padx=5, pady=5, sticky="we")
        
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
        
        # Debug info
        debug_frame = ttk.LabelFrame(root, text="Debug Info", padding="10")
        debug_frame.pack(fill="x", padx=10, pady=5)
        self.debug_text = tk.Text(debug_frame, height=5, width=50)
        self.debug_text.pack(fill="both", expand=True)
        
        # Configure grid
        input_frame.columnconfigure(1, weight=1)
        result_frame.columnconfigure(1, weight=1)
        
    def validate_input(self, bitstring, key):
        if not all(bit in '01' for bit in bitstring) or len(bitstring) != 8:
            messagebox.showerror("Error", "Bitstring must be 8 bits (0s and 1s only)")
            return False
            
        if not all(bit in '01' for bit in key) or len(key) != 10:
            messagebox.showerror("Error", "Key must be 10 bits (0s and 1s only)")
            return False
            
        return True
        
    def process(self):
        bitstring = self.bitstring_entry.get().strip()
        key = self.key_entry.get().strip()
        
        if not self.validate_input(bitstring, key):
            return
            
        # Convert strings to lists of integers
        bitstring_list = [int(bit) for bit in bitstring]
        key_list = [int(bit) for bit in key]
        
        try:
            # Create SDES instance
            sdes = SDES(key_list)
            
            # Process based on selected operation
            if self.operation.get() == "encrypt":
                result = sdes.encrypt_block(bitstring_list)
                # For verification, also decrypt
                verify = sdes.decrypt_block(result)
            else:
                result = sdes.decrypt_block(bitstring_list)
                # For verification, also encrypt
                verify = sdes.encrypt_block(result)
            
            # Convert result back to string and display
            result_string = ''.join(str(bit) for bit in result)
            self.result_entry.configure(state='normal')
            self.result_entry.delete(0, tk.END)
            self.result_entry.insert(0, result_string)
            self.result_entry.configure(state='readonly')
            
            # Update debug info
            self.debug_text.delete(1.0, tk.END)
            self.debug_text.insert(tk.END, f"Input: {bitstring}\n")
            self.debug_text.insert(tk.END, f"Key: {key}\n")
            self.debug_text.insert(tk.END, f"Operation: {self.operation.get()}\n")
            self.debug_text.insert(tk.END, f"Result: {result_string}\n")
            verify_string = ''.join(str(bit) for bit in verify)
            self.debug_text.insert(tk.END, f"Verification: {verify_string}")
            
        except Exception as e:
            messagebox.showerror("Error", f"Processing error: {str(e)}")

if __name__ == "__main__":
    root = tk.Tk()
    app = SDESInterface(root)
    root.mainloop()