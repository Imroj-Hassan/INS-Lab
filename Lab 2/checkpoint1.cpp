#include <bits/stdc++.h>
using namespace std;
// decrypt a single character with a Caesar shift (lowercase only)
char decrypt_char(char c, int shift) {
    if (c >= 'a' && c <= 'z') {
        int x = (c - 'a' - shift) % 26;
        if (x < 0) x += 26;
        return char('a' + x);
    }
    if (c >= 'A' && c <= 'Z') {
        int x = (c - 'A' - shift) % 26;
        if (x < 0) x += 26;
        return char('A' + x);
    }
    return c; // non-letter unchanged
}
// decrypt whole string with given shift
string caesar_decrypt(const string &cipher, int shift) {
    string out;
    out.reserve(cipher.size());
    for (char c : cipher) out.push_back(decrypt_char(c, shift));
    return out;
}
int main() {
    string cipher = "odroboewscdrolocdcwkbdmyxdbkmdzvkdpybwyeddrobo";
    cout << "Ciphertext:\n" << cipher << "\n\n";
    cout << "Trying all 26 shifts (0..25). Look for the readable English line:\n\n";
    for (int s = 0; s < 26; ++s) {
        cout << "Shift " << setw(2) << s << ": " << caesar_decrypt(cipher, s) << "\n";
    }
    return 0;
}