def break_caesar_simple(ciphertext):
    print("Breaking Caesar Cipher...")
    print(f"Ciphertext: {ciphertext}")
    print("-" * 50)
    
    for shift in range(1, 26):
        plaintext = ""
        for char in ciphertext:
            if char.isalpha():
                # Convert to number (a=0, b=1, ..., z=25)
                char_num = ord(char) - ord('a')
                # Apply shift and wrap around
                new_num = (char_num - shift) % 26
                # Convert back to character
                plaintext += chr(new_num + ord('a'))
            else:
                plaintext += char
        
        print(f"Shift {shift:2d}: {plaintext}")

# Example 1: Easy to understand
print("=== EXAMPLE 1 ===")
cipher1 = "khoorzruog"  # "hello world" with shift 3
break_caesar_simple(cipher1)

print("\n" + "="*50 + "\n")

# Example 2: Your actual lab cipher
print("=== LAB CIPHER ===")
cipher_lab = "odrobcewscdrolocdewkbdmyxdbkmdzvkdpybwyeddrobo"
break_caesar_simple(cipher_lab)