import os

def files():
    f=open("list.txt","r")
    for sd in f:
        sd2 = sd[:-1]+'/output/'
        list=os.listdir(sd2)
        f2=open(sd2+"samples.txt", "w")
        for l in list:
            if l != 'samples.txt':
                f2.write(l+"\n")

files()
