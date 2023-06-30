import hashlib
import json
import os
import mmap
from base64 import b64decode
from datetime import datetime

from Cryptodome.Cipher import AES
from Cryptodome.Util.Padding import unpad


class DecryptionTool:
    def __init__(self, user_file, user_key, video_list, expires_at, display_at, second_screen):
        self.user_file = user_file

        self.input_file_size = os.path.getsize(self.user_file)
        self.chunk_size = 1024 * 1024 * 500
        self.total_chunks = self.input_file_size // self.chunk_size + 1

        # convert the key and salt to bytes
        self.user_key = bytes(user_key, "utf-8")
        self.user_salt = bytes(user_key[::-1], "utf-8")
        self.video_list = video_list
        self.expires_at = expires_at
        self.display_at = display_at
        self.second_screen = second_screen
        self.error_list = list()

        # get the file extension
        self.file_extension = self.user_file.split(".")[-1]

        self.hash_type = "SHA256"

        # dictionary to store hashed key and salt

        self.hashed_key_salt = dict()
        # hash key and salt into 16 bit hashes

        self.hash_key_salt()

    @staticmethod
    def read_in_chunks(file_object, chunk_size):
        """Lazy function (generator) to read a file piece by piece.
        Default chunk size: 1k.
        """

        while True:
            data = file_object.read(chunk_size)
            if not data:
                break
            yield data

    def decrypt(self):
        # change error list to set
        self.error_list = list(set(self.error_list))

        # check display at validation
        if not self.second_screen:
            if self.display_at:
                self.error_list.append(414)
                return None

        # check if key has expired validation
        if self.expires_at < datetime.now().strftime("%Y-%m-%d"):
            if 413 in self.error_list:
                self.error_list.remove(413)
            self.error_list.append(410)
            return None

        #  exact same as above function except in reverse
        content = b''
        with open(self.user_file, 'rb') as input_file:
            with mmap.mmap(input_file.fileno(), 0, access=mmap.ACCESS_READ) as mm:
                content = mm.read()
                # for piece in self.read_in_chunks(mm, self.chunk_size):
                #     content += piece

        try:
            parsed_data = json.loads(content.decode('utf-8'))
            json_k = ['iv', 'ciphertext', 'extra']
            jv = {k: b64decode(parsed_data[k]) for k in json_k}
            del parsed_data

            if isinstance(self.video_list, list):
                if jv['extra'].decode() not in self.video_list:
                    # check if 410, 413 is in error list
                    if 410 in self.error_list:
                        self.error_list.remove(410)
                    if 413 in self.error_list:
                        self.error_list.remove(413)
                    self.error_list.append(411)
                    return None

            cipher = AES.new(
                self.hashed_key_salt["key"], AES.MODE_OFB, iv=jv['iv']
            )
            ciphertext = jv['ciphertext']
            del jv

            # split ciphertext to chunks
            offset = 0
            done_chunks = 0
            while offset < len(ciphertext):
                yield cipher.decrypt(ciphertext[offset:offset+self.chunk_size])
                offset += self.chunk_size
                done_chunks += 1

            # clean up the cipher object
            del cipher
            del ciphertext
            del content
        except (ValueError, KeyError):
            yield None
            if 410 not in self.error_list:
                self.error_list.append(413)

    def hash_key_salt(self):

        # --- convert key to hash
        #  create a new hash object

        hasher = hashlib.new(self.hash_type)
        hasher.update(self.user_key)

        # turn the output key hash into 32 bytes (256 bits)

        self.hashed_key_salt["key"] = bytes(hasher.hexdigest()[:32], "utf-8")

        # clean up hash object

        del hasher

        # --- convert salt to hash
        #  create a new hash object

        hasher = hashlib.new(self.hash_type)
        hasher.update(self.user_salt)

        # turn the output salt hash into 16 bytes (128 bits)

        self.hashed_key_salt["salt"] = bytes(hasher.hexdigest()[:16], "utf-8")

        # clean up hash object

        del hasher