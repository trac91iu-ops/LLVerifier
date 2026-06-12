#!/bin/python3
import random
import os
_NAME = 'iotlogic'
_alphabet = ['_']
_alphabet += [chr(i) for i in range(ord('A'),ord('Z')+1)]
_alphabet += [chr(i) for i in range(ord('a'),ord('z')+1)]
_counter = 0
def multiLineInput(txt=''):
    tmpFile = f'/tmp/{_NAME}_buffer'
    f = open(tmpFile,'w')
    f.close()
    cmd = input('Multiple lines input>').strip()
    if cmd =='q':
        return None
    else:
        os.system(f'$EDITOR {tmpFile}')
        return fread(tmpFile)

def editInTmpFile(txt):
    tmpFile = f'/tmp/{_NAME}_buffer'
    f = open(tmpFile,'w')
    f.write(txt)
    os.system(f'$EDITOR {tmpFile}')
    return fread(tmpFile)

def fwrite(fn,txt:str):
    with open(fn,'w') as f:
        f.write(txt)

def fread(fn):
    with open(fn,'r') as f:
        return f.read()

def genTmpFileName():
    global _counter
    _counter += 1
    return f'/tmp/{_NAME}_tmp{_counter}'
    #return f'/tmp/{_NAME}_'+''.join([random.choice(_alphabet) for i in range(6)])

def allf(*fs):
    '''
    condition combinator
    fs = fa,fb,...
    fa(x)->Bool
    fb(x)->Bool
    '''
    def helper(x):
        for f in fs:
            if not f(x):
                return False
        return True
    return helper

def disDuplicate(el:list)->list:
    #no used in current version
    #dis-duplicate while keeping the original order
    l = []
    for e in el:
        if e not in l:
            l.append(e)
    return l

def parentDir(path):
    return os.path.abspath(os.path.join(path, os.pardir))

if __name__ == '__main__':
    print(genTmpFileName())
