# Caesar Cipher Brute Force Attack
# Try all possible shifts (1-25) to decrypt the message

cipher_text = "odroboewscdrolocdcwkbdmyxdbkmdzvkdpybwyeddrobo"

def caesar_decrypt(text, shift):
    """Decrypt Caesar cipher by shifting letters back"""
    result = ""
    for char in text:
        if char.isalpha():  # Only shift letters
            # Shift character back by 'shift' positions
            result += chr((ord(char) - ord('a') - shift) % 26 + ord('a'))
        else:
            result += char  # Keep non-letters as is
    return result

# Try all possible shifts
print(f"Encrypted: {cipher_text}\n")
for shift in range(1, 26):
    print(f"Shift {shift:2d}: {caesar_decrypt(cipher_text, shift)}")
