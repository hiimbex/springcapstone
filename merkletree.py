import hashlib, json
from collections import OrderedDict

class Merkle_Tree:
  def __init__(self):
    self.transaction_list = None
    self.past_transaction = OrderedDict()

  def set_transaction_list(self, transaction_list):
      self.transaction_list = transaction_list
      return transaction_list

  def generate_tree(self):
    transaction_list = self.transaction_list
    past_transaction = self.past_transaction
    temp_transaction = []

    # loop by 2s to get the left element
    for i in range(0, len(transaction_list), 2):
      # get left child
      element = transaction_list[i]
      # if more elements remain, go to next element
      if i + 1 < len(transaction_list):
        element_right = transaction_list[i + 1]
      # if no elements remain we reached the end
      else:
        element_right = ''
      # hash
      element_hash = hashlib.sha256(element)
      # add transaction of element addition
      past_transaction[transaction_list[i]] = element_hash.hexdigest()
      # if not at end hash right element, add transaction and temp_transaction
      if element_right != '':
        element_right_hash = hashlib.sha256(element_right)
        past_transaction[transaction_list[i + 1]] = element_right_hash.hexdigest()
        temp_transaction.append(element_hash.hexdigest() + element_right_hash.hexdigest())
      # if at end add current element temp_transaction
      else:
        temp_transaction.append(element_hash.hexdigest())
    # while not gone through every transaction, add transactions
    if len(transaction_list) != 1:
      self.transaction_list = temp_transaction
      self.past_transaction = past_transaction
      self.generate_tree()

  def get_past_transaction(self):
    return self.past_transaction

  def get_root(self):
    last_key = self.past_transaction.keys()[-1]
    return self.past_transaction[last_key]

if __name__ == "__main__":
  tree = Merkle_Tree()
  tree.set_transaction_list(['hi','hello','hey','sup'])
  tree.generate_tree()

  tampered_tree = Merkle_Tree()
  tampered_tree.set_transaction_list(['hi','hello','hey','goodbye'])
  tampered_tree.generate_tree()

  print 'Non-tampered tree past transactions: ', tree.get_past_transaction(), '\n'
  print 'Tampered tree past transactions: ', tampered_tree.get_past_transaction(), '\n'
  print 'Final root of the valid tree : ', tree.get_root(), '\n'
  print 'Final root of the tampered tree : ', tampered_tree.get_root(), '\n'


  transactionz = { 'my message': 'author sig?', 'hello world!': '123abc'}

  # 'hello world!\n123abc'
