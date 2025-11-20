#!/usr/bin/env python3
import os
import time
import argparse
import matplotlib.pyplot as plt
import pandas as pd
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.backends import default_backend
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import secrets
import base64

class CryptographicTool:
    def __init__(self):
        self.keys_dir = "keys"
        self.data_dir = "data"
        os.makedirs(self.keys_dir, exist_ok=True)
        os.makedirs(self.data_dir, exist_ok=True)
        self.generate_keys()
    
    def generate_keys(self):
        # Generate AES keys
        aes_128_key = secrets.token_bytes(16)
        aes_256_key = secrets.token_bytes(32)
        with open(os.path.join(self.keys_dir, "aes_128_key.key"), "wb") as f: f.write(aes_128_key)
        with open(os.path.join(self.keys_dir, "aes_256_key.key"), "wb") as f: f.write(aes_256_key)
        
        # Generate RSA key pair
        private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048, backend=default_backend())
        public_key = private_key.public_key()
        with open(os.path.join(self.keys_dir, "rsa_private.pem"), "wb") as f:
            f.write(private_key.private_bytes(encoding=serialization.Encoding.PEM, format=serialization.PrivateFormat.PKCS8, encryption_algorithm=serialization.NoEncryption()))
        with open(os.path.join(self.keys_dir, "rsa_public.pem"), "wb") as f:
            f.write(public_key.public_bytes(encoding=serialization.Encoding.PEM, format=serialization.PublicFormat.SubjectPublicKeyInfo))
        print("Keys generated successfully!")
    
    def load_aes_key(self, key_size=128):
        key_file = f"aes_{key_size}_key.key"
        with open(os.path.join(self.keys_dir, key_file), "rb") as f: return f.read()
    
    def load_rsa_keys(self):
        with open(os.path.join(self.keys_dir, "rsa_private.pem"), "rb") as f:
            private_key = serialization.load_pem_private_key(f.read(), password=None, backend=default_backend())
        with open(os.path.join(self.keys_dir, "rsa_public.pem"), "rb") as f:
            public_key = serialization.load_pem_public_key(f.read(), backend=default_backend())
        return private_key, public_key
    
    def aes_encrypt(self, input_file, output_file, key_size=128, mode='ECB'):
        start_time = time.time()
        key = self.load_aes_key(key_size)
        with open(os.path.join(self.data_dir, input_file), "rb") as f: plaintext = f.read()
        
        if mode.upper() == 'ECB':
            cipher = AES.new(key, AES.MODE_ECB)
            ciphertext = cipher.encrypt(pad(plaintext, AES.block_size))
        elif mode.upper() == 'CFB':
            iv = secrets.token_bytes(16)
            cipher = AES.new(key, AES.MODE_CFB, iv=iv)
            ciphertext = iv + cipher.encrypt(plaintext)
        
        with open(os.path.join(self.data_dir, output_file), "wb") as f: f.write(ciphertext)
        elapsed_time = time.time() - start_time
        print(f"AES-{key_size} {mode} Encryption: {elapsed_time:.4f}s")
        return elapsed_time
    
    def aes_decrypt(self, input_file, output_file, key_size=128, mode='ECB'):
        start_time = time.time()
        key = self.load_aes_key(key_size)
        with open(os.path.join(self.data_dir, input_file), "rb") as f: ciphertext = f.read()
        
        if mode.upper() == 'ECB':
            cipher = AES.new(key, AES.MODE_ECB)
            plaintext = unpad(cipher.decrypt(ciphertext), AES.block_size)
        elif mode.upper() == 'CFB':
            iv = ciphertext[:16]
            actual_ciphertext = ciphertext[16:]
            cipher = AES.new(key, AES.MODE_CFB, iv=iv)
            plaintext = cipher.decrypt(actual_ciphertext)
        
        with open(os.path.join(self.data_dir, output_file), "wb") as f: f.write(plaintext)
        elapsed_time = time.time() - start_time
        print(f"Decrypted: {plaintext.decode('utf-8')}")
        print(f"AES-{key_size} {mode} Decryption: {elapsed_time:.4f}s")
        return elapsed_time
    
    def rsa_encrypt(self, input_file, output_file):
        start_time = time.time()
        private_key, public_key = self.load_rsa_keys()
        with open(os.path.join(self.data_dir, input_file), "rb") as f: plaintext = f.read()
        ciphertext = public_key.encrypt(plaintext, padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA256()), algorithm=hashes.SHA256(), label=None))
        with open(os.path.join(self.data_dir, output_file), "wb") as f: f.write(ciphertext)
        elapsed_time = time.time() - start_time
        print(f"RSA Encryption: {elapsed_time:.4f}s")
        return elapsed_time
    
    def rsa_decrypt(self, input_file, output_file):
        start_time = time.time()
        private_key, public_key = self.load_rsa_keys()
        with open(os.path.join(self.data_dir, input_file), "rb") as f: ciphertext = f.read()
        plaintext = private_key.decrypt(ciphertext, padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA256()), algorithm=hashes.SHA256(), label=None))
        with open(os.path.join(self.data_dir, output_file), "wb") as f: f.write(plaintext)
        elapsed_time = time.time() - start_time
        print(f"Decrypted: {plaintext.decode('utf-8')}")
        print(f"RSA Decryption: {elapsed_time:.4f}s")
        return elapsed_time
    
    def rsa_sign(self, input_file, signature_file):
        start_time = time.time()
        private_key, public_key = self.load_rsa_keys()
        with open(os.path.join(self.data_dir, input_file), "rb") as f: data = f.read()
        signature = private_key.sign(data, padding.PSS(mgf=padding.MGF1(hashes.SHA256()), salt_length=padding.PSS.MAX_LENGTH), hashes.SHA256())
        with open(os.path.join(self.data_dir, signature_file), "wb") as f: f.write(signature)
        elapsed_time = time.time() - start_time
        print(f"RSA Signature: {elapsed_time:.4f}s")
        return elapsed_time
    
    def rsa_verify(self, input_file, signature_file):
        start_time = time.time()
        private_key, public_key = self.load_rsa_keys()
        with open(os.path.join(self.data_dir, input_file), "rb") as f: data = f.read()
        with open(os.path.join(self.data_dir, signature_file), "rb") as f: signature = f.read()
        try:
            public_key.verify(signature, data, padding.PSS(mgf=padding.MGF1(hashes.SHA256()), salt_length=padding.PSS.MAX_LENGTH), hashes.SHA256())
            result = "Signature VALID"
        except Exception as e: result = f"Signature INVALID: {str(e)}"
        elapsed_time = time.time() - start_time
        print(f"Verification: {result}")
        print(f"RSA Verify: {elapsed_time:.4f}s")
        return elapsed_time, result
    
    def sha256_hash(self, input_file):
        start_time = time.time()
        with open(os.path.join(self.data_dir, input_file), "rb") as f: data = f.read()
        digest = hashes.Hash(hashes.SHA256(), backend=default_backend())
        digest.update(data)
        hash_value = digest.finalize()
        elapsed_time = time.time() - start_time
        hash_hex = hash_value.hex()
        print(f"SHA-256: {hash_hex}")
        print(f"SHA-256 Time: {elapsed_time:.4f}s")
        with open(os.path.join(self.data_dir, "hash_output.txt"), "w") as f: f.write(hash_hex)
        return elapsed_time, hash_hex

def main():
    tool = CryptographicTool()
    parser = argparse.ArgumentParser(description='CSE-478 Lab 4 Cryptographic Tool')
    parser.add_argument('--interactive', action='store_true', help='Run in interactive mode')
    args = parser.parse_args()
    
    if args.interactive:
        print("Interactive mode - use functions directly in code")
    else:
        print("=== Running All Cryptographic Operations ===")
        tool.aes_encrypt("input.txt", "encrypted_aes.bin", 128, 'ECB')
        tool.aes_decrypt("encrypted_aes.bin", "decrypted_aes.txt", 128, 'ECB')
        tool.rsa_encrypt("input.txt", "encrypted_rsa.bin")
        tool.rsa_decrypt("encrypted_rsa.bin", "decrypted_rsa.txt")
        tool.rsa_sign("input.txt", "signature.bin")
        tool.rsa_verify("input.txt", "signature.bin")
        tool.sha256_hash("input.txt")
        print("=== All operations completed ===")

if __name__ == "__main__":
    main()
