import argparse
import hashlib
import zlib

print("Welcome to Hash Calculator CLI Edition")
print("Version: 1.1")

class HashCalculatorCLI:
    def __init__(self, file_path):
        self.file_path = file_path
        self.results = {}

    def calculate_hash(self):
        if self.file_path:
            try:
                with open(self.file_path, 'rb') as file:
                    content = file.read()
                    for algorithm in ['MD5', 'SHA1', 'SHA256', 'SHA512', 'CRC32']:
                        if algorithm == 'MD5':
                            hash_value = hashlib.md5(content).hexdigest()
                        elif algorithm == 'SHA1':
                            hash_value = hashlib.sha1(content).hexdigest()
                        elif algorithm == 'SHA256':
                            hash_value = hashlib.sha256(content).hexdigest()
                        elif algorithm == 'SHA512':
                            hash_value = hashlib.sha512(content).hexdigest()
                        elif algorithm == 'CRC32':
                            hash_value = format(zlib.crc32(content) & 0xFFFFFFFF, '08x')

                        self.results[algorithm] = hash_value

            except Exception as e:
                print(str(e))

    def display_results(self):
        print("Hash Values:")
        for algorithm, value in self.results.items():
            print(f"{algorithm}: {value}")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='CLI Hash Calculator')
    parser.add_argument('file_path', nargs='?', default=None, type=str, help='Path to the file to calculate hash values')
    args = parser.parse_args()

    if args.file_path is None:
        file_path = input("Enter the path to the file: ")
    else:
        file_path = args.file_path

    hash_calculator = HashCalculatorCLI(file_path)
    hash_calculator.calculate_hash()
    hash_calculator.display_results()
