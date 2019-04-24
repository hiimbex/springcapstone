#Test and tutorial
from . keymaker import *
if __name__ == '__main__':

    print("Make a master key")
    input("\nPress <Return> to continue\n")
    print("Wait a sec...",flush=True)
    key = MasterKey()
    print("Your private key PEM encoded:")
    fmtted = key.dump_private().decode('ascii')
    fmtted = fmtted.split('\n')
    fmtted = fmtted[:3]+['...']+fmtted[-4:]
    print('\n'.join(fmtted))
    input("\nPress <Return> to continue\n")
    print("Your public key PEM encoded:")
    print(key.dump_public().decode('ascii'))
    input("\nPress <Return> to continue\n")
    print("Sign the message \"I solemnly swear...\"")
    input("\nPress <Return> to continue\n")
    msg = b"I solemnly swear..."
    sig = key.sign_data(msg)
    print("Signature of message in hexadecimal: ")
    print(sig.hex())
    input("\nPress <Return> to continue\n")
    print("Now let's verify: ")
    print("Call: key.verify_data(msg,sig)")
    input("\nPress <Return> to continue\n")
    if key.verify_data(msg,sig) is True:
        print("Signature verified!")
    input("\nPress <Return> to continue\n")
    print("Now let's alter the message: ")
    input("\nPress <Return> to continue\n")
    fakemsg = b"\"I solemnly sweat...\""
    print("Fake message: "+fakemsg.decode("ascii"))
    print("Try to verify with key.verify_data(fakemsg,sig)")
    input("\nPress <Return> to continue\n")
    key.verify_data(fakemsg,sig)
