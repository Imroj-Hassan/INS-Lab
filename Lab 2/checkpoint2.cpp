#include <bits/stdc++.h>
using namespace std;

// English frequency order (most -> least)
const string ENG_ORDER = "etaoinshrdlcumwfgypbvkjxqz";

// basic list of common small words to reward
const vector<string> COMMON = {" the ", " and ", " of ", " to ", " a ", " in ", " is "};

// count letter frequencies in ciphertext (lowercase)
array<int,26> count_freq(const string &s){
    array<int,26> cnt; cnt.fill(0);
    for(char c: s) if (c >= 'a' && c <= 'z') cnt[c-'a']++;
    return cnt;
}

// build initial key: most frequent cipher letters -> ENG_ORDER
array<char,26> initial_key(const string &cipher){
    auto cnt = count_freq(cipher);
    vector<int> idx(26); iota(idx.begin(), idx.end(), 0);
    sort(idx.begin(), idx.end(), [&](int a,int b){ return cnt[a] > cnt[b]; });
    array<char,26> key; key.fill('?');
    for(int i=0;i<26;i++) key[idx[i]] = ENG_ORDER[i];
    // fill any remaining with leftover letters (simple)
    vector<bool> used(26,false);
    for(int i=0;i<26;i++) if(key[i] != '?') used[key[i]-'a'] = true;
    int p=0;
    for(int i=0;i<26;i++){
        if(key[i]=='?'){
            while(p<26 && used[p]) p++;
            key[i] = char('a' + p);
            used[p] = true;
        }
    }
    return key;
}

// decrypt using key (key[cipher_index] = plaintext letter)
string decrypt_with_key(const array<char,26> &key, const string &cipher){
    string out; out.reserve(cipher.size());
    for(char c: cipher){
        if (c >= 'a' && c <= 'z') out.push_back(key[c-'a']);
        else if (c >= 'A' && c <= 'Z') {
            char p = key[c - 'A'];
            out.push_back(char(toupper(p)));
        } else out.push_back(c);
    }
    return out;
}

// very simple scoring: reward common words and frequent letters
int score_plain(const string &plain){
    int score = 0;
    string low = plain;
    for(char &c: low) if(c >= 'A' && c <= 'Z') c = c - 'A' + 'a';
    // add points for each common word occurrence
    for(auto &w: COMMON){
        size_t pos = 0;
        while((pos = low.find(w, pos)) != string::npos){
            score += 10;
            pos += w.size();
        }
    }
    // small letter-frequency bonus: reward 'e' and 't' etc.
    for(char c: low){
        if (c == 'e') score += 1;
        if (c == 't') score += 1;
    }
    return score;
}

int main(){
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    // Put either cipher1 or cipher2 here. For demo we'll show both one by one.
    string cipher1 = "af p xpkcaqvnpk pfg, af ipqe qpri, gauuikifc tpw, ceiri udvk tiki afgarxifrphni cd eao--wvmd popkwn, hiqpvri du ear jvaql vfgikrcpfgafm du cei xkafqaxnir du xrwqedearcdkw pfg du ear aopmafpcasi xkdhafmr afcd fit pkipr. ac tpr qdoudkcafm cd lfdt cepc au pfwceafm epxxifig cd ringdf eaorinu hiudki cei opceiopcaqr du cei uaing qdvng hi qdoxnicinw tdklig dvc--pfg edt rndtnw ac xkdqiigig, pfg edt odvfcpafdvr cei dhrcpqnir--ceiki tdvng pc niprc kiopaf dfi mddg oafg cepc tdvng qdfcafvi cei kiripkqe";
    string cipher2 = "aceah toz puvg vcdl omj puvg yudqecov, omj loj auum klu thmjuv hs klu zlcvu shv zcbkg guovz, upuv zcmdu lcz vuwovroaeu jczoyyuovomdu omj qmubyudkuj vukqvm. klu vcdluz lu loj avhqnlk aodr svhw lcz kvopuez loj mht audhwu o ehdoe eunumj, omj ck toz yhyqeoveg auecupuj, tlokupuv klu hej sher wcnlk zog, klok klu lcee ok aon umj toz sqee hs kqmmuez zkqssuj tckl kvuozqvu.";

    // Choose which to solve: change this variable to cipher1 or cipher2
    string cipher = cipher2; // set to cipher1 for the short one, cipher2 (longer) likely better

    // lowercase the ciphertext for processing (keep non-letters)
    string low = cipher;
    for (char &c : low) if (c >= 'A' && c <= 'Z') c = c - 'A' + 'a';

    // 1) Initial guess: frequency mapping
    auto key = initial_key(low);
    string plain = decrypt_with_key(key, low);
    cout << "=== Initial (frequency) decryption ===\n";
    cout << plain << "\n\n";

    // 2) Simple hill-climb: try some random swaps and keep better results
    int best_score = score_plain(plain);
    string best_plain = plain;
    array<char,26> best_key = key;

    mt19937 rng((unsigned)chrono::high_resolution_clock::now().time_since_epoch().count());
    const int TRIES = 2000; // small number to keep code simple & fast
    for (int t = 0; t < TRIES; ++t) {
        // make a candidate by swapping two letters in the key
        array<char,26> cand_key = best_key;
        int i = rng() % 26, j = rng() % 26;
        swap(cand_key[i], cand_key[j]);
        string cand_plain = decrypt_with_key(cand_key, low);
        int sc = score_plain(cand_plain);
        if (sc > best_score) {
            best_score = sc;
            best_plain = cand_plain;
            best_key = cand_key;
            // print progress (small)
            cout << "[improved score " << best_score << "] " << best_plain.substr(0,120) << "\n";
        }
    }

    cout << "\n=== Best after simple swaps (score=" << best_score << ") ===\n";
    cout << best_plain << "\n\n";
    cout << "\n";
    return 0;
}
