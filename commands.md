# Create a key pair

### Create private key:
```
openssl genrsa -des3 -out private.pem 2048
```

### Create public key from private key:
```
openssl rsa -in private.pem -outform PEM -pubout -out public.pem
```

# Encrypt and Decrypt with the key pair

### Encrypt with public key:
```
openssl rsautl -encrypt -inkey public.pem -pubin -in file.txt -out file.ssl
```

### Decrypt with private key:
```
openssl rsautl -decrypt -inkey private.pem -in file.ssl -out decrypted.txt
```
