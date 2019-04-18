import hashlib, json
from collections import OrderedDict
from keymaker import *
import datetime
import merkletools

class Transaction:
  def __init__(self, who, what, when):
    self.who = who
    self.what = what
    self.when = when

  def format_data(self):
    # data must be byte string
    data = {'Timestamp': self.when, 'Data': self.what}
    string_byte_data = json.dumps(data, default=str).encode()
    return string_byte_data

  def sign(self):
    string_byte_data = self.format_data()
    # sign the data
    signature = self.who.get('key', '').sign_data(string_byte_data)
    return signature, string_byte_data

  def verify(self, sig):
    string_byte_data = self.format_data()
    return self.who.get('key', '').verify_data(string_byte_data, sig)

def sign_transaction(data, signature):
    return data + signature

if __name__ == "__main__":
  # sign root of merkle tree with company key
  # print out root hash, tree head signature, timestamp, tree size

  # make an employee's key (at some point need to check if company or employee and get relvant signature ??)

  employeeA = {'id': '1234', 'key': MasterKey()}
  transaction = Transaction(employeeA, 'insert on customer database', datetime.datetime.now())
  signature, data = transaction.sign()
  # combine them
  signed_transaction = sign_transaction(data, signature)

  employeeB = {'id': '1234', 'key': MasterKey()}
  diff_transaction = Transaction(employeeB, 'insert on shipping database', datetime.datetime.now())
  diff_signature, diff_data = diff_transaction.sign()
  # combine them
  diff_signed_transaction = sign_transaction(diff_data, diff_signature)

  mt = merkletools.MerkleTools()
  mt.add_leaf(signed_transaction.hex())
  mt.add_leaf(diff_signed_transaction.hex())
  mt.make_tree()
  root = mt.get_merkle_root()

  print(mt.validate_proof(mt.get_proof(0), mt.get_leaf(0), root))
  hashed_value = mt.get_leaf(0)
  print(employeeA.get('key', '').verify_data(transaction.format_data(), signature))

  # verify Signature
  def verify_sig(mt, index, employee, signed_transaction):
    if (mt.validate_proof(mt.get_proof(index), mt.get_leaf(index), mt.get_merkle_root())):
      print('valid merkle tree')
      if (signed_transaction.hex() == mt.get_leaf(index)):
        print('valid signature')
        return True
    return False

  verifyA = verify_sig(mt, 0, employeeA, signed_transaction)
  verifyB = verify_sig(mt, 1, employeeB, diff_signed_transaction)
  print(verifyA, verifyB)
