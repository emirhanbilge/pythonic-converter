import xml.etree.ElementTree as ET
import csv ,json ,sys
from xml.dom import minidom
from xml.etree.ElementTree import ElementTree
from lxml import etree

def CSVtoXML(readFile,writeFile):

    root = ET.Element('departments')
    with open(readFile, "r", encoding="utf-8", errors="ignore") as f:
        file = csv.reader(f, delimiter=";")
        next(file)  # ilk satırı geç
        uniName =""
        for row in file:
            if row[1] != uniName:
                university = ET.SubElement(root,'university', {'name':str(row[1]),'uType':str(row[0])})
                uniName = str(row[1])

            item = ET.SubElement(university ,'item',{'id':str(row[3]) , 'faculty':str(row[2]) })
            if row[5] == "İngilizce":
                row[5] = "en"
            else:
                row[5] = "tr"
            if row[6] =="":
                row[6] ="No"
            else:
                row[6]="Yes"

            name = ET.SubElement(item,'name',{'lang':str(row[5]),'second':str(row[6])})
            name.text = str(row[4])
            period = ET.SubElement(item,'period')
            period.text = str(row[8])
            quota = ET.SubElement(item,'quota',{'spec':str(row[11])})
            quota.text = row[10]
            field = ET.SubElement(item,'field')
            field.text = row[9]
            last_min_score = ET.SubElement(item,'last_min_score',{'order':row[12]})
            last_min_score.text = row[13]
            grant = ET.SubElement(item,"grant")
            grant.text =row[7]
        
        from xml.etree.ElementTree import ElementTree
        tree = ET.ElementTree(root)
        tree.write(writeFile,encoding="utf-8",xml_declaration=True)

def XMLtoCSV(openFile,writeFile):
    tree = ET.parse(openFile)
    root = tree.getroot()
  
    first_row = "ÜNİVERSİTE_TÜRÜ;ÜNİVERSİTE;FAKÜLTE;PROGRAM_KODU;PROGRAM;DİL;ÖĞRENİM_TÜRÜ;BURS;ÖĞRENİM_SÜRESİ;PUAN_TÜRÜ;KONTENJAN;OKUL_BİRİNCİSİ_KONTENJANI;GEÇEN_YIL_MİN_SIRALAMA;GEÇEN_YIL_MİN_PUAN\n"
    rootCount = 0 
    file = open(writeFile,"a")
    file.write(first_row)
    str = "%s;%s;%s;%s;%s;%s;%s;%s;%s;%s;%s;%s;%s;%s\n"
    while(rootCount<len(list(root))):
        uniName = root[rootCount].get('name')
        uniType = root[rootCount].get('uType').title()
        for i in range(len(list(root[rootCount]))):
            id      = root[rootCount][i].get('id')
            faculty = root[rootCount][i].get('faculty')
            depName = root[rootCount][i].find('name').text
            lang    = root[rootCount][i].find('name').get('lang')
            if lang=='en':
                lang = "İngilizce"
            else:
                lang=""
            second  = root[rootCount][i].find('name').get('second')
            period  = root[rootCount][i].find('period').text
            quatoSpec = root[rootCount][i].find('quota').get('spec')
            quato     = root[rootCount][i].findtext('quota',default=None)
            field     = root[rootCount][i].find('field').text
            order     = root[rootCount][i].find('last_min_score').get('order')
            last_min_score = root[rootCount][i].find('last_min_score').text
            grant  = root[rootCount][i].find('grant').text
            file.write((str %(uniType,uniName,faculty,id,depName,lang,second,grant,period,field,quato,quatoSpec,order,last_min_score)))
        rootCount+=1
    file.close()

def XMLtoJSON(readFile,writeFile):

    tree = ET.parse(readFile)
    root = tree.getroot()
    rootCount = 0
    totalArr = []
    while(rootCount<len(list(root))):
        university = {}
        university['uType'] = root[rootCount].get('uType').title()
        university['university_name'] = root[rootCount].get('name')
        item = {}
        items =[]
        departments = []
        for i in range(len(list(root[rootCount]))):
            item = {}
            items =[]
            body = {}
            body['id']      = root[rootCount][i].get('id')
            item['faculty']  = root[rootCount][i].get('faculty')
            body['name'] = root[rootCount][i].find('name').text
            body['lang']    = root[rootCount][i].find('name').get('lang')
            body['second']  = root[rootCount][i].find('name').get('second')
            body['period']  = root[rootCount][i].find('period').text
            body['spec'] = root[rootCount][i].find('quota').get('spec')
            body['quota']     = root[rootCount][i].findtext('quota',default=None)
            body['field']     = root[rootCount][i].find('field').text
            body['order']     = root[rootCount][i].find('last_min_score').get('order')
            body['last_min_score'] = root[rootCount][i].find('last_min_score').text
            body['grant']  = root[rootCount][i].find('grant').text
            departments.append(body)
            item['departments'] = departments
            items.append(item)
        university['items'] = items
        totalArr.append(university)
        rootCount+=1
    with open(writeFile, 'w',encoding="utf-8") as f:
        json.dump(totalArr, f ,ensure_ascii=False)
    f.close()

def JSONtoXML(readFile,writeFile):
    root = ET.Element('departments')
    data = json.load(open(readFile,encoding='utf-8-sig'))
    for i in data:
        uniName = i['university_name']
        uType = i['uType']
        items = i['items'][0]
        university = ET.SubElement(root,'university', {'name':uniName,'uType':uType})
        faculty = items['faculty']
        departments = items['departments']
        for j in range(len(departments)):
            item = ET.SubElement(university ,'item',{'id':departments[j]['id'],'faculty':faculty})
            name = ET.SubElement(item,'name',{'lang':departments[j]['lang'],'second':departments[j]['second']})
            name.text = departments[j]['name']
            period = ET.SubElement(item,'period')
            period.text = departments[j]['period']
            quota = ET.SubElement(item,'quota',{'spec':departments[j]['spec']})
            quota.text = departments[j]['quota']
            field = ET.SubElement(item,'field')
            field.text = departments[j]['field']
            last_min_score = ET.SubElement(item,'last_min_score',{'order':departments[j]['order']})
            last_min_score.text = departments[j]['last_min_score']
            grant = ET.SubElement(item,"grant")
            grant.text =departments[j]['grant']  
    tree = ET.ElementTree(root)
    tree.write(writeFile,encoding="utf-8",xml_declaration=True)

def CSVtoJSON(readFile, writeFile):
    with open(readFile, "r", encoding="utf-8", errors="ignore") as f:
        file = csv.reader(f, delimiter=";")
        next(file)  
        """
        Created by EBB Hierarchy :

            FinalJson []
                -->University Dictionary
                        *name :
                        *uType:
                        *items []
                            -->
                                *faculty :
                                *departments []
                                    --> Body dictionary    """
        finalJson = []
        university = {}
        items = []
        dictionary_item = {}
        departments = []
        uniname = ""
        for row in file:
            
            if  uniname!=row[1] and uniname!="":
                dictionary_item['faculty'] = row[2]
                dictionary_item['departments'] = departments
                items.append(dictionary_item)
                university['items'] = items
                finalJson.append(university)
                university = {}
                items = []
                dictionary_item = {}
                departments = []
                uniname = row[1]
            
            university['uType'] = row[0]
            university['name'] = row[1]
            uniname = row[1]  
            body = {}
            body['id'] = row[3]
            body['name'] = row[4]
            body['lang'] = row[5]
            body['second'] = row[6]
            body['period'] = row[8]
            body['spec'] = row[11]
            body['quota'] = row[10]
            body['field'] = row[9]
            body['order'] = row[12]
            body['last_min_order'] = row[13]
            body['grant'] = row[7]
            departments.append(body)
        
        dictionary_item['faculty'] = row[2]
        dictionary_item['departments'] = departments
        items.append(dictionary_item)
        university['items'] = items
        finalJson.append(university)

    f.close()
    with open(writeFile, 'w',encoding="utf-8") as f:
        json.dump(finalJson, f ,ensure_ascii=False)
    f.close()

def JSONtoCSV(readFile,writeFile):

    data = json.load(open(readFile,encoding='utf-8-sig') ) 
    outputFile = open(writeFile, 'w') #load csv file
    output = csv.writer(outputFile, delimiter=';', quoting=csv.QUOTE_MINIMAL)
    output.writerow(["ÜNİVERSİTE_TÜRÜ","ÜNİVERSİTE","FAKÜLTE","PROGRAM_KODU","PROGRAM","DİL","ÖĞRENİM_TÜRÜ","BURS","ÖĞRENİM_SÜRESİ","PUAN_TÜRÜ","KONTENJAN","OKUL_BİRİNCİSİ_KONTENJANI","GEÇEN_YIL_MİN_SIRALAMA","GEÇEN_YIL_MİN_PUAN"])
    for i in data:
        uniName = i['university_name']
        uType = i['uType']
        items = i['items'][0]
        faculty = items['faculty']
        departments = items['departments']
        line = "%s#%s#%s#%s#%s#%s#%s#%s#%s#%s#%s#%s#%s#%s"
        for j in range(len(departments)):
            output.writerow((line % (uType,uniName,faculty,departments[j]['id'],departments[j]['name'],departments[j]['lang'],departments[j]['second'],departments[j]['grant'], departments[j]['period'],departments[j]['field'],departments[j]['quota'],departments[j]['spec'],departments[j]['order'],departments[j]['last_min_score'])).split("#"))

def Validation(readFile,xsdFile):
    openXML = etree.parse(readFile)
    validator = etree.XMLSchema(file = xsdFile)
    checkResult =validator.validate(openXML)
    print(checkResult)



if __name__ == "__main__":

    if len(sys.argv)<4:
        print("error")
    else:
       # print("(1=CSV to XML, 2=XML to CSV, 3=XML to JSON, 4=JSON to XML, 5=CSV to JSON, 6=JSON to CSV,7=XML validates with XSD)")
        readFile = sys.argv[1].strip()
        writeFile = sys.argv[2].strip()
        choose = sys.argv[3].strip()
        try:
            if  choose =="1":
                CSVtoXML(readFile,writeFile)
            elif choose == "2":
                XMLtoCSV(readFile,writeFile)
            elif choose =="3":
                XMLtoJSON(readFile,writeFile)
            elif choose =="4":
                JSONtoXML(readFile,writeFile)
            elif choose =="5":
                CSVtoJSON(readFile,writeFile)
            elif choose =="6":
                JSONtoCSV(readFile,writeFile)
            elif choose =="7":
                Validation(readFile,writeFile)
            else:
                print(choose)
        except :
            print("Not integer")
        
""" The functions are given in a sequential order. """