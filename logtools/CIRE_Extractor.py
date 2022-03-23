# -*- coding: utf-8 -*-
"""
Created on Tue Jan 25 15:36:54 2022

@author: phili
"""

import os, subprocess, tarfile, shutil
import urllib
from pathlib import Path
processEnv = {'JAVA_HOME': os.environ.get('JAVA_HOME'),
              'Path' : os.environ.get('PATH')}

def getData (dirPath, gameId, extract):
    url='http://ts.powertac.org/log/finals_2021_' + str(gameId) + '.tar.gz'
    # dirPath='D:/Powertac/finals-2021/'
    tarname=url[27:]
    file = tarname
    print(file)
    gameDirPath=str(gameId)
    
    currentDir = os.getcwd()
    os.chdir(dirPath)
    
    if not os.path.isdir(gameDirPath):
        os.mkdir(gameDirPath)
    os.chdir(gameDirPath)
    
    if not os.path.exists(tarname):
        g = urllib.request.urlopen(url)
        with open(tarname, 'wb') as f:
            f.write(g.read())
            print('Download complete.')
    else:
        print('Already downloaded.')
            
    if extract==True:
        if not os.path.exists("./log"):
            tar = tarfile.open(tarname)
            tar.extractall()
            tar.close
            print('Extraction complete.')
        else:
            print('Already extracted.')
        
        # # find the actual paths to the boot and sim logs and xml boot record
        # bootxml = ''
        # gameDir = Path(dirPath, gameDirPath)
        # for file in gameDir.glob('*.xml'):
        #     bootxml = file
        # bootDir = Path(dirPath, gameDirPath, 'boot-log')
        # bootfile = ''
        # simDir = Path(dirPath, gameDirPath, 'log')
        # simfile = ''
        # for file in bootDir.glob('*.state'):
        #     if (not str(file).endswith('init.state')):
        #         bootfile = file
        # for file in simDir.glob('*.state'):
        #     if (not str(file).endswith('init.state')):
        #         simfile = file
    
    os.chdir(currentDir)     
    
    return gameId, dirPath, file                
    
def extractData (dirPath, file, gameId, extractorClass,
                 dataPrefix):
    logtoolDir = 'C:\\Users\phili\Documents\PowerTac\powertac\powertac-tools\logtool-examples'
    logtoolDir = logtoolDir.replace(os.sep, '/')
    print("Processing ", file)
    datafileName = dataPrefix + str(gameId) + '.csv'
    dataDir = dirPath + '/data'
    dataPath = Path(dirPath, dataDir, datafileName)
    filePath = dirPath + '/' + str(gameId) + '/' + file
    
    # cmd_executeable_file_path = shutil.which('mvn')
    
    os.chdir(logtoolDir)
    
    if not dataPath.exists():
        args = ''.join(['org.powertac.logtool.example.' + extractorClass, ' ',
                        str(filePath), ' ',
                        dataDir + "/" + datafileName])
        args = args.replace("\\","/")
        command_line = 'mvn exec:exec -Dexec.args="' + args + '"'
        print(command_line)
        print(subprocess.run(command_line, shell=True, check=True,
                               stdout=subprocess.PIPE).stdout)

for i in range(1, 5):
    gameId, dirPath, file = getData('D:/Powertac/finals-2021', str(i), extract=False)
    extractData(dirPath, file, gameId,
                extractorClass = 'MktPriceStats', dataPrefix = 'mktPr')


