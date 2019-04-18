import hashlib, json
from collections import OrderedDict
from keymaker import *
import datetime
import merkletools
from employees import Employee

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

  employeeA = Employee()
  transaction = Transaction({'id': employeeA.get_id(), 'key': employeeA.get_key()},
                             'insert on customer database', datetime.datetime.now())
  signature, data = transaction.sign()
  signed_transaction = sign_transaction(data, signature)

  employeeB = Employee()
  diff_transaction = Transaction({'id': employeeB.get_id(), 'key': employeeB.get_key()},
                                   'insert on shipping database', datetime.datetime.now())
  diff_signature, diff_data = diff_transaction.sign()
  diff_signed_transaction = sign_transaction(diff_data, diff_signature)

  mt = merkletools.MerkleTools()
  mt.add_leaf(signed_transaction.hex())
  mt.add_leaf(diff_signed_transaction.hex())
  mt.make_tree()
  root = mt.get_merkle_root()

  # verify signature
  def verify_sig(mt, index, employee, transaction):
    if (mt.validate_proof(mt.get_proof(index),
        mt.get_leaf(index), mt.get_merkle_root())):
      print('valid merkle tree')
      if (transaction[0].hex() == mt.get_leaf(index) and
          employee.get_key().verify_data(transaction[1], transaction[2])):
        print('valid signature')
        return True
    return False

  verifyA = verify_sig(mt, 0, employeeA, [signed_transaction, data, signature])
  verifyB = verify_sig(mt, 1, employeeB, [diff_signed_transaction, diff_data, diff_signature])
  print(verifyA, verifyB)
