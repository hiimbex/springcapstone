import hashlib, json, pprint, datetime, merkletools, random
from collections import OrderedDict
from keymaker import *
from employees import Employee

# Transaction class
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
    # sign the data
    string_byte_data = self.format_data()
    signature = self.who.get('key', '').sign_data(string_byte_data)
    return signature, string_byte_data

  def verify(self, sig):
    # verify the data
    string_byte_data = self.format_data()
    return self.who.get('key', '').verify_data(string_byte_data, sig)

# combine the signature with the data from the transaction
def sign_transaction(data, signature):
    return data + signature

# verify signature
def verify_sig(mt, index, employee, transaction):
  if (mt.validate_proof(mt.get_proof(index),
      mt.get_leaf(index), mt.get_merkle_root())):
    print('valid merkle tree')
    if (transaction[0].hex() == mt.get_leaf(index) and
        employee.get_key().verify_data(transaction[1], transaction[2])):
      print('valid signature')
      return True
    else:
      print('invalid signature')
      return False
  else:
    print('invalid merkle tree')
    return False

if __name__ == "__main__":
  # instantiate merkle tree
  mt = merkletools.MerkleTools()
  # generate company's master key
  company = MasterKey()
  # generate several employees to use for testing
  employeeA = Employee()
  employeeB = Employee()
  employeeC = Employee()
  employeeD = Employee()
  employeeE = Employee()
  employeeF = Employee()
  employeeG = Employee()
  employeeH = Employee()
  employeeI = Employee()
  employeeJ = Employee()
  employees = [ employeeA, employeeB, employeeC, employeeD, employeeE,
                employeeF, employeeG, employeeH, employeeI, employeeJ ]
  # generate several 'database entries' to use for testing
  db_entries = [ 'insert on customer database', 'insert on shipping database',
                 'delete on customer database', 'delete on shipping database',
                 'delete on product database', 'insert on product database',
                 'delete on management database', 'insert on management database',
                 'delete on payment database', 'insert on payment database' ]

  # create some random transactions
  for i in range(10):
    # randomly choose an employee
    employee = random.choice(employees)
    # generate transaction (randomly chooses db entry)
    transaction = Transaction({ 'id': employee.get_id(), 'key': employee.get_key() },
                               random.choice(db_entries), datetime.datetime.now())
    # create signature
    signature, data = transaction.sign()
    # add signature to transaction
    signed_transaction = sign_transaction(data, signature)
    # store combined signature and transaction to merkle tree
    mt.add_leaf(signed_transaction.hex()) # library requires hex data

    # randomly save the fifth signature to be verified
    if i == 5:
      sample_index = 5
      sample_employee = employee
      sample_transaction = [ signed_transaction, data, signature ]

  # generate merkle tree
  mt.make_tree()
  # get tree size
  leaves = mt.get_leaf_count()
  # get tree root
  root = mt.get_merkle_root()
  # sign root with company key
  root_signature = company.sign_data(json.dumps(root, default=str).encode())
  # aggregate tree data
  signed_root = { 'root_hash': root, 'tree_head_signature': root_signature,
                 'timestamp': datetime.datetime.now(), 'tree_size': leaves }
  pp = pprint.PrettyPrinter(indent=2)
  print('\n Tree Root Info: \n')
  pp.pprint(signed_root)
  print('\n')

  # verify randomly chosen signature
  verifyTrueSample = verify_sig(mt, sample_index, sample_employee, sample_transaction)
  print('Verify True Sample: ', verifyTrueSample, '\n')

  # use the same data to verify a different index to demonstrate failure
  verifyFalseSample = verify_sig(mt, sample_index + 1, sample_employee, sample_transaction)
  print('Verify False Sample: ', verifyFalseSample)
