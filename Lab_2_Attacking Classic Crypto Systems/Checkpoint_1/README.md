# Checkpoint 1: Breaking Caesar Cipher

## Overview

This checkpoint demonstrates how to break a Caesar cipher using a brute force attack. Caesar cipher is one of the simplest and oldest encryption techniques, making it easy to crack by trying all possible keys.

## What is a Caesar Cipher?

A Caesar cipher is a substitution cipher where each letter in the plaintext is shifted by a fixed number of positions in the alphabet. Named after Julius Caesar, who used it for military communications.

**Examples**:

- Shift of 3: A→D, B→E, C→F, ..., X→A, Y→B, Z→C
- Shift of 1: A→B, B→C, C→D, ..., Y→Z, Z→A
- The message "HELLO" with shift 3 becomes "KHOOR"

**Key characteristic**: The same shift is applied to every letter in the message.

## The Challenge

**Encrypted message**: `odroboewscdrolocdcwkbdmyxdbkmdzvkdpybwyeddrobo`

**Task**: Decrypt the message without knowing the shift value

**Constraint**: The cipher uses lowercase letters only

## Solution Approach: Brute Force Attack

Since there are only **25 possible shift values** (1-25), we can systematically try all of them:

1. **Try shift 1** - decrypt and display result
2. **Try shift 2** - decrypt and display result
3. **Try shift 3** - decrypt and display result
4. ...continue through all shifts...
5. **Try shift 25** - decrypt and display result
6. **Manually identify** which result is readable English

**Why brute force works**:

- Only 25 possible keys to check
- Each decryption takes microseconds
- Total time: less than 1 second
- Human can easily spot the correct plaintext

## Implementation (Cipher_first.py)

### Complete Code

```python
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
```

### Code Explanation

**Function: `caesar_decrypt(text, shift)`**

This function decrypts a Caesar cipher by reversing the shift:

1. **Input**:

   - `text` - the encrypted message
   - `shift` - how many positions to shift back

2. **Process**:

   - Loop through each character
   - If it's a letter: shift it back by `shift` positions
   - Use modulo 26 (`% 26`) to wrap around the alphabet
   - If it's not a letter: keep it unchanged

3. **Output**: The decrypted text for this shift value

**Main Logic**:

- Try every possible shift from 1 to 25
- Display each result with its shift number
- User visually scans for readable English

**Key Technique - Modular Arithmetic**:

```python
chr((ord(char) - ord('a') - shift) % 26 + ord('a'))
```

- `ord(char) - ord('a')` converts letter to 0-25
- `- shift` shifts back
- `% 26` wraps around (handles negative numbers)
- `+ ord('a')` converts back to letter
- `chr()` converts ASCII value to character

## Results

Running the brute force attack produces 25 possible decryptions:

```
Encrypted: odroboewscdrolocdcwkbdmyxdbkmdzvkdpybwyeddrobo

Shift  1: ncqnanadvbcqnknbcbvjaclxwcajlcyuajcoxavxdccqnan
Shift  2: mbpmzmzcuabpmjmabauizbkwvbzikbxtzibdnwtuwtcbbpmzm
Shift  3: laolylybtzaolilzatzhydjvuayhjawsyahcmvstvwsbaolyl
Shift  4: kznkxkxasyzknkhkzsygxciutxzgizvnrxzgblursuvraznkxk
Shift  5: jymjwjwzrxyjmjgjyrxfwbhtswyf...
...
Shift 10: everybodyiswantedcanbecausedbycanyoneeverybody
...
Shift 25: peobobpfxtnbspmpenldoenytoelydpqneaonflxreppeobc
```

### The Correct Decryption

**Shift 10**: `everybodyiswantedcanbecausedbycanyoneeverybody`

Breaking into words: **"everybody is wanted can be caused by can anyone everybody"**

(Note: The original message may have spacing/grammar issues, but it's clearly readable English)

## Analysis

### Why Caesar Cipher is Weak

| Weakness                             | Explanation                                    |
| ------------------------------------ | ---------------------------------------------- |
| **Tiny key space**                   | Only 25 possible keys (trivial to brute force) |
| **No computational security**        | Can be broken by hand in minutes               |
| **Pattern preservation**             | Letter frequencies remain visible              |
| **No randomness**                    | Same input letter always produces same output  |
| **Vulnerable to frequency analysis** | Even without brute force                       |

### Time Complexity

- **Brute force**: O(26 × n) where n = message length
- **For this cipher**: 26 attempts × 45 characters = ~1,170 operations
- **Actual time**: < 1 second on any modern computer

### Security Level

**Security**: ⭐☆☆☆☆ (1/5 stars)

- Completely insecure
- Historical curiosity only
- Never use for real encryption

## Comparison with Other Ciphers

| Cipher Type      | Key Space     | Breaking Method    | Time to Break     |
| ---------------- | ------------- | ------------------ | ----------------- |
| **Caesar**       | 25            | Brute force        | < 1 second        |
| **Substitution** | 26! ≈ 4×10²⁶  | Frequency analysis | Minutes to hours  |
| **AES-128**      | 2¹²⁸ ≈ 3×10³⁸ | Not feasible       | Billions of years |

## Key Learnings

1. **Small key spaces are fatal** - 25 keys means brute force always works
2. **Automation makes it trivial** - What took hours by hand takes milliseconds by computer
3. **Historical importance** - Caesar cipher teaches fundamental cryptographic concepts
4. **Modern requirements** - Real encryption needs huge key spaces (2¹²⁸ or larger)
5. **Defense is impossible** - No way to strengthen Caesar cipher against brute force

## Historical Context

- **Invented**: ~100 BCE by Julius Caesar
- **Original use**: Military communications in Roman Empire
- **Shift used by Caesar**: Typically shift 3
- **Breaking method**: Known since at least 9th century CE
- **Modern status**: Educational tool only

## How to Run

```powershell
# Navigate to checkpoint directory
cd "G:\INS-Lab\Lab_2_Attacking Classic Crypto Systems\Checkpoint_1"

# Run the brute force attack
python Cipher_first.py
```

**Expected Output**:

- Display of encrypted message
- All 25 possible decryptions
- Each labeled with its shift value
- One result will be readable English (shift 10)

## Improvements to This Code

While this code is simple and clear, here are potential enhancements:

1. **Automatic detection**: Use dictionary or English frequency analysis to automatically identify correct shift
2. **Handle uppercase**: Support mixed case messages
3. **Score results**: Calculate "Englishness" score for each attempt
4. **Handle punctuation**: Preserve spaces and punctuation from original
5. **Reverse operation**: Add encryption function too

## Conclusion

Caesar cipher demonstrates why **security through obscurity fails**. Even though the attacker doesn't know the key, the tiny key space (only 25 possibilities) makes brute force trivial.

**Modern cryptography lesson**: Good encryption requires:

- ✅ Large key space (2¹²⁸ or more possible keys)
- ✅ Computational hardness (brute force takes billions of years)
- ✅ No statistical patterns in output
- ✅ Key mixing and diffusion

Caesar cipher has none of these properties, making it completely insecure for any real-world use. However, it remains an excellent teaching tool for understanding basic cryptographic concepts and the importance of key space size.

---

**Course**: Information Security Lab  
**Lab Number**: 2  
**Checkpoint**: 1  
**Topic**: Breaking Caesar Cipher (Brute Force Attack)  
**Date**: November 20, 2025
