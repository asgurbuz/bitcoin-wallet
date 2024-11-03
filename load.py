from ecdsa import SigningKey, VerifyingKey
import hashlib
import base58check
def loadkey(usb):

    usb = input("please type  the letter for USB disk path: ")
    usb = usb.capitalize()
    with open(usb + ":/private.pem") as f:
        sk = SigningKey.from_pem(f.read())

    priv1=sk



    #public key variable
    public1 = priv1.verifying_key

    print("priv_key")
    print(priv1.to_string().hex())

    ##wif generate from private key
    ##version byte 0x80 for mainnet, 0xef for testnet

    p_sha=hashlib.sha256(bytes.fromhex("80") + priv1.to_string() )
    p_sha2=hashlib.sha256(p_sha.digest())
    p_checksum = p_sha2.digest()[0:4]
    base = bytes.fromhex("80") + priv1.to_string()  + p_checksum
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


    testnet = 1

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
    return created
    """
    ##public key compression
    if int((priv1.get_verifying_key().to_string().hex()[len(priv1.get_verifying_key().to_string().hex())-1]),16) % 2 == 0:
        pub_key_comp2 = bytes.fromhex("02") +priv1.get_verifying_key().to_string()[0:32]
    else:
        pub_key_comp2 = bytes.fromhex("03") + priv1.get_verifying_key().to_string()[0:32]




    ##first sha256
    t=hashlib.sha256(pub_key_comp2)

    ##ripemd160 hashing
    a=hashlib.new('ripemd160')
    a.update(t.digest())



    ##add version checksum 0x6f for testnet, 0x00 for main net
    q= "6F" + a.hexdigest()
    qq = bytes.fromhex("6F") + a.digest()


    ##second sha256 , first after ripemd160
    e=hashlib.sha256(qq)


    ##after ripemd, second sha256
    ee=hashlib.sha256(e.digest())


    ##address cheksum
    addr_chksm=ee.digest()[0:4]


    ##result + address checksum
    ad = qq + addr_chksm


    ## base58 check encode
    address=base58check.b58encode(ad)
    print(f"address is : {address.decode()}")


    print("priv_key: "+priv1.to_string().hex())
    print("public key: "+priv1.get_verifying_key().to_string().hex())

    ##version byte 0x80 for mainnet, 0xEF for testnet
    wif=base58check.b58encode(bytes.fromhex("EF") + priv1.to_string() + bytes.fromhex("01"))
    print(f"wif: {wif.decode()}")
    print(f"wif hex: {wif.hex()}")

    class addr:
        def __init__(self,priv,public,address,wif):
            self.priv = priv
            self.public = public
            self.address = address
            self.wif = wif

    created = addr(priv=priv1.to_string,public=bytes.fromhex("04") + priv1.get_verifying_key().to_string(),address=address.decode(), wif=wif)

    return created
    """