import base64



class Cipher():
    def __init__(self, message):
        self.text_to_encrypt = message
        self.encrypted_text = ""
        

class CaesarCipher(Cipher):
    def __init__(self, key, message):
        super().__init__(message)
        try:
            self.shift = int(key)
        except:
            self.shift = 0

    
    def encryption(self, x):
        for sign in self.text_to_encrypt:
            sign_num = ord(sign)
            print("unencrypted", sign_num)
            if sign_num <= 90 and sign_num >= 65:
                sign_num = (sign_num + (self.shift*x)%26) % 91
                if sign_num < 65:
                    sign_num += 65
            elif sign_num <= 122 and sign_num >= 97:
                sign_num = (sign_num + (self.shift*x)%26) % 123
                if sign_num < 97:
                    sign_num = (sign_num + 97) % 123
            print("encrypted", sign_num)
            self.encrypted_text += chr(sign_num)
        
        return str(self.encrypted_text)
    
    def encrypt(self):
        self.encrypted_text = ""
        return self.encryption(1)
    
    def decrypt(self):
        self.encrypted_text = ""
        return self.encryption(-1)


class PlayfairCipher(Cipher):
    def __init__(self, key, message):
        super().__init__(message)
        try:
            self.keyword = key
        except:
            self.keyword = ""
        self.matrix = self.create_matrix()
        self.print_matrix()
        self.diagrams = self.create_diagrams()

    def print_matrix(self):
        print(f"+-----+-----+-----+-----+-----+")
        print(f"|     |     |     |     |     |")
        print(f"|  {self.matrix[0][0]}  |  {self.matrix[0][1]}  |  {self.matrix[0][2]}  |  {self.matrix[0][3]}  |  {self.matrix[0][4]}  |")
        print(f"|     |     |     |     |     |")
        print(f"+-----+-----+-----+-----+-----+")
        print(f"|     |     |     |     |     |")
        print(f"|  {self.matrix[1][0]}  |  {self.matrix[1][1]}  |  {self.matrix[1][2]}  |  {self.matrix[1][3]}  |  {self.matrix[1][4]}  |")
        print(f"|     |     |     |     |     |")
        print(f"+-----+-----+-----+-----+-----+")
        print(f"|     |     |     |     |     |")
        print(f"|  {self.matrix[2][0]}  |  {self.matrix[2][1]}  |  {self.matrix[2][2]}  |  {self.matrix[2][3]}  |  {self.matrix[2][4]}  |")
        print(f"|     |     |     |     |     |")
        print(f"+-----+-----+-----+-----+-----+")
        print(f"|     |     |     |     |     |")
        print(f"|  {self.matrix[3][0]}  |  {self.matrix[3][1]}  |  {self.matrix[3][2]}  |  {self.matrix[3][3]}  |  {self.matrix[3][4]}  |")
        print(f"|     |     |     |     |     |")
        print(f"+-----+-----+-----+-----+-----+")
        print(f"|     |     |     |     |     |")
        print(f"|  {self.matrix[4][0]}  |  {self.matrix[4][1]}  |  {self.matrix[4][2]}  |  {self.matrix[4][3]}  |  {self.matrix[4][4]}  |")
        print(f"|     |     |     |     |     |")
        print(f"+-----+-----+-----+-----+-----+")

    def create_matrix(self):
        matrix = [chr(i) for i in range(65, 91) if i not in (73, 74)]
        matrix.insert(8, "I/J")
        # remove duplicated letters
        key_word = ""
        for letter in self.keyword:
            if letter not in key_word and letter.isalpha():
                key_word += letter
        # create matrix
        key_word = key_word[::-1]
        for letter in key_word.upper():
            if letter in "IJ":
                matrix.remove("I/J")
                matrix.insert(0, "I/J")
            else:
                matrix.remove(letter)
                matrix.insert(0, letter)
        new_matrix = [matrix[i:i+5] for i in range(0,21,5)]
        return new_matrix
    
    def create_diagrams(self):
        diagrams = []
        message = [letter for letter in self.text_to_encrypt.upper() if letter.isalpha()]
        # for i in range(0, len(message), 2):
        #     try:
        #         if message[i] == message[i+1]:
        #             message.insert(i+1, "X")
        #     except:
        #         message.append("X")
        if len(message) % 2 != 0:
            message.append("X")
        self.text_to_encrypt = "".join(message)

        diagrams = [[char for char in self.text_to_encrypt[i:i+2]] for i in range(0, len(self.text_to_encrypt), 2)]
        return diagrams


    def encryption(self, x):
        encrypted_diagrams = []
        for diagram in self.diagrams:
            letter_indexes = []
            bi = ""
            for letter in diagram:
                for i, row in enumerate(self.matrix):
                    for j, val in enumerate(row):
                        if letter in val:
                            letter_indexes.append((i, j))
            # same row
            if letter_indexes[0][0] == letter_indexes[1][0]:
                bi += self.matrix[letter_indexes[0][0]][(letter_indexes[0][1]+x)%5]
                bi += self.matrix[letter_indexes[1][0]][(letter_indexes[1][1]+x)%5]
            # same column
            elif letter_indexes[0][1] == letter_indexes[1][1]:
                bi += self.matrix[(letter_indexes[0][0]+x)%5][letter_indexes[0][1]]
                bi += self.matrix[(letter_indexes[1][0]+x)%5][letter_indexes[0][1]]
            # different column and row
            else:
                bi += self.matrix[letter_indexes[0][0]][letter_indexes[1][1]]
                bi += self.matrix[letter_indexes[1][0]][letter_indexes[0][1]]
            
            encrypted_diagrams.append(bi)
            
        self.encrypted_text = " ".join(encrypted_diagrams)
        return str(self.encrypted_text)
    
    def encrypt(self):
        return self.encryption(1)
    
    def decrypt(self):
        return self.encryption(-1)


class Base64(Cipher):
    def __init__(self, message):
        super().__init__(message)


    def encode(self):
        encoded = base64.b64encode(self.text_to_encrypt.encode()).decode('utf-8')
        self.encrypted_text = encoded
        return encoded

    
    def decode(self):
        text = self.text_to_encrypt

        if text.startswith("b'") and text.endswith("'"):
            text = text[2:-1]

        decoded_bytes = base64.b64decode(text)
        decoded_str = decoded_bytes.decode('utf-8')
        self.encrypted_text = decoded_str
        return decoded_str






# cipher = CaesarCipher(1, "abcxyz")
# print(cipher.encrypt())
# print()
# print(cipher.decrypt())

# cipher = PlayfairCipher("sdasdasd","sadasdas")
# cipher.print_matrix()
# print(cipher.matrix)
# print(cipher.diagrams)
# print(cipher.decrypt())