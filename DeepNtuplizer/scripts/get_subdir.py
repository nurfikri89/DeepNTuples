import os

root=("/eos/cms/store/group/phys_btag/ParticleEdge/Sun_112358_2025_prep/") ### Change to your production dir ###

def files(dir):
    list=os.listdir(dir)
    f=open("list.txt","w")
    for l in list:
        f.write(root+l+"\n")
        if os.path.isdir(os.path.join(dir,l)):
            files(os.path.join(dir,l))

files(root)
