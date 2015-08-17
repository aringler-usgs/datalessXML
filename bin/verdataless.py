#!/usr/bin/env python

import glob
import os
import sys
from time import gmtime, strftime

sys.path.append(os.getcwd())
from aslparser import Parser

datalessLoc = '/dcc/metadata/dataless'

gitxmlLoc = '/home/aringler/datalessXML'
gitRepo = 'git@github.com:aringler-usgs/datalessXML.git'
debug = True







if __name__ == "__main__":

    

    #Grab the directory
    curDir = os.getcwd()

    #Move to the git repository and pull
    os.chdir(gitxmlLoc)
    process = os.system("git pull")

    #Remove the old conversion results file
    os.system('got rm ' + gitxmlLoc + '/ConversionResults')
    f = open(gitxmlLoc + '/ConversionResults','w')
    if debug:
        print(process)

    #Grab all dataless and convert it to xml
    dataLessFiles = glob.glob(datalessLoc + '/*.ASL*.seed')

    for dataLess in dataLessFiles:
        if debug:
            print(dataLess)
        try:
            sp = Parser(dataLess)
            newXML = dataLess.replace('seed','xml')
            newXML = newXML.replace('DATALESS','metadata')
            newXML = newXML.replace(datalessLoc,gitxmlLoc + '/stationdataless')
            if debug:
                print 'New xml file: ' + newXML
            sp.writeXSEED(newXML)
        except:
            print 'Unable to parse ' + dataLess 
            f.write('Unable to parse ' + dataLess + '\n')

    #Add new files to local git repository
    process = os.system("git add *.xml")
    f.close()
    process = os.system("git add ConversionResults")
    if debug:
        print(process)

    #Commit the changes using a message of the current time
    currentTime = "Changed" + strftime("%Y-%m-%d", gmtime())
    print(currentTime)
    process = os.system("git commit -m " + currentTime)
    if debug:
        print(process)
    process = os.system("git push " + gitRepo)
    
    os.chdir(gitxmlLoc)
    

