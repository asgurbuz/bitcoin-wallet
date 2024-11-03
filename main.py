import createkey
import load
import spend
import seeds
usb = input("please type  the letter for USB disk path: ")

usb = usb.capitalize()

opt = input("please type \n1 to create address\n2 to load your wallet from the USB disk\n3 to spend\n"
            "4 to recover the wallet from seed (it works only if you have a seed file in appropriate format): \n")
if opt == "1":

    a = createkey.create(usb)
elif opt == "2":
    b = load.loadkey(usb)

elif opt == "3":
    b = load.loadkey(usb)
    to = input("please type the address you want to spend to: ")
    amount = input("please type the amount how much you want to spend: ")

    spend.spend(b.priv, to, amount)
elif opt == "4":
    seed = seeds.fromseed(usb)
    u = seeds.keyfromseed(usb, seedb=seed)
else:
    print("wrong input!!")
