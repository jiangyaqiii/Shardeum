import json
import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
answer_dict = {
    'level1':{
        'Which of the following is not a decentralized/public blockchain network?':'B',
        'Which of the following best describes a "block" in a blockchain?':'A',
        'Which of the following is a layer 1 blockchain platform/network?':'C',
        'What is the purpose of a merkle tree in a blockchain?': 'D',
        'Which of the following is NOT a consensus mechanism used in typical blockchain networks?': 'A',
        'What type of digital ledger and database is blockchain technology?':'D',
        'Nonces in ____  network are used to create unique identifiers for transactions to prevent double-spending/replay attacks but are NOT used to determine the selection of validators.':'D',
        'What is the unique identifier for a block in a blockchain called?': 'C',
        'What is the core problem that blockchain solves?':'B',
        'Which of the following represent the bedrock principles of a public blockchain?':'C',
    },'level2':{
        'What are three primary types of blockchain clients?':'A',
        'What is the benefit of decentralization in blockchain networks?':'D',
        'Which of the following is what makes it possible for a group of strangers to work together to build and maintain a shared database like blockchain, without needing to trust each other?': 'D',
        'Which of the following is the primary benefit of decentralization in the context of censorship resistance?': 'C',
        'Which of the following best describes how decentralization operates in blockchain networks?': 'B',
        """Which blockchain consensus mechanism promotes decentralization by allowing any participant to contribute to the network's security and governance, albeit, by using expensive and powerful hardware?""":'A',
        'Which is the most significant indicator of a highly decentralized blockchain/Web3 network?':'C',
        'Which decentralized technology allows users to access web content and services without relying on traditional domain names and centralized DNS?':'D',
        'Which of the following does NOT represent decentralization in the Decentralized Finance or DeFi industry?':'B',
        'Which of the following best describes a blockchain “client”?':'C',
    },'level3':{
        'What is the primary reason for keeping a safe backup of your passphrase (or seed phrase/backup codes) when using blockchain wallets, even though other security measures mentioned here may also apply?': 'A',
        """Consider a malicious attacker creating multiple pseudonymous identities by taking control over a node or group of nodes. These nodes are then used to spread misinformation, disrupt consensus, or attempt to influence the network's decisions. What is the nefarious act known as in the context of blockchain?""":'A',
        'As modern blockchain networks strive to reduce transaction fees, which attack type lets attackers cheaply flood the network with low cost requests to slow/disrupt it?':'D',
        'Beyond the consensus mechanism, which of the below is the most ideal technique sharded blockchains can employ to maintain the high security levels that public blockchains are known for?':'A',
        'Asides from hashing, which other key cryptographic method does blockchain technology employ to ensure that data doesn’t change during the broadcast of validated transactions between nodes and throughout all blockchain transactions for that matter?':'C',
        'Why do experts often emphasize addressing security issues at Layer 1 of a blockchain rather than relying solely on Layer 2 blockchains and other scaling solutions?':'C',
        'Safe deposit boxes (or bank lockers) are secured by a key that only the owner (custodians like banks) have access to. Similarly, what protects digital assets owned by users themselves on a blockchain?':'C',
        'How can Proof-of-Stake (PoS) networks, such as Ethereum, achieve a security level comparable to that of Proof-of-Work (PoW) networks like Bitcoin?':'B',
        'Which term is commonly associated with the practice of prioritizing certain transactions on a blockchain by reordering them for potential financial gains, especially in the context of DeFi platforms?':'C',
        'Which is the most battle-tested, highly secure hashing algorithm used by various blockchain networks to handle transactions and record data?':'D',
    },'level4':{
        'Which statement accurately describes the relationship between ERC standards (Ethereum request for Comments) and EIPs in the Ethereum ecosystem?':'B',
        'In the Ethereum blockchain, if someone were describing the overall structure and various levels of data organization, which of the following statements is accurate?':'C',
        'In which layer of blockchain architecture do smart contracts and dapps primarily operate while the end users directly interact with?': 'A',
        'Choose the correct answer. Which consensus algorithms are used by L1 blockchains, Bitcoin and Ethereum respectively?': 'B',
        'Which key property in blockchain helps it to achieve both these desired outcomes - high fairness and prevent double-spending?': 'A',
        'What type of blockchain network or platform allows anyone to participate in running nodes, anyone can read from or write to and is permissionless?': 'C',
        'Which of the following reasons explains why specialized sandbox environments called testnets or test networks are crucial for blockchain platforms?':'C',
        'What is the primary purpose of improvement proposals or blockchain standards like EIP or BIP (Ethereum/Bitcoin Improvement Protocols) in the Ethereum/Bitcoin ecosystem?': 'D',
        'What is the role of Virtual Machines like Ethereum Virtual Machine (EVM) in blockchain architecture?':'D',
        'What is the primary purpose of a smart contract in a blockchain network?':'D',
    }
    ,'level5':{
        '"Blockchain trilemma” or “Scalability trilemma," is a longstanding issue that hinders the mass adoption of blockchain networks. Which three features are encompassed by this trilemma in public blockchains?':'A',
        'Which feature of blockchain and smart contract platform represents this statement “A decentralized exchange (DEX) can be combined with a decentralized lending protocol to create a new application that allows users to borrow and lend assets while also trading them.”':'D',
        'Which feature in blockchain ensures that once a transaction is confirmed, it cannot be reversed?':'D',
        'Which of the following best describes the average transactions per second (TPS) comparison between a centralized network like Visa and typical public blockchain networks?':'A',
        'Which feature ensures that transactions on the blockchain are processed quickly?':'C',
        'What is a primary consequence of a blockchain network relying on high staking requirements and increased processing power (vertical scalability) while having limited throughput and scalability?':'D',
        'In public blockchains, what permanent consequence occurs when validators fail to achieve consensus on the upcoming blocks or transactions to be appended?':'A',
        'Which of the below is an ideal and a highly decentralized solution for scalability issues in public blockchains?':'B',
        'Why is high fairness important in a blockchain network?':'B',
        'Which feature addresses the potential of a public blockchain to handle increased transaction loads?':'D',
    },'level6':{
        'In a blockchain network, which type of nodes provides interfaces for querying and interacting with the blockchain without the need to store the full transaction history?':'C',
        'What are nodes in a blockchain network?':'A',
        'Which nodes are known to facilitate data transmission and propagation across PoS networks including sharded and cross-chain networks?':'A',
        'Which nodes are primarily responsible for actively participating in the process of ordering and validating transactions, forming consensus, proposing a block, and securing the network in PoS networks?':'B',
        'What type of nodes provide an interface between traditional web browsers and IPFS (InterPlanetary File System), a decentralized storage network?':'D',
        'What type of nodes typically store the complete blockchain transaction history while maintaining the blockchain’s historical data as well?':'C',
        'In Filecoin, a decentralized storage platform, which type of nodes offer storage capacity, furnish cryptographic evidence of their reliable data storage, and swiftly deliver stored data to users when requested?':'B',
        'What type of nodes typically store the complete blockchain transaction history while maintaining the current state of the ledger?':'D',
        'Which of the following best describes the role of blockchain client software for nodes?':'B',
        'What is the most accurate statement with respect to consensus mechanisms in sharded blockchain networks?':'A',
    },'level7':{
        'Which of the following best describes the difference between on-chain and off-chain solutions in the context of blockchain technologies?':'B',
        'What necessitated layer 2 blockchains and solutions on top of layer 1 blockchains?':'D',
        'In the evolving landscape of blockchain infrastructure, how do decentralized storage networks differentiate themselves from traditional data storage mechanisms?':'C',
        'How does a “wallet” primarily interface with the blockchain network':'B',
        'What is the primary role of a wallet in blockchain?':'B',
        'In the context of blockchain technology, what primary role do websockets play?':'C',
        'Which of the following is not considered a layer 2 solution in blockchain?':'A',
        'Why are development tools/frameworks like Truffle, Hardhat and Anchor essential for blockchain development':'A',
        'Which of the following popular software clients are used for interacting with the Bitcoin and Ethereum blockchains respectively?':'A',
        'Which of the following are considered to be part of blockchain infrastructure?':'D',
    },'level8':{
        'In the context of Ethereum dapp development, how is the Solidity programming language best characterized?':'C',
        'Which of the following options represent the primary challenge for smart contracts and the larger blockchain industry as a whole?':'C',
        'Which of these is NOT a use case for smart contracts?':'B',
        'What is the significant advantage of using oracles in smart contracts?':'A',
        'How exactly did Ethereum elevate the potential of blockchain technology pioneered by Bitcoin? Choose the correct answer.':'B',
        'Which of the following is the MOST accurate definition of gas estimate and gas limit?':'A',
        'How are smart contract vulnerabilities typically exploited?':'D',
        'What is the term used to refer to the fee paid by end users to execute a function in a smart contract such as transferring tokens, voting in a DAO or minting an NFT?':'C',
        'What are the benefits of using smart contracts to manage supply chains?':'D',
        'Which of the following best describes a complex smart contract?':'A',
    },'level9':{
        'Which of the following does not operate as a decentralized application (dapp)?':'B',
        'Which of the following is a use case of decentralized application (Dapp)?':'C',
        'What is the main distinction between smart contracts and dapps (Decentralized Applications)?':'D',
        'Which layer on a L1 blockchain does smart contracts and dapps typically reside?':'A',
        'Which of the following platforms does NOT function both as a Layer 1 (L1) blockchain and as a smart contract platform enabling decentralized solutions and applications for end users?':'A',
        'Which term refers to a collection of smart contracts that act as a back-end with a front-end user interface?':'A',
        "In a dapp, what is the role of a 'token'?":'D',
        'Which component in a dapp ensures that it can operate without a central authority?':'C',
        'How can dapps be described in terms of governance?':'B',
        "On which of the following factors does a dapp's performance primarily depend?":'C',
    },'level10':{
        '_____  are blockchain systems that run parallel to a “mainchain" or L1 blockchain providing a mechanism to offload transactions from the mainchain, while performing their own consensus mechanism to reduce congestion and allow for faster processing times and interoperability.':'D',
        'What is the use case of Zero-Knowledge Proofs (zk-proofs) technology in blockchain?':'D',
        'Which statement best describes the differences among lightweight wallets, full-node wallets, and third-party wallet applications in the context of blockchain?':'C',
        'What role does a blockchain explorer play in the blockchain ecosystem?':'D',
        'Which of the following best describes the primary function of the MetaMask web browser extension?':'C',
        'What is the common objective that blockchain bridges, atomic swaps, and synthetics aim to achieve in the Web3 ecosystem?':'B',
        '_____ platforms aggregate and interpret vast amounts of on-chain data to produce useful metrics and insights about network health, economic activity, market sentiment, and more.':'B',
        "Which (Ethereum) Layer-2 scaling solution utilizes zero-knowledge proofs to cryptographically ensure every transaction's correctness without requiring fraud verification windows or challenge periods?":'D',
        'Why are oracles considered an important blockchain interface?':'A',
        'Which Ethereum Layer-2 scaling solution processes transactions off-chain assuming them to be correct unless proven otherwise requiring a dispute resolution window?':'C',
    }
}
link_dict = {
    '1':'https://shardeum.org/explore/blockchain-grandmaster-quiz/level-1-blockchain-technology/',
    '2':'https://shardeum.org/explore/blockchain-grandmaster-quiz/level-2-decentralization/',
    '3':'https://shardeum.org/explore/blockchain-grandmaster-quiz/level-3-blockchain-security/',
    '4':'https://shardeum.org/explore/blockchain-grandmaster-quiz/level-4-blockchain-architecture/',
    '5':'https://shardeum.org/explore/blockchain-grandmaster-quiz/level-5-blockchain-features/',
    '6':'https://shardeum.org/explore/blockchain-grandmaster-quiz/level-6-blockchain-nodes/',
    '7':'https://shardeum.org/explore/blockchain-grandmaster-quiz/level-7-blockchain-infrastructure/',
    '8':'https://shardeum.org/explore/blockchain-grandmaster-quiz/level-8-smart-contracts/',
    '9':'https://shardeum.org/explore/blockchain-grandmaster-quiz/level-9-dapps/',
    '10':'https://shardeum.org/explore/blockchain-grandmaster-quiz/level-10-blockchain-interfaces-utilities/',
}

letter_index_dict = {'A':1, 'B':2, 'C':3, 'D':4}
# def get_driver():
#     options = Options()
#     # 连接到已经打开的Chrome浏览器会话
#     options.add_experimental_option("debuggerAddress", "127.0.0.1:9223")
#     driver = webdriver.Chrome("chromedriver.exe", options=options)  ##启动搜索引擎
#     return driver
def get_driver():
    def Modify_option_attribute():
        chrome_options = Options()
        chrome_options.add_experimental_option('excludeSwitches', ['enable-automation']) ##开发者模式
        chrome_options.add_argument("headless") ##无头模式
        chrome_options.add_argument('disable-blink-feathers=AutomationControlled') ##禁用启用Blink运行时的功能
        chrome_options.add_argument('user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36')
        return chrome_options
    chrome_options = Modify_option_attribute()
    driver = webdriver.Chrome("chromedriver.exe", options=chrome_options)  ##启动搜索引擎
    driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
        "source":"""
        Object.defineProperty(navigator, 'webdriver', {
            get: () => undefined
        })
        """
    })
    return driver
def start_timu(driver, level_index, name, email, country, address):
    ##点击开始
    try:
        driver.find_element_by_name('next').click()
    except:
        driver.find_element_by_xpath('/html/body/div[2]/div[1]/div/div/div[2]/button[3]').click()
        time.sleep(3)
        driver.find_element_by_name('next').click()
    ##持续加载题目，直到加载出题目为止
    for question_num in range(1, 11):
        if level_index == 1:
            id = f'//*[@id="ays_finish_quiz_7"]/div[{question_num+1}]/div'
        elif level_index == 2:
            id = f'//*[@id="ays_finish_quiz_6"]/div[{question_num+1}]/div'
        else:
            id = f'//*[@id="ays_finish_quiz_{7+level_index-2}"]/div[{question_num+1}]/div'
        while driver.find_element_by_xpath(f'{id}/div[1]').text == '':
            pass
        ##此等級的答案合集，因为顺序错乱的
        total_answers = answer_dict[f'level{level_index}']
        ##问题描述
        question_sub = driver.find_element_by_xpath(f'{id}/div[1]').text
        ##答案对应的数字
        letter_index = letter_index_dict[total_answers[question_sub]]
        answer_xpath = f'{id}/div[3]/div[{letter_index}]'
        try:
            driver.find_element_by_xpath(answer_xpath).click()
        except:
            driver.find_element_by_xpath('/html/body/div[2]/div[1]/div/div/div[2]/button[3]').click()
            time.sleep(3)
            driver.find_element_by_xpath(answer_xpath).click()
    if 'See Result' in driver.page_source:
        try:
            driver.find_element_by_name('ays_user_name').clear()
            driver.find_element_by_name('ays_user_name').send_keys(name)
        except:
            driver.find_element_by_name('ays_user_name').send_keys(name)
        try:
            driver.find_element_by_name('ays_user_email').clear()
            driver.find_element_by_name('ays_user_email').send_keys(email)
        except:
            driver.find_element_by_name('ays_user_email').send_keys(email)
        try:
            driver.find_element_by_name('quiz_attr_3').clear()
            driver.find_element_by_name('quiz_attr_3').send_keys(country)
        except:
            driver.find_element_by_name('quiz_attr_3').send_keys(country)
        try:
            driver.find_element_by_name('quiz_attr_4').clear()
            driver.find_element_by_name('quiz_attr_4').send_keys(address)
        except:
            driver.find_element_by_name('quiz_attr_4').send_keys(address)
        try:
            driver.find_element_by_name('ays_finish_quiz').click()
        except:
            driver.find_element_by_xpath('/html/body/div[2]/div[1]/div/div/div[2]/button[3]').click()
            time.sleep(3)
            driver.find_element_by_name('ays_finish_quiz').click()

def answer(name, email, country, address):
    print(f'地址:{address}开始测验')
    driver = get_driver()
    for level_index in range(1, 11):
        driver.get(link_dict[str(level_index)])
        ##Start
        while 'Start' not in driver.page_source:
            print(f'{address}:重新加载{link_dict[str(level_index)]}')
            driver.get(link_dict[str(level_index)])
            time.sleep(2)
        start_timu(driver, level_index, name, email, country, address)
        time.sleep(2)
    driver.close()
    print(f'地址:{address}完成了测验')

import threading
def shardeum_main():
    fin_list = []
    userinfo = pd.read_csv('userinfo.csv')
    userinfo_list = userinfo.values
    thread_list = []
    for user in userinfo_list:
        name = user[0]
        email = user[1]
        country = user[2]
        address = user[3]
        _t = threading.Thread(target=answer, args=(name, email, country, address, ))
        _t.start()
        fin_list.append(address)
        thread_list.append(_t)
    for _t in thread_list:
        _t.join()
    return fin_list




