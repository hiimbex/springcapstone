import  cryptography.hazmat.primitives.asymmetric.rsa as rsa
import cryptography.hazmat.primitives.serialization as serial
import cryptography.hazmat.primitives.asymmetric.padding as padding
from cryptography.hazmat.primitives.hashes import SHA256
from cryptography.hazmat.backends import default_backend
from cryptography.exceptions import InvalidSignature

# Accesses your computer's backend for doing cryptological calculations
def_be = default_backend()
mgf_salt_length = 16

class MasterKey:
    """ Key for manager to sign root. ***Keep it safe!*** """

    def __init__(self):
        # We'll the moduls 4096 bits for security; the standard public
        # exponent is 65537, so we'll use that
        self.privkey = rsa.generate_private_key(65537,4096,def_be)
        self.pubkey = self.privkey.public_key()
        # ... Feel free to add extra attributes

    def dump_private(self):
        """ This dumps the key contents to a PEM encoding string,
        which can be used for hard storage. Note that this
        file is unencrypted, so be careful!"""

        # N.B. This is a byte string. To convert to a string, just do 
        # something like key_pem.decode('ascii').  This will always
        # work since PEM encodings only contain ascii characters

        return self.privkey.private_bytes(serial.Encoding.PEM,
                serial.PrivateFormat.PKCS8,serial.NoEncryption())
        
    def dump_public(self):
        """ Like dump_private, but the public part.  This, of course,
        should be publicly available. """

        return self.pubkey.public_bytes(serial.Encoding.PEM,
                serial.PublicFormat.PKCS1) 

    def sign_data(self,data):
        """ This signs the data with the private key.  We the
        RSASSA-PSS signature scheme (see rfc 3347) since it is recommended
        by the pros. N.B. that `data' must a byte string. 
        
        We will use the SHA256 hashing algorithm, and use a salt
        length of 16"""

        return self.privkey.sign(data,
                padding.PSS(padding.MGF1(SHA256()),mgf_salt_length),
                SHA256())

    def verify_data(self,data,signature):
        try:
            self.pubkey.verify(signature,data,
                    padding.PSS(padding.MGF1(SHA256()),mgf_salt_length),
                    SHA256())
        except InvalidSignature:
            # Bex and Rose decide how to handle an invalid signature
            print("Sorry, bad signature")
        else:
            # Signature was valid
            return True
