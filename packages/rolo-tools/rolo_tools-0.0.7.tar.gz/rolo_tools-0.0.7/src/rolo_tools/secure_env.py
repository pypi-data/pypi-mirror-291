"""A class for securely storing and retrieving environment variables"""
from cryptography.fernet import Fernet
import os, json

class SecureEnv:
    def __init__(self, key=None):
        #Runs in either encrypted or raw mode
        if key is None:
            if os.environ.get('SECURE_KEY') is not None:
                self.cipher = Fernet(os.environ['SECURE_KEY'])
                self.mode = "encrypted"
            elif os.environ.get('SECURE_ENV') == "raw":
                self.mode = "raw"
            else:
                print("No key provided. Cannot encrypt or decrypt values.")
                print("If you have added your environment variables without encryption, set the 'SECURE_ENV' environment variable to 'raw'.")
                choice = input("Would you like to run raw for this session? (y/n): ")
                if choice.lower() == "y":
                    self.mode = "raw"
                else:
                    self.generate_key()
        else:
            self.cipher = Fernet(key)
            self.mode = "encrypted"

    def decrypt(self, env_variable):
        """Decrypts an environment variable"""
        if self.mode == "encrypted":
            if self.check_secure_keys(env_variable): #checks if the key is present in the file secure_keys.json
                return self.cipher.decrypt(self.get_secure_key(env_variable)).decode()
            elif self.check_env_exists(env_variable): #checks if the environment variable exists
                return self.cipher.decrypt(os.environ[env_variable]).decode()        
            else:
                self.env_is_missing(env_variable)
        else:
            return os.environ[env_variable]
    
    def encrypt(self, value):
        """Encrypts a value using the class's key"""
        if self.mode != "encrypted":
            print("Cannot encrypt value. No key provided. Keys are provided when initializing the SecureEnv class.")
            self.generate_key()
        print("Encrypted value: ", self.cipher.encrypt(value.encode()))
        print("Please store this key in a secure location.")

    def generate_key(self):
        """Generates a key for encrypting and decrypting environment variables"""
        choice = input("Would you like to generate a key now? (y/n): ")
        if choice.lower() == "y":
            key = Fernet.generate_key()
            print("Key generated: "+key.decode())
            print("Please store this key in a secure location.")
            self.cipher = Fernet(key)
            self.mode = "encrypted"
            return True
        else: #if we get here and still dont have a key, we cannot continue
            print("Cannot continue without a key.")
            print("Exiting program.")
            exit()

    def check_env_exists(self, env_name):
        """Checks if an environment variable exists"""
        return env_name in os.environ

    def check_secure_keys(self, env_name):
        """Checks if the key is present in the file secure_keys.json"""
        with open('secure_keys.json', 'r') as f:
            keys = json.load(f)
        if env_name in keys:
            return True
        
    def get_secure_key(self, env_name):
        """Retrieves the key from the file secure_keys.json"""
        with open('secure_keys.json', 'r') as f:
            keys = json.load(f)
        return keys[env_name]

    @staticmethod
    def env_is_missing(env_name):
        """Prints an error message and exits the program if an environment variable is missing"""
        print(f"{env_name} not found in environment variables")
        print("Please add it to the environment variables and try again")
        exit()        