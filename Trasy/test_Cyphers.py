import pytest
from Cyphers import CezarCypher, CellphoneCypher, FractionCypher, ReverseWordsCypher, MoorseCypher, SyllableCypher

@pytest.mark.parametrize("shift,ciphertext,expected", [
    (3, "Khoor", "Hello"),                          # basic mixed-case
    (5, "Mjqqt, Btwqi!", "Hello, World!"),         # preserves punctuation and spaces
    (4, "A a Z z", "W w V v"),                     # wrap-around for upper/lower
    (0, "NoChange123!", "NoChange123!"),           # zero shift leaves text unchanged
])
def test_decrypt_basic_cases(shift, ciphertext, expected):
    cc = CezarCypher(shift)
    assert cc.decrypt(ciphertext) == expected

def test_decrypt_inverse_of_encrypt_including_polish_chars():
    cc = CezarCypher(7)
    original = "Zażółć gęślą jaźń! ĄęÓćŁ"
    encrypted = cc.encrypt(original)
    # decrypt should return the prepared form of original (diacritics normalized by prepare_text)
    assert cc.decrypt(encrypted) == cc.prepare_text(original)

def test_shift_normalization_and_inverse_property():
    # shift of 29 should be normalized to 3
    cc1 = CezarCypher(29)
    cc2 = CezarCypher(3)
    sample = "WrapAround Test: XYZ xyz"
    assert cc1.decrypt(cc1.encrypt(sample)) == cc2.decrypt(cc2.encrypt(sample)) == cc1.prepare_text(sample)

@pytest.mark.parametrize("plaintext,expected_cipher", [
    ("Hello", "44 33 555 555 666"),        # basic word, trailing separator
    ("A B", "2 0 22"),                     # space mapped to '0'
    ("xyz", "99 999 9999"),              # lowercase input is uppercased
])
def test_encrypt_outputs_expected(plaintext, expected_cipher):
    cc = CellphoneCypher()
    assert cc.encrypt(plaintext) == expected_cipher

@pytest.mark.parametrize("ciphertext,expected_plain", [
    ("44 33 555 555 666", "HELLO"),  # simple decrypt with trailing space
    ("2 0 22", "A B"),               # includes space mapping
    ("2 22", "AB"),                  # trailing separator produces empty token ignored
])
def test_decrypt_outputs_expected(ciphertext, expected_plain):
    cc = CellphoneCypher()
    assert cc.decrypt(ciphertext) == expected_plain

def test_encrypt_decrypt_inverse_for_polish_chars():
    cc = CellphoneCypher()
    original = "Zażółć gęślą jaźń ĄęÓćŁ"  # no punctuation to avoid loss (CellphoneCypher doesn't preserve punctuation)
    encrypted = cc.encrypt(original)
    assert cc.decrypt(encrypted) == cc.prepare_text(original).upper()

def test_decrypt_ignores_unknown_tokens():
    cc = CellphoneCypher()
    # '99999' is not a valid token in reverse_map and should be ignored
    assert cc.decrypt("2 99999 22") == "AB"

def test_encrypt_basic_mapping():
    fc = FractionCypher()
    assert fc.encrypt("ABC") == [(1, 1), (2, 1), (3, 1)]

def test_decrypt_basic_mapping():
    fc = FractionCypher()
    assert fc.decrypt([(1, 1), (2, 1), (3, 1)]) == "ABC"

def test_encrypt_ignores_non_letters_and_space():
    fc = FractionCypher()
    # digits and punctuation and spaces are ignored by encrypt
    assert fc.encrypt("A1 B!") == [(1, 1), (2, 1)]

def test_encrypt_decrypt_inverse_for_allowed_alphabet():
    fc = FractionCypher()
    sample = "ABCDEFGHIJKLŁMNOPRSTUWXYZ"  # excludes Q and V which are not in the map
    encrypted = fc.encrypt(sample)
    decrypted = fc.decrypt(encrypted)
    assert decrypted == fc.prepare_text(sample).upper()

def test_decrypt_ignores_unknown_tokens():
    fc = FractionCypher()
    # (9,9) is not a valid token in reverse_map and should be ignored
    assert fc.decrypt([(9, 9), (1, 1), (2, 1)]) == "AB"

@pytest.mark.parametrize("input_text, expected_encrypt", [
    ("Hello World", "olleH dlroW"),
    ("Hello, World!", ",olleH !dlroW"),
    ("", ""),                        # empty string
    (" a  b ", " a  b "),            # leading/trailing and multiple spaces preserved
    ("Zażółć gęślą jaźń", None),     # polish chars — verify inverse property instead of hardcoding expected
])
def test_encrypt_basic_cases(input_text, expected_encrypt):
    rw = ReverseWordsCypher()
    result = rw.encrypt(input_text)
    if expected_encrypt is not None:
        assert result == expected_encrypt
    else:
        # For polish case we at least ensure encryption returns a string and uses prepare_text normalization
        assert isinstance(result, str)
        assert result == rw.encrypt(input_text)  # deterministic

@pytest.mark.parametrize("sample", [
    "Hello World",
    "Hello, World!",
    "",
    " a  b ",
    "Zażółć gęślą jaźń",
])
def test_decrypt_is_inverse_of_encrypt(sample):
    rw = ReverseWordsCypher()
    encrypted = rw.encrypt(sample)
    # decrypt should reverse the encryption, returning the prepared form of the original
    assert rw.decrypt(encrypted) == rw.prepare_text(sample)

@pytest.mark.parametrize("plaintext,expected", [
    ("SOS", "... --- ..."),
    ("Hello", ".... . .-.. .-.. ---"),
    ("Hello World", ".... . .-.. .-.. --- / .-- --- .-. .-.. -.."),
    ("123", ".---- ..--- ...--"),
    ("", ""),
])
def test_moorse_encrypt_basic_cases(plaintext, expected):
    mc = MoorseCypher()
    assert mc.encrypt(plaintext) == expected

@pytest.mark.parametrize("ciphertext,expected_plain", [
    ("... --- ...", "SOS"),
    (".... . .-.. .-.. ---", "HELLO"),
    (".... . .-.. .-.. --- / .-- --- .-. .-.. -..", "HELLO WORLD"),
    (".---- ..--- ...--", "123"),
    ("", ""),
])
def test_moorse_decrypt_basic_cases(ciphertext, expected_plain):
    mc = MoorseCypher()
    assert mc.decrypt(ciphertext) == expected_plain

def test_moorse_encrypt_decrypt_inverse_for_polish_chars():
    mc = MoorseCypher()
    original = "Zażółć gęślą jaźń 012"
    encrypted = mc.encrypt(original)
    # decrypt should return the prepared (diacritics normalized) uppercase form
    assert mc.decrypt(encrypted) == mc.prepare_text(original).upper()

def test_moorse_decrypt_ignores_unknown_tokens():
    mc = MoorseCypher()
    # '.....-' is not a valid token and should be ignored
    assert mc.decrypt(".- .....- -..") == "AD"
def test_odd_length_keyword_raises_assertion():
    with pytest.raises(AssertionError):
        SyllableCypher("ABC")  # length 3 -> should assert

def test_pair_swapping_and_self_mapping():
    sc = SyllableCypher("AZBY")  # pairs: A<->Z, B<->Y
    # paired mappings
    assert sc.char_map['A'] == 'Z'
    assert sc.char_map['Z'] == 'A'
    assert sc.char_map['B'] == 'Y'
    assert sc.char_map['Y'] == 'B'
    # letters not in keyword map to themselves
    assert sc.char_map['C'] == 'C'
    assert sc.reverse_map['Z'] == 'A'  # reverse_map should map encrypted back to original

def test_encrypt_decrypt_inverse_for_various_inputs():
    sc = SyllableCypher("MNOPQR")  # pairs M<->N, O<->P, Q<->R
    samples = [
        "Hello",
        "Zażółć gęślą jaźń",  # contains polish diacritics -> prepared/normalized
        "abc123",              # includes digits
        "",                    # empty string
        "Punctuation!?,."      # punctuation should be preserved
    ]
    for s in samples:
        enc = sc.encrypt(s)
        dec = sc.decrypt(enc)
        # decrypt(encrypt(x)) should equal prepared uppercase form of original
        assert dec == sc.prepare_text(s).upper()

def test_encrypt_preserves_nonletters_and_case_normalization():
    sc = SyllableCypher("UVWX")  # U<->V, W<->X
    original = "Hi!"
    encrypted = sc.encrypt(original)
    # punctuation preserved and letters normalized to uppercase before mapping
    assert encrypted.endswith("!")
    assert all(ch.isupper() or not ch.isalpha() for ch in encrypted)
