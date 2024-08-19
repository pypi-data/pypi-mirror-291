import os
import LigPrepper as lp
try:
    from openbabel import openbabel
except:
    print(">>> Warning:\n"
          "            Could not find OpenBabel!!! SMILES2MOL2 and SMILES2PDBQT are not available!\n"
          ">>> To install openbabel:\n"
          "            conda install -c conda-forge openbabel")

def RunVina(vinabin, receptor, ligand, config):
    os.system("mkdir -p output log")
    command = vinabin+' --config '+config+' --receptor '+receptor+' --ligand '+ligand+' --out ./output/'+ligand+' > ./log/'+str(ligand)[0:-6]+'.log'
    os.system("%s" % command)
    if os.path.exists("./output/%s"%(ligand)):
        return "./output/%s"%(ligand)
    else:
        return None

def protpdb2pdbqt(protpdb):
    obConversion = openbabel.OBConversion()
    obConversion.SetInAndOutFormats("pdb", "pdbqt")
    obConversion.AddOption("p")
    obConversion.AddOption("r")
    mol = openbabel.OBMol()
    obConversion.ReadFile(mol, "%s.pdb"%(str(protpdb)[0:-4]))
    obConversion.WriteFile(mol, "%s.pdbqt"%(str(protpdb)[0:-4]))
    return "%s.pdbqt"%(str(protpdb)[0:-4])

def RunAutoDocker(protpdb, sdfile, config, vinabin):
    receptor = protpdb2pdbqt(protpdb)
    #receptor = "%s.pdbqt"%(str(protpdb)[0:-4])
    count, sdfiles = lp.splitsdf(sdfile)
    for sdf in sdfiles:
        ligand = lp.sdf2pdbqt(sdf)
        print("> %s"%(ligand[0:-6]),end=": ")
        outpdbqt = RunVina(str(vinabin), str(receptor), str(ligand), str(config))
        if outpdbqt:
            print("Success")
            outsdf = lp.pdbqt2sdf(outpdbqt)
            os.system("rm %s"%(ligand))
            os.system("rm %s"%(sdf))
        else:
            print("Failed")

