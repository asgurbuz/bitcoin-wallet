import binascii
import random
import textwrap
import hashlib
import base58check
import codecs
from ecdsa.util import PRNG
from ecdsa import SigningKey, VerifyingKey
from ecdsa import SECP256k1


def rand_key(p):

    key1 = ""

    for i in range(p):

        temp = str(random.randint(0, 1))
        # Concatenating the random 0, 1
        key1 += temp

    return (key1)


def create(usb, opt=0, sed=0):
    testnet = 1
    n = 256
    if opt == 0:
        str1 = rand_key(n)
        checksum = n/32
        bip39_m = str1 + str(bin(int(checksum)))[2:len(str(bin(int(checksum))))]


        t=bin(int(bip39_m,2))

        k=textwrap.wrap(bip39_m,11)


        ## BIP39 file opening
        bip=open("english.txt")
        a=0
        i=0
        seedwords=""


        ## Words are picking and importing into a text file
        for i in range(24):
            bip.seek(0)
            a=0
            for line in bip:
                a+=1
                if a == int(k[i], 2):
                    seedwords=seedwords+line
                    print(line)


        ##text file to import seed words are created
        seed=open(usb + ":/seed.txt","w")
        seed.write(seedwords)
        bip39_m = PRNG(t)
    if opt == 1:
        bip39_m=PRNG(sed)



    #private key is generated on secp256k1 curve with the seed created in early stage
    priv1=SigningKey.generate(curve=SECP256k1,entropy=bip39_m)

    #public key variable
    public1 = priv1.verifying_key

    print("priv_key")
    print(priv1.to_string().hex())

    ##wif generate from private key
    ##version byte 0x80 for mainnet, 0xef for testnet
    testnet_versionbyte = "ef"
    mainnet_versionbyte = "80"
    if testnet:
        p_sha=hashlib.sha256(bytes.fromhex(testnet_versionbyte) + priv1.to_string() )
        p_sha2=hashlib.sha256(p_sha.digest())
        p_checksum = p_sha2.digest()[0:4]
        base = bytes.fromhex(testnet_versionbyte) + priv1.to_string()  + p_checksum
    else:
        p_sha=hashlib.sha256(bytes.fromhex(mainnet_versionbyte) + priv1.to_string() )
        p_sha2=hashlib.sha256(p_sha.digest())
        p_checksum = p_sha2.digest()[0:4]
        base = bytes.fromhex(mainnet_versionbyte) + priv1.to_string()  + p_checksum
    wif=base58check.b58encode(base)

    print(f"wif: {wif.decode()}")
    print(f"wif hex: {wif.hex()}")

    #public key generated from private key (signing key= private key, verifying key=public key)
    print("pub_key:")
    print(priv1.get_verifying_key().to_string().hex())
    pub_key = bytes.fromhex("04") + priv1.get_verifying_key().to_string()
    print("public key in hexadecimal" + pub_key.hex())
    ##public key compression
    if int((priv1.get_verifying_key().to_string().hex()[len(priv1.get_verifying_key().to_string().hex())-1]),16) % 2 == 0:
        pub_key_comp2 = bytes.fromhex("02") +priv1.get_verifying_key().to_string()[0:32]
    else:
        pub_key_comp2 = bytes.fromhex("03") + priv1.get_verifying_key().to_string()[0:32]

    print(f"compressed pub_key is: {pub_key_comp2.hex()}")
    ##add version checksum 0x6f for testnet, 0x00 for main net
    chk_main="00"
    chk_test="6f"


    #uncompressed
    sha_un=hashlib.sha256(pub_key)


    ##ripemd160 hashing
    rp160_un=hashlib.new('ripemd160')
    rp160_un.update(sha_un.digest())


    

    ##add version checksum 0x6f for testnet, 0x00 for main net
    if testnet != 1 :

        q = chk_main + rp160_un.hexdigest()
        avcks_un = bytes.fromhex(chk_main) + rp160_un.digest()


    else:
        q= chk_test + rp160_un.hexdigest()
        avcks_un = bytes.fromhex(chk_test) + rp160_un.digest()

    ##second sha256 , first after ripemd160
    sha2_un=hashlib.sha256(avcks_un)


    ##after ripemd, second sha256
    sha3_un=hashlib.sha256(sha2_un.digest())


    ##address cheksum
    addr_chksm=sha3_un.digest()[0:4]


    ##result + address checksum
    pubbase_un = avcks_un + addr_chksm

    ## base58 check encode
    address=base58check.b58encode(pubbase_un)
    print(f"address is : {address.decode()}")

    class addr:
        def __init__(self,priv,public,address,wif):
            self.priv = priv
            self.public = public
            self.address = address
            self.wif = wif

    created = addr(priv=priv1.to_string,public=bytes.fromhex("04") + priv1.get_verifying_key().to_string(),address=address.decode(),wif=wif)

    with open(usb + ":/private.pem", "wb") as f:
         f.write(priv1.to_pem())
    with open(usb + ":/public.pem", "wb") as f:
         f.write(public1.to_pem())

    imp_addr = open(usb + ":/address.txt","w")
    imp_addr.write("address is: " + address.decode() + "\nwif: " + wif.decode() +
                    "\npriv key: " + priv1.to_string().hex() + "\npublic key: "
                   + priv1.get_verifying_key().to_string().hex() + "\ncompressed public key: " + pub_key_comp2.hex())
    print("\n Testnet:"+str(testnet) + "\n")
    print("key and address are successfully created and saved in the usb located in " + usb)

    return created
