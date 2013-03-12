import pybel
import numpy as np
import csv
from numpy import zeros
from numpy import asarray , sum
import io
import sys
from cStringIO import StringIO

def returnLsttoStr(numList):
    #print numList
    old_stdout = sys.stdout
    sys.stdout = stdout = StringIO()
    sys.stdout = stdout = StringIO()
    print numList
    sys.stdout = old_stdout
    foobar = stdout.getvalue()
    #print "foobar= ", foobar
    foobar = foobar.replace("]","")
    foobar = foobar.lstrip('[')
    return foobar;

'''
   Function  =  matrixCreate . this function creates the matrix of 0,1
   Details   =  We use numpy to create matrix as it performs faster
'''				
   
def matrixCreate(hashCompound , newCompoundList ):
    row_vector = []
    column_vector = []
    sortedKeys = hashCompound.keys()
    sortedKeys.sort()
    [row_vector.append(hashCompound[k]) for k in sortedKeys]
    [column_vector.append(k) for k in newCompoundList.keys()]
    hal_matrix = zeros([len(row_vector), len(column_vector)])
    count  = 0
    for k in column_vector:
        row_id_set =  newCompoundList[k]
        column_id =  count
        for row_id in row_id_set:
            hal_matrix[row_id,column_id] = 1
        count = count + 1    
    #when u print in file print column_vector
    #Against that print row_vector .
    '''
    with open('some.csv', 'wb') as f:
        writer = csv.writer(f)
        writer.writerows(column_vector)
   '''
    matrix_transpose = hal_matrix.transpose()
    f = open('matrix.txt',"w")
    #print matrix_transpose
    
    f.close()		
		
'''
    Function : searchPattern, two parameters are compunds dictionary and file with all compound details
	Details  : this function uses pybel library . It takes hashvalues from the dictionary , pybel library
		   the new dictionary output is newCompounds .
		   Now key of the dictionary is all compound values and every element of the dictionary points to 
		   a list of [key values from compounds dictionary]
'''			   


def searchPattern(compounds,filename):
    f = file(filename)
    newCompounds = dict()
    onlyCompounds = set()
    for keyValues in compounds.keys():
        #print values;
        hashval = compounds[keyValues]
        smarts = pybel.Smarts(hashval)
        f = file(filename)
        for line in f:
          line = line.replace("\n","")  
          smiles = line
          #print line
          mol = pybel.readstring( "smi", smiles)
          if smarts.findall( mol):
              if newCompounds.has_key(line):
                  temp = newCompounds[line]
                  temp.append(keyValues)
                  newCompounds[line] = temp
              else:
                  temp = []
                  temp.append(keyValues)
                  newCompounds[line] = temp         
        f.close()
    f = open('output.txt',"w")
    #for k , v in newCompounds.items():
        #print >>f,k , "  " , v
    '''
    for k,v in newCompounds.items():
        st = returnLsttoStr(v)
        line = ''
        strK = str(k)
        st = st.replace("]","")
        #f.write(st)
        line = line + strK + "   " + st
        f.write(line)
    '''
    for k,v in newCompounds.items():
        line = str(v)[1:-1]
        line = k + "    " + line  + "\n"
        f.write(line)
        #f.write("\n")
        #if "\n" in k:
            #print "is present"
    f.close()
    return newCompounds
'''
  Function : processTextFile
   Details :  it reads the hash file . It first seperates key and values . 
              After that keys are stored as keys of dictionary and value = hash value
'''   
def processTextFile(filename):
    compounds = dict()
    try:
        lines = open(filename).readlines() #take the whole corpus into a buffer
        for words in lines:
            total_words = words.split()
            modword =  total_words[0]
            modword = modword.replace("\n","")
            compounds[total_words[1]] = modword
    except Exception as inst:
         print inst
    #print compounds.items().sort     
    return compounds

def main():
    compounds = processTextFile("hash_file.txt")
    newCompounds = searchPattern(compounds,"compounds.txt")
    #matrixCreate(compounds,newCompounds);    
if __name__ == '__main__':
    main()
   
