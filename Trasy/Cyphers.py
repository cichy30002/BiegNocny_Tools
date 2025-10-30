from docx.oxml import OxmlElement

class Cypher:
    def __init__(self):
        pass

    def encrypt(self, plaintext: str) -> str:
        raise NotImplementedError("Encrypt method not implemented.")
        pass

    def decrypt(self, ciphertext: str) -> str:
        raise NotImplementedError("Decrypt method not implemented.")
        pass

    def prepare_text(self, text: str) -> str:
        polish_dict = {
            'ą': 'a',
            'ć': 'c',
            'ę': 'e',
            'ł': 'l',
            'ń': 'n',
            'ó': 'o',
            'ś': 's',
            'ź': 'z',
            'ż': 'z',
            'Ą': 'A',
            'Ć': 'C',
            'Ę': 'E',
            'Ł': 'L',
            'Ń': 'N',
            'Ó': 'O',
            'Ś': 'S',
            'Ź': 'Z',
            'Ż': 'Z'
        }
        for pl_char, repl_char in polish_dict.items():
            text = text.replace(pl_char, repl_char)
        return text
    
class CezarCypher(Cypher):
    def __init__(self, shift: int):
        super().__init__()
        self.shift = shift % 26

    def encrypt(self, plaintext: str) -> str:
        plaintext = self.prepare_text(plaintext)
        ciphertext = ""
        for char in plaintext:
            if char.isalpha():
                base = ord('A') if char.isupper() else ord('a')
                encrypted_char = chr((ord(char) - base + self.shift) % 26 + base)
                ciphertext += encrypted_char
            else:
                ciphertext += char
        return ciphertext

    def decrypt(self, ciphertext: str) -> str:
        ciphertext = self.prepare_text(ciphertext)
        plaintext = ""
        for char in ciphertext:
            if char.isalpha():
                base = ord('A') if char.isupper() else ord('a')
                decrypted_char = chr((ord(char) - base - self.shift) % 26 + base)
                plaintext += decrypted_char
            else:
                plaintext += char
        return plaintext
    
class CellphoneCypher(Cypher):
    def __init__(self):
        super().__init__()
        self.char_map = {
            'A': '2', 'B': '22', 'C': '222',
            'D': '3', 'E': '33', 'F': '333',
            'G': '4', 'H': '44', 'I': '444',
            'J': '5', 'K': '55', 'L': '555',
            'M': '6', 'N': '66', 'O': '666',
            'P': '7', 'Q': '77', 'R': '777', 'S': '7777',
            'T': '8', 'U': '88', 'V': '888',
            'W': '9', 'X': '99', 'Y': '999', 'Z': '9999',
            ' ': '0'
        }
        self.reverse_map = {v: k for k, v in self.char_map.items()}

    def encrypt(self, plaintext: str) -> str:
        plaintext = self.prepare_text(plaintext).upper()
        ciphertext = ""
        for char in plaintext:
            ciphertext += self.char_map.get(char, '')
            ciphertext += ' '
        ciphertext = ciphertext.strip()
        return ciphertext

    def decrypt(self, ciphertext: str) -> str:
        plaintext = ""
        tokens = ciphertext.split(' ')
        for token in tokens:
            if token in self.reverse_map:
                plaintext += self.reverse_map[token]
        return plaintext
    
class FractionCypher(Cypher):
    def __init__(self):
        super().__init__()
        self.char_map = {
            'A': (1, 1), 'B': (2, 1), 'C': (3, 1), 'D': (4, 1), 'E': (5, 1),
            'F': (1, 2), 'G': (2, 2), 'H': (3, 2), 'I': (4, 2), 'J': (5, 2),
            'K': (1, 3), 'L': (2, 3), 'Ł': (3, 3), 'M': (4, 3), 'N': (5, 3),
            'O': (1, 4), 'P': (2, 4), 'R': (3, 4), 'S': (4, 4), 'T': (5, 4),
            'U': (1, 5), 'W': (2, 5), 'X': (3, 5), 'Y': (4, 5), 'Z': (5, 5)
        }
        self.reverse_map = {v: k for k, v in self.char_map.items()}

    def encrypt_oMath(self, plaintext: str) -> list:
        fractions = self.encrypt(plaintext)
        return self.to_oMath(fractions)

    def encrypt(self, plaintext: str) -> list:
        plaintext = self.prepare_text(plaintext).upper()
        ciphertext = []
        for char in plaintext:
            if char in self.char_map:
                ciphertext.append(self.char_map[char])
        return ciphertext

    def decrypt(self, ciphertext: list) -> str:
        plaintext = ""
        for token in ciphertext:
            if token in self.reverse_map:
                plaintext += self.reverse_map[token]
        return plaintext
    
    def prepare_text(self, text: str) -> str:
        polish_dict_without_l = {
            'ą': 'a',
            'ć': 'c',
            'ę': 'e',
            'ń': 'n',
            'ó': 'o',
            'ś': 's',
            'ź': 'z',
            'ż': 'z',
            'Ą': 'A',
            'Ć': 'C',
            'Ę': 'E',
            'Ń': 'N',
            'Ó': 'O',
            'Ś': 'S',
            'Ź': 'Z',
            'Ż': 'Z'
        }
        for pl_char, repl_char in polish_dict_without_l.items():
            text = text.replace(pl_char, repl_char)
        return text

    def to_oMath(fractions: list) -> OxmlElement:
        oMath = OxmlElement('m:oMath')

        for num_val, den_val in fractions:
            f = OxmlElement('m:f')  # Fraction
            num = OxmlElement('m:num')
            den = OxmlElement('m:den')
            num_t = OxmlElement('m:t')
            den_t = OxmlElement('m:t')

            num_t.text = str(num_val)
            den_t.text = str(den_val)

            num.append(num_t)
            den.append(den_t)
            f.append(num)
            f.append(den)
            oMath.append(f)

        return oMath
        
class ReverseWordsCypher(Cypher):
    def __init__(self):
        super().__init__()
    
    def encrypt(self, plaintext: str) -> str:
        plaintext = self.prepare_text(plaintext)
        words = plaintext.split(' ')
        reversed_words = [word[::-1] for word in words]
        return ' '.join(reversed_words)
    
    def decrypt(self, ciphertext: str) -> str:
        # decryption is the same as encryption
        return self.encrypt(ciphertext)
    
class MoorseCypher(Cypher):
    def __init__(self):
        super().__init__()
        self.char_map = {
            'A': '.-', 'B': '-...', 'C': '-.-.', 'D': '-..', 'E': '.',
            'F': '..-.', 'G': '--.', 'H': '....', 'I': '..', 'J': '.---',
            'K': '-.-', 'L': '.-..', 'M': '--', 'N': '-.', 'O': '---',
            'P': '.--.', 'Q': '--.-', 'R': '.-.', 'S': '...', 'T': '-',
            'U': '..-', 'V': '...-', 'W': '.--', 'X': '-..-', 'Y': '-.--',
            'Z': '--..',
            '1': '.----', '2': '..---', '3': '...--', '4': '....-', '5': '.....',
            '6': '-....', '7': '--...', '8': '---..', '9': '----.', '0': '-----',
            ' ': '/'
        }
        self.reverse_map = {v: k for k, v in self.char_map.items()}

    def encrypt(self, plaintext: str) -> str:
        plaintext = self.prepare_text(plaintext).upper()
        ciphertext = ""
        for char in plaintext:
            ciphertext += self.char_map.get(char, '') + ' '
        return ciphertext.strip()

    def decrypt(self, ciphertext: str) -> str:
        plaintext = ""
        tokens = ciphertext.split(' ')
        for token in tokens:
            if token in self.reverse_map:
                plaintext += self.reverse_map[token]
        return plaintext


class SyllableCypher(Cypher):
    def __init__(self, keyword: str):
        super().__init__()
        self.keyword = self.prepare_text(keyword).upper()
        assert len(self.keyword)%2 == 0
        self.char_map = self._create_char_map()
        self.reverse_map = {v: k for k, v in self.char_map.items()}

    def _create_char_map(self):
        char_map = {}
        for i in range(len(self.keyword) // 2):
            char_map[self.keyword[i * 2]] = self.keyword[i * 2 + 1]
            char_map[self.keyword[i * 2 + 1]] = self.keyword[i * 2]
        
        for i in range(26):
            char = chr(i + 65)
            if char not in self.keyword:
                char_map[char] = char
        return char_map
    
    def encrypt(self, plaintext: str) -> str:
        plaintext = self.prepare_text(plaintext).upper()
        ciphertext = ""
        for char in plaintext:
            ciphertext += self.char_map.get(char, char)
        return ciphertext
    
    def decrypt(self, ciphertext: str) -> str:
        plaintext = ""
        for char in ciphertext:
            plaintext += self.reverse_map.get(char, char)
        return plaintext
