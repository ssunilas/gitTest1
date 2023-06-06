from datetime import datetime
import urllib.request
import re
import xml.etree.ElementTree as ET
from xml.dom import minidom
import os
import os.path
import requests

#eb_number
# workArea = 'C:\bw-dev\'
# baseLineRelativePath = "product\installer\local\baseline\"
# bwIniFile = workArea+baseLineRelativePath+"tibco.home\bw\system\hotfix\bw\lib\bw.ini" 
bwIniFile = "'C:\bw-dev\product\installer\local\baseline\tibco.home\bw\system\hotfix\bw\lib\bw.ini"

isEbBuild = False

# def my_function(hii):
#   print(hii)


def readFile():
      with open(r'C:\bw-dev\product\installer\local\baseline\tibco.home\bw\system\hotfix\bw\lib\bw.ini', 'r') as file:
       line =  file.read()
      #  print(line)
       return line

def writeFileContents(file,contents):
  file.write(contents)
  file.close()
  line = file.read()
  return line

#
def updateBwIniFile():
    contents = [readFile()]
    print("*****************************8")
    print(contents[0])
    print(len(contents[0]))
    print("*****************************8")

    localtime = datetime.now();
    
    counter=0;
    tHfVer = " ";
    
    if(isEbBuild == True):
        tHfVer="EB$eb_number"
    else:
        tHfVer="$hotfix_no";
        print("eb build number should be valid")
    while(counter < len(contents)):
        contents[counter] = contents[counter].replace("product.hf.version= ", "product.hf.version="+tHfVer)
        contents[counter] = contents[counter].replace("product.build= ", "product.build=V$build_no")
        contents[counter] = contents[counter].replace("product.build.date= ", "product.build.date="+str(localtime.date()))
        counter=counter+1

    print('updated bw.ini file:')
    # contents.append("()())()()()()()()()()()()()()()()()")
   

    for line in contents:
        print(line);
    # push the changes i.e write the contents changes into BW INI File
    # eg :writeFileContents('C:\bw-dev\product\installer\local\baseline\tibco.home\bw\system\hotfix\bw\lib\bw.ini',contents)


def updateFeatureXml(xmlFilePath,feature,version):
     #with open(r'C:\bw-dev\palettes\design\features\com.tibco.bw.palette.design.feature\feature.xml','r') as fil:
    with open(r'C:\bw-dev\platform\binding\design\features\com.tibco.bw.core.design.binding.feature\feature.xml','r') as fil:
      content = fil.read()
      tree = ET.parse(fil.name)
      myroot = tree.getroot()
      for impor in myroot.iter('import'):
          if(impor.attrib.get('feature') == feature):
            impor.set('version',version)
            print(impor.attrib.get('version'))
    #   tree.write(file.name)
    #  fil.close()

def optimizeRus(listOfRus):
    myFeatures = listOfRus.split(',')
    feature = myFeatures[0]
    print(feature)

def validateParamter():
    
    productId = productId.strip()  
    version = version.strip()
    srcUrl = srcUrl.strip()
    hotfixNo = hotfixNo.strip()
    workArea = workArea.strip()
    buildNo = buildNo.strip()
    isBuildTrim = isBuildTrim.strip()
    listOfRus = listOfRus.strip()
    ebNumber = ebNumber.strip()
    cleanupTargetFiles = cleanupTargetFiles.strip()
    
    if(not hotfixNo.isdigit()):
        print("Please check value of hotfix number" + hotfixNo +" . It should be valid integer number")
        return
    elif(buildNo.isdigit()):
        print("Please check value of hotfix number" + buildNo +" . It should be valid integer number")
        return
    elif(isEbBuild.casefold() != 'true' or isEbBuild.casefold() != 'false'):
        print("Illegal choice for parameter " + isEbBuild + ", It should be either true or false.")
        return
    elif(not os.path.exists(workArea)):
         print("Please check value of workarea "+ workArea + ". It must be an existing directory")
         return
    elif(listOfRus):
        optimizeRus(listOfRus)

    pkg_path="/tsi/pkg/"+productId+"/"+version
    pkg_url="http://reldist.na.tibco.com/package/"+productId+"/"+version

def githubCheck(owner, repo, base_commit, head_commit):
    #Todo - barnch can be different other than master in case we need to specify branch
    url = f"https://api.github.com/repos/{owner}/{repo}/compare/{base_commit}...{head_commit}"
    response = requests.get(url)
    if response.status_code == 200:
        compare_data = response.json()
        files_changed = compare_data["files"]
        changed_files = [file["filename"] for file in files_changed]
        return changed_files
    else:
        print("Failed to fetch commit comparison. Status code:", response.status_code)


 # Provide the repository details and commit IDs
owner = "ssunilas"
repo = "firstProject"
base_commit = "b45be35"     #commit ID from
head_commit = "f1dc2a8"

# Call the function to get the changed files
changed_files = githubCheck(owner, repo, base_commit, head_commit)
# Print the changed files
print("Files changed after the commit:")
for file in changed_files:
    file_path = f"{owner}/{repo}/{file}"
    print(file_path)


     
# validateParamter() 
#updateFeatureXml("C:\bw-dev\palettes\design\features\com.tibco.bw.palette.design.feature\feature.xml","com.tibco.zion.feature","1.3.3001")    
  



