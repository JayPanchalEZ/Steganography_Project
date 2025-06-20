import cv2 as cv
from Cryptodome.Cipher import AES
from Cryptodome.Util.Padding import pad, unpad
from Cryptodome.Random import get_random_bytes
import hashlib

def derive_key(userkey):
    return hashlib.sha256(userkey.encode()).digest()[:16]  # Use SHA-256 to derive a 16-byte key

def encrypt_messg(message, userkey):
    key = derive_key(userkey)
    cipher = AES.new(key, AES.MODE_CBC)
    ct = cipher.encrypt(pad(message.encode(), AES.block_size))
    return cipher.iv + ct

def decrypt_messg(cipher_bytes, userkey):
    key = derive_key(userkey)
    iv = cipher_bytes[:16]
    ct = cipher_bytes[16:]
    cipher = AES.new(key, AES.MODE_CBC, iv)
    return unpad(cipher.decrypt(ct), AES.block_size).decode()

def embed_data(image, encrypted_bytes):
    # Prepend message length (in bytes) as 4 bytes
    length_bytes = len(encrypted_bytes).to_bytes(4, 'big')
    data = length_bytes + encrypted_bytes

    n, m, z = 0, 0, 0
    for byte in data:
        for bit_pos in range(8):
            bit = (byte >> (7 - bit_pos)) & 1
            image[n, m, z] = (image[n, m, z] & 0xFE) | bit
            z = (z + 1) % 3
            if z == 0:
                m += 1
                if m == image.shape[1]:
                    m = 0
                    n += 1
    return image

def extract_data(image):
    n = m = z = 0
    # First, extract the length (first 4 bytes)
    length_bytes = bytearray()
    for _ in range(4):
        byte = 0
        for bit_index in range(8):
            bit = image[n, m, z] & 1
            byte = (byte << 1) | bit
            z = (z + 1) % 3
            if z == 0:
                m += 1
                if m == image.shape[1]:
                    m = 0
                    n += 1
        length_bytes.append(byte)
    data_length = int.from_bytes(length_bytes, 'big')

    # Now extract the encrypted data of that length
    data = bytearray()
    for _ in range(data_length):
        byte = 0
        for bit_index in range(8):
            bit = image[n, m, z] & 1
            byte = (byte << 1) | bit
            z = (z + 1) % 3
            if z == 0:
                m += 1
                if m == image.shape[1]:
                    m = 0
                    n += 1
        data.append(byte)
    return bytes(data)