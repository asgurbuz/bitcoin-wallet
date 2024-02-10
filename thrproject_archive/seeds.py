from createkey import create

def fromseed(usb):
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
    create(usb,opt = 1,sed=seedb)
