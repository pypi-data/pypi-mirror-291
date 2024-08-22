from abstract_solcatcher import eatAll,make_list,callSolcatcherRpc
def get_txn_data(file_path=None):
  file_path = file_path or 'txnData.json'
  return safe_read_from_json(file_path)
def get_account_keys(txnData):
    return txnData['transaction']['message']['accountKeys']

def get_loaded_addresses(txnData):
    return txnData['meta']['loadedAddresses']

def get_read_only_addresses(txnData):
    return get_loaded_addresses(txnData).get('readonly', [])

def get_writable_addresses(txnData):
    return get_loaded_addresses(txnData).get('writable', [])

def get_all_account_keys(txnData):
  accountKeys = get_account_keys(txnData) 
  accountKeys+= get_read_only_addresses(txnData)
  accountKeys+= get_writable_addresses(txnData)
  return accountKeys

class saveAcountKeys:
  def __init__(self,txnData):
    self.accountKeys = get_account_keys(txnData)
    self.loaded_addresses = get_loaded_addresses(txnData)
    self.read_only_addresses = get_read_only_addresses(txnData)
    self.writable_addresses = get_writable_addresses(txnData)
    self.accountKeys = self.get_all_addresses()
    
  def get_all_addresses(self):
    self.accountKeys = self.accountKeys
    self.accountKeys += self.read_only_addresses
    self.accountKeys += self.writable_addresses
    return self.accountKeys

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
        clusterCount = 0
        self.logClusters =[]
        for i,log in enumerate(self.logMessages):
          logLower = log.lower()
          if 'invoke' in logLower:
            self.logClusters.append({"logs":[],"clusterIndex":clusterCount,"type":None,"types":[],"start":i,"end":i,"programId":log.split(' ')[1]})
          if 'success' in logLower:
            self.logClusters[-1]["end"]=i
          self.logClusters = self.get_log_type(log)
        return self.logClusters
      def get_log_type(self,log):
        currentLogClusterJs = {}
        logSpl = [eatAll(logSp,[' ',':']) for logSp in log.split(' ') if logSp][1:]
        currentLogClusterJs = {"programId":logSpl[0],"type":logSpl[1]}
        for i,log in enumerate(logSpl):
          if log == 'log':
            currentLogClusterJs['type'] = logSpl[-1] or logSpl[-2]
            self.logClusters[-1]["type"] = currentLogClusterJs['type']
        if len(logSpl)>2:
         currentLogClusterJs["action"]=logSpl[2]
        if len(logSpl)>2:
         currentLogClusterJs["vars"]=' '.join(logSpl[3:])
        self.logClusters[-1]["types"].append(currentLogClusterJs['type'])
        self.logClusters[-1]["logs"].append(currentLogClusterJs)
        return self.logClusters
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
      input(self.txnData)
      txnData['transaction']['message']['instructions'] = self.instruction_mgr.instructions
      txnData['meta']['innerInstructions'][0]['instructions'] = self.instruction_mgr.inner_instructions
      return self.txnData
    
    def getTransacion(self,signature,**kwargs):
      kwargs['signature']=signature
      return callSolcatcherRpc('getTransaction',**kwargs)
def get_transaction(signature,**kwargs):
  kwargs['signature']=signature
  txn_mgr = TransactionProcessor(**kwargs)
  return txn_mgr.get_txn_data()

