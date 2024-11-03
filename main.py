import createkey
import load
import spend
import seeds


class addr:
    def __init__(self, priv, public, address, wif):
        self.priv = priv
        self.public = public
        self.address = address
        self.wif = wif
usb = ""
a = addr
opt = input("please type \n1 to create address\n2 to load your wallet from the USB disk\n3 to spend\n"
            "4 to recover the wallet from seed (it works only if you have a seed file in appropriate format): \n")
if opt == "1":
    a = createkey.create(usb)
elif opt == "2":
    b = load.loadkey(usb)
elif opt == "3":
    if not a:
        try:
            c = load.loadkey(usb)
        except FileNotFoundError:
            print("File not found")

    to = input("please type the address you want to spend to: ")
    amount = input("please type the amount how much you want to spend: ")
    spend.spend(c.priv, to, amount)
elif opt == "4":
    seed = seeds.fromseed(usb)
    u = seeds.keyfromseed(usb, seedb=seed)
else:
    print("wrong input!!")
