#! /usr/bin/env python3

from GauAPIs.Molecule import Molecule
from GauAPIs import New_Calculator
from sys import argv
import numpy as np
import os 
import argparse


def get_external_coord(filein):
    with open(filein, 'r') as f:
        [atoms, deriva, charge ,spin] = [int(s) for s in f.readline().split()]
        ele = np.zeros((atoms,), dtype = int)
        
        atomlist = np.zeros((atoms,3), dtype = float)

        for i in range(atoms):
            axestr = f.readline().split()
            ele[i] = int(axestr[0])
            #convert from Bohr to Angstrom
            atomlist[i][0] = float(axestr[1])*0.52917724
            atomlist[i][1] = float(axestr[2])*0.52917724
            atomlist[i][2] = float(axestr[3])*0.52917724
    os.system(f'cp {filein} /share/home/Liaoyt/Work/DPI/1br5/3_layer/opt/test/')
    return ele, atomlist, deriva, charge, spin

def write_fileout(fileout, Ene, Gradient,der):
    with open(fileout, 'w') as f:
        f.write('%20.12E%20.12E%20.12E%20.12E\n'% (Ene,0.0,0.0,0.0)) 
        if der == 0:
            for i in range(Gradient.shape[0]):
                f.write('%20.12E%20.12E%20.12E\n'% (0.0,0.0,0.0))
                f.write('\n')
        elif der == 1:
            for i in range(Gradient.shape[0]):
                f.write('%20.12E%20.12E%20.12E\n'% (Gradient[i][0],Gradient[i][1],Gradient[i][2]))
                f.write('\n')
    
    return


def get_paras():
    parser = argparse.ArgumentParser(description='Connect files passed from Gaussian External command to the assigned methods for computation.',formatter_class=argparse.RawTextHelpFormatter)
    #Define all the regular arguments from Gaussian---by setting up the 固定参数
    inlist = ['layer','infile','outfile','Msg','FChk','MatE']
    helplist = ['layer info','.EIn','.EOu','.EMs','.EFc','.EUF']
    for i, it in enumerate(inlist):
        parser.add_argument(it,default=None,type=str,help=helplist[i])
    '''
    parser.add_argument('layer',default=None,type=str,help='layer info')
    parser.add_argument('infile',default=None,required=True,type=str,help='.EIn')
    parser.add_argument('outfile',default=None,required=True,type=str,help='.EOu')
    parser.add_argument('Msg',default=None,required=True,type=str,help='.EMs')
    parser.add_argument('FChk',default=None,required=True,type=str,help='.EFc')
    parser.add_argument('MatE',default=None,required=True,type=str,help='.EUF')
    '''
    #Define optional argument, i.e method
    parser.add_argument('-m','--method',default=None,type=str,help='Method e.g. aiqm1...')
    parser.add_argument('-n','--CPU',default=None,type=int,help='define cpu for parallelization')
    args = parser.parse_args()
    return args

def run():

    '''    
    if len(argv) < 8:
        print("You should define a certain method used to calculate this layer\n e.g.: APIs gfn2-xtb\n ")
        print("If you want to use orca, you should method meanwhile define the core \n e.g.: APIs method core\n")
    elif len(argv) == 9 :
        
        method_use = argv[1]
        core = argv[2]
        filein = argv[4]
        fileout = argv[5]
    elif len(argv) == 8:
        method_use = argv[1]
        filein = argv[3]
        fileout = argv[4]
        '''
    args = get_paras()
    filein = args.infile
    fileout = args.outfile
    method_use = args.method
    molname = f'{method_use}-input'
    elelist, coors, deriva, charge, spin = get_external_coord(filein)
    Mole = Molecule(elelist,coors,charge,spin,molname)
    New_Calculator.mol2xyz(Mole)
    #use different calculators to calculate the energy and gradient according to method defined.
    if args.CPU != 1:
    #set parallelization and stacksize
        os.environ['OMP_STACKSIZE'] = f'{args.CPU}G'
        os.environ['OMP_NUM_THREADS'] = f'{args.CPU},1'
        os.environ['OMP_MAX_ACTIVE_LEVELS'] = '1'    
        print(os.environ['OMP_NUM_THREADS'])
        print(os.environ['OMP_STACKSIZE'])
        
    if args.method != None:
        if method_use.lower() in ['xtb', 'gfn2-xtb', 'gfn1-xtb']:
            #os.system('source activate Strain_VIZ')
            print('Using xtb-python')
            if method_use == 'xtb' or method_use == 'gfn2-xtb':
                meth_in = 'GFN2-xTB'                                  # gfn2xtb=1 in Param
            elif method_use == 'gfn1-xtb':
                meth_in = 'GFN1-xTB'                                 ## gfn2xtb=2 in Param

            #define parallelization
            if args.CPU != None:
                print(f'This xtb task will use {args.CPU} cores ')
                Ene, Gradient = New_Calculator.calculate_mol_tblite(Mole,meth_in,int(args.CPU))
            #Ene, Gradient = New_Calculator.calculate_mol_xTB(Mole,meth_in)
            Ene, Gradient = New_Calculator.calculate_mol_tblite(Mole,meth_in)
            print('xtb calculation finished')
        elif method_use.lower() in ['ani-1x', 'ani-2x','ani-1ccx']:
            print('Using ani')
            #os.system('source activate Strain_VIZ')
            Ene, Gradient = New_Calculator.calculate_mol_ani(Mole,method_use)
            print('ani calculation finished')
        elif method_use.lower() in ['aiqm1', 'aiqm1@dft']:
            print('Using mlatom')
            method_use = method_use.upper()
            Ene,Gradient = New_Calculator.calculate_mol_mlatom(f'{Mole.name}.xyz',charge,spin,method_use)  
            print('mlatom finished')
        else:
            os.system('source /share/home/yanz/bin/env/OC51.env')
            print(f'External will try use orca to compute the energy and gradient in {method_use} level')
            core = args.CPU
            Ene, Gradient = New_Calculator.calculate_mol_orca(Mole,charge,spin,method_use,core,deriva)

    write_fileout(fileout, Ene, Gradient,deriva)



if __name__ == "__main__":
    run()
    


        
    
    
    
    
    