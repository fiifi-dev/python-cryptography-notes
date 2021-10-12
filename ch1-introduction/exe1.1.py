from string import ascii_uppercase


def encrypt(msg: str, shift_len: int) -> str:
    result = ""


    for letter in msg.upper():
        try:
            index = ascii_uppercase.index(letter)
            result += ascii_uppercase[index+shift_len]
        except ValueError:
            result += letter
        except IndexError:
            result += ascii_uppercase[abs((index+shift_len)-26)]

    return result


def dencrypt(msg: str, shift_len: int) -> str:
    result = ""

    for letter in msg.upper():
        try:
            index = ascii_uppercase.index(letter)
            result += ascii_uppercase[index-shift_len]
        except ValueError:
            result += letter

    return result


# # Testing
print(encrypt("Hello World", 10))
print(dencrypt("ROVVY GYBVN", 10))
