from ..abstract_async_requests import callSolcatcherRpc
from .address_lookup import get_sorted_addresses
from abstract_utilities import eatAll,make_list,get_any_value
from abstract_bots.bot_functions import divide_it,return_0,exponential
from abstract_bots.txn_functions import get_any_value,get_account_keys
import pandas as pd
def search_for_account_index(data,index_number):
    for index_data in data:
        if str(index_data.get('accountIndex')) == str(index_number):
            return index_data
          

def get_account_keys(txnData):
    return txnData['transaction']['message']['accountKeys']

def get_loaded_addresses(txnData):
    return txnData['meta']['loadedAddresses']

def get_read_only_addresses(txnData):
    return get_loaded_addresses(txnData).get('readonly', [])

def get_writable_addresses(txnData):
    return get_loaded_addresses(txnData).get('writable', [])

def get_all_account_keys(txnData):
  accountKeys = get_read_only_addresses(txnData)
  accountKeys += get_writable_addresses(txnData)
  accountKeys += get_account_keys(txnData) 

  return accountKeys

class saveAcountKeys:

  def __init__(self,txnData):
    self.txnData = txnData
    self.accountKeys = get_account_keys(txnData)
    self.loaded_addresses = get_loaded_addresses(txnData)
    self.read_only_addresses = get_read_only_addresses(txnData)
    self.writable_addresses = get_writable_addresses(txnData)
    self.accountKeys = self.get_all_addresses()
    
  def get_all_addresses(self,txnData=None):
    txnData = txnData or self.txnData
    return get_sorted_addresses(txnData)
    
  def sort_account_keys(self, accountKeys):
    return sorted(accountKeys, key=lambda x: x['pubkey'].to_base58())    


  def get_account_from_index(self,index):
    account = None
    if len(self.accountKeys)>index:
      account = self.accountKeys[index]
    return account

  def get_account_keys_from_instruction(self,instruction):
    indexes = instruction.get('accounts')
    accounts = []
    for index in indexes:
      accounts.append(self.get_account_from_index(index))
    return accounts
  def add_accounts_to_instruction(self,instruction):
    accounts = self.get_account_keys_from_instruction(instruction)
    instruction['extractedAccounts'] = accounts
    return instruction
  def add_accounts_to_instructions(self,instructions):
    for i,instruction in enumerate(instructions):
      instruction = self.add_accounts_to_instruction(instruction)
      instructions[i] = instruction
    return instructions

  
  def get_programIdIndex_from_instruction(self,instruction):
    index = instruction.get('programIdIndex')
    programId = self.get_account_from_index(index)
    return programId
  def add_programId_to_instruction(self,instruction):
    programId = self.get_programIdIndex_from_instruction(instruction)
    instruction['programId'] = programId
    return instruction
  def add_programIds_to_instructions(self,instructions):
    for i,instruction in enumerate(instructions):
      instruction = self.add_programId_to_instruction(instruction)
      instructions[i] = instruction
    return instructions

def get_log_messages(txnData):
    return txnData['meta']['logMessages']

class logMessageManager:
      def __init__(self,txnData):
        self.logMessages = get_log_messages(txnData)
        self.logClusters = self.get_log_index_clusters()
      def get_log_index_clusters(self):
        clusters =[]
        clusterCount=-1
        for j,log in enumerate(self.logMessages):
            curr_logs = {}
            
            # Split the log into parts based on whitespace
            parts = [part.replace(':','') for part in log.split()]
            
            if not parts:
                continue  # Skip empty lines
            # Parse based on the structure
            if "invoke" in parts:
                
                clusterCount+=1
                clusters.append({"logs":[],"clusterIndex":clusterCount,"programId":parts[1],"stackHeight":str(parts[-1])[1:-1],"start":j,"end":j,"types":[]})
                
                curr_logs['cmdType'] = parts[0]
                curr_logs['programId'] = parts[1]
                curr_logs['event'] = parts[2]  # 'invoke' or 'success'
                curr_logs['vars'] = parts[3] if len(parts) > 3 else None
            
            elif "consumed" in parts:
                curr_logs['cmdType'] = parts[0]
                curr_logs['programId'] = parts[1]
                curr_logs['event'] = 'consumed'
                consumed_index = parts.index('consumed')
                curr_logs['vars'] = " ".join(parts[consumed_index + 1:])
            
            elif "return:" in log:
                curr_logs['cmdType'] = parts[0]
                curr_logs['programId'] = parts[1]
                curr_logs['event'] = 'return'
                curr_logs['vars'] = " ".join(parts[2:])
            
            elif "log:" in log:
                curr_logs['cmdType'] = parts[0]
                curr_logs['programId'] = parts[1]
                log_index = parts.index('log')
                curr_logs['event'] = parts[log_index + 1]
                curr_logs['type'] = parts[log_index + 2] if len(parts) > log_index + 2 else None
                clusters[-1]['types'].append(curr_logs['type'])
                if clusters[-1].get('type') == None:
                  clusters[-1]['type']=curr_logs['type']
                curr_logs['vars'] = " ".join(parts[log_index + 3:]) if len(parts) > log_index + 3 else None
            
            else:
                curr_logs['cmdType'] = parts[0]
                curr_logs['programId'] = parts[1]
                curr_logs['event'] = parts[2] if len(parts) > 2 else None
                curr_logs['vars'] = " ".join(parts[3:]) if len(parts) > 3 else None
            clusters[-1]['end']=j
            # Store parsed log in the list
            clusters[-1]["logs"].append(curr_logs)
        return clusters      
      def get_cluster_type_from_index(self,index):
        cluster = {}
        if len(self.logClusters) >index:
          cluster = self.logClusters[index]
        clusterType = make_list(cluster.get("type") or cluster.get('types'))
        if clusterType:
          clusterType = clusterType[0]
        return clusterType
      def add_cluster_type_to_instruction(self,index,instruction):
        clusterType = self.get_cluster_type_from_index(index)
        instruction['type']=clusterType
        return instruction
      
      def add_cluster_types_to_instructions(self,instructions,indexStart=0):
        new_instructions = []
        for i,instruction in enumerate(instructions):
          index = i+indexStart
          instruction = self.add_cluster_type_to_instruction(index,instruction)
          new_instructions.append(instruction)
        return new_instructions
  
def get_instructions(txnData):
  return txnData['transaction']['message']['instructions']

def get_inner_instructions(txnData):
  return txnData['meta']['innerInstructions'][0]['instructions']

def update_instructions(txnData,instructions):
  txnData['transaction']['message']['instructions'] = instructions
  return  txnData
def update_inner_instructions(txnData,inner_instructions):
  txnData['meta']['innerInstructions'][0]['instructions'] = inner_instructions
  return txnData

class saveInstructions:
  def __init__(self,txnData,account_mgr=None,log_mgr=None):
    self.account_mgr = account_mgr or saveAcountKeys(txnData)
    self.log_mgr = log_mgr or logMessageManager(txnData)
    self.instructions = get_instructions(txnData)
    self.inner_instructions = get_inner_instructions(txnData)
    self.allInstructions = self.make_all_associations()
    
  def associate_accounts_with_instructions(self):
    self.instructions = self.account_mgr.add_accounts_to_instructions(self.instructions)
    return self.instructions

  def associate_accounts_with_inner_instructions(self):
    self.inner_instructions = self.account_mgr.add_accounts_to_instructions(self.inner_instructions)
    return self.inner_instructions

  def associate_programIdIndexs_with_instructions(self):
    self.instructions = self.account_mgr.add_programIds_to_instructions(self.instructions)
    return self.inner_instructions

  def associate_programIdIndexs_with_inner_instructions(self):
    self.inner_instructions = self.account_mgr.add_programIds_to_instructions(self.inner_instructions)
    return self.inner_instructions

  def associate_types_with_instructions(self):
    self.instructions = self.log_mgr.add_cluster_types_to_instructions(self.instructions)
    return self.instructions

  def associate_types_with_inner_instructions(self):
    index_start = len(self.instructions)
    self.inner_instructions = self.log_mgr.add_cluster_types_to_instructions(self.inner_instructions,indexStart=index_start)
    return self.inner_instructions

  def associate_all_instructions(self):
    self.instructions = self.associate_types_with_instructions()
    self.instructions = self.associate_accounts_with_instructions()
    self.instructions = self.associate_programIdIndexs_with_instructions()
    return self.instructions
  
  def associate_all_inner_instructions(self):
    self.inner_instructions = self.associate_types_with_inner_instructions()
    self.inner_instructions = self.associate_accounts_with_inner_instructions()
    self.inner_instructions = self.associate_programIdIndexs_with_inner_instructions()
    return self.inner_instructions

  def get_all_instructions(self):
    self.allInstructions = self.instructions
    self.allInstructions += self.inner_instructions
    return self.allInstructions

  def make_all_associations(self):
    self.instructions = self.associate_all_instructions()
    self.inner_instructions = self.associate_all_inner_instructions()
    return self.get_all_instructions()


class TransactionProcessor:
    def __init__(self, txnData=None,signature=None,instruction_mgr = None,account_mgr=None,log_mgr=None,**kwargs):
        txnData = txnData or self.getTransacion(signature,**kwargs)
        self.txnData = txnData
        self.log_mgr = log_mgr or logMessageManager(txnData)
        self.account_mgr = account_mgr or saveAcountKeys(txnData)
        self.instruction_mgr = instruction_mgr or saveInstructions(self.txnData,log_mgr=self.log_mgr,account_mgr=self.account_mgr)
    def get_instructions(self):
      return self.instruction_mgr.allInstructions

    def get_log_clusters(self):
      return self.log_mgr.logClusters

    def get_account_keys(self):
      return self.account_mgr.accountKeys

    def get_txn_data(self):
      self.txnData['transaction']['message']['instructions'] = self.instruction_mgr.instructions
      self.txnData['meta']['innerInstructions'][0]['instructions'] = self.instruction_mgr.inner_instructions
      return self.txnData
    
    def getTransacion(self,signature,**kwargs):
      kwargs['signature']=signature
      return callSolcatcherRpc('getTransaction',**kwargs)


class txnManager:
    def __init__(self, txnData=None, signature=None, txn_mgr=None, acct_mgr=None):
        self.signature = signature
        self.txn_mgr = txn_mgr or get_txnMgr(txnData=txnData, signature=self.signature)
        self.acct_mgr = acct_mgr or self.txn_mgr.account_mgr
        self.txnData = self.txn_mgr.txnData or get_transaction(self.signature)
        self.preBalances = self.txnData['meta']['preBalances']
        self.postBalances = self.txnData['meta']['postBalances']
        self.preTokenBalances = self.txnData['meta']['preTokenBalances']
        self.postTokenBalances = self.txnData['meta']['postTokenBalances']
        self.all_txns = {"Address":[],"Owner":[],'Balance Before':[],"Balance After":[],"Change":[],"Token":[]}
        self.accountKeys = self.acct_mgr.accountKeys
        self.all_txns = {"Address": [], "Owner": [], 'Balance Before': [], "Balance After": [], "Change": [], "Token": []}
        
        # Create a dictionary for quick lookups by accountIndex
        self.index_to_postToken = {token['accountIndex']: token for token in self.postTokenBalances}
    def get_from_postToken_index(self,index):
      return search_for_account_index(self.postTokenBalances,index)
    def get_postToken_amnt_dict(self,index):
      return self.get_from_postToken_index(index)
    def get_from_preToken_index(self,index):
      return search_for_account_index(self.preTokenBalances,index)
    def get_preToken_amnt_dict(self,index):
      return self.get_from_preToken_index(index)
    def get_amount_dict(self, amount, decimals=9):
        if isinstance(amount, dict):
            amount_dict = get_any_value(amount, 'uiTokenAmount')
            amount = get_any_value(amount_dict, 'amount')
            decimals = get_any_value(amount_dict, 'decimals')
        return exponential(amount, decimals, -1)

    def create_token_txns(self):
        dont_use = []
        for i,balances in enumerate([self.preTokenBalances,self.postTokenBalances]):
            for post in balances:
                index = post.get('accountIndex')
                if index not in dont_use:
                    dont_use.append(index)
                    after = self.get_amount_dict(self.get_from_postToken_index(index))
                    change = self.get_amount_dict(post)
                    if after!=None and change !=None:
                        before = after-change
                        address = self.acct_mgr.get_account_from_index(index)
                        owner = post.get('owner')
                        token = post.get('mint')
                        if i == 0:
                            pre_change = change
                            change = before
                            before = pre_change
                        self.all_txns["Address"].append(address)
                        self.all_txns["Owner"].append(owner)
                        self.all_txns['Balance Before'].append(before)
                        self.all_txns["Balance After"].append(after)
                        self.all_txns["Change"].append(change)
                        self.all_txns["Token"].append(token)
        return self.all_txns
      
    def visualize_txns(self):
        if not self.all_txns['Address']:  # Check if transactions are populated
            self.create_token_txns()  # Populate the transactions if not already done
        
        df = pd.DataFrame(self.all_txns)
        pd.set_option('display.max_columns', None)  # To display all columns
        print(df)

        return df
      
def get_token_txn_data(txnData=None,signature=None):
  txn_mgr = txnManager(txnData=txnData,signature=signature)
  return txn_mgr.create_token_txns()

def display_txn_data(txnData=None,signature=None):
  txn_mgr = txnManager(txnData=txnData,signature=signature)
  return txn_mgr.visualize_txns()

def get_transaction(signature,**kwargs):
  kwargs['signature']=signature
  txnData_mgr = TransactionProcessor(**kwargs)
  return txnData_mgr.get_txn_data()

