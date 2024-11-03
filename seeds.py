from createkey import create

def fromseed(usb):
    usb = input("please type  the letter for USB disk path: ")
    usb = usb.capitalize()
    seedb=""
    biplist = []
    seed = open(usb + ":/seed.txt")
    bip = open("english.txt")
    for line in bip:
        biplist.append(line)
    for line in seed:
        seedb = seedb + str(bin(biplist.index(line)).removeprefix("0b"))

    return seedb.removeprefix("0b")
def keyfromseed(usb,seedb):
    usb = input("please type  the letter for USB disk path: ")
    usb = usb.capitalize()
    create(usb,opt = 1,sed=seedb)
