def compare_hashes(hex1, hex2):
    hex1 = hex1.strip().lower()
    hex2 = hex2.strip().lower()
    
    num1 = int(hex1, 16)
    num2 = int(hex2, 16)
    
    differing_bits = bin(num1 ^ num2).count('1')
    total_bits = len(hex1) * 4
    
    same_bits = total_bits - differing_bits
    print(f"Same bits: {same_bits}/{total_bits}")
    print(f"Percentage similarity: {(same_bits/total_bits)*100:.2f}%")
    print(f"Bits changed: {differing_bits}/{total_bits} ({(differing_bits/total_bits)*100:.2f}%)")

# Read hashes from files
with open('H1_sha256.txt', 'r') as f:
    content = f.read()
    h1_line = content.split("= ")[1] if "= " in content else content

with open('H2_sha256.txt', 'r') as f:
    content = f.read()
    h2_line = content.split("= ")[1] if "= " in content else content

print("Original Hash (H1):", h1_line)
print("Modified Hash (H2):", h2_line)
print("\nBit Comparison:")
compare_hashes(h1_line, h2_line)
