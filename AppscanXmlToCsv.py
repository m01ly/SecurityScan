#appscan的报告格式只有xml的，不利于交流，使用该脚本实现xml格式转为csv
import csv, xmltodict
import os,time
rowlist=[]
def get_xml_files():
    xml_file_array = []
    files_in_dir = os.listdir(".")
    found_xml_count = 0
    for file in files_in_dir:
        if file.lower().find(".xml") > -1:
            found_xml_count += 1
            xml_file_array.append(file)
    if found_xml_count == 0:
        print
        "[-] Error - no .xml files found in current directory! Quiting..."
    else:
        print
        "[+] Found " + str(found_xml_count) + " xml files to parse"
        return xml_file_array
def getURL(ref):
    for url_item in xml['xml-report']['url-group']['item']:
        if(url_item['@id'] == ref):
            return(url_item['name'])

def getIssueType(ref):
    for issue_item in xml['xml-report']['issue-type-group']['item']:
        if(issue_item['@id'] == ref):
            return(issue_item['name'])

def getEntity(ref):
    for ent_item in xml['xml-report']['entity-group']['item']:
        if(ent_item['@id'] == ref):
            return(ent_item['entity-type'])

def getIssueInfoResponse(path):
    if 'issue-information' in path:
        return(path['issue-information']['testResponseChunk'])

def getIssueInfoTraffic(path):
    if 'issue-information' in path:
        return(path['issue-information']['test-http-traffic'])

def getRemediation(ref):
    for issue_item in xml['xml-report']['remediation-group']['item']:
        if(issue_item['@id'] == ref):
            return(issue_item['name'])
def writetoscv(content):
    st = time.strftime("%Y%m%d", time.localtime())
    # 以写的方式打开文件，如果文件不存在，就会自动创建
    csvReportPath = "appscanresult" + st + ".csv"
    with open(csvReportPath,'w',encoding='utf-8',newline='')as csvfile:
        writer = csv.writer(csvfile)
        # ADD HEADER
        writer.writerow(["target",
            "issue-type", "severity", "cvss-score",
            "url", "entity-type",
            "remediation", "reasoning"])
        writer.writerows(content)
if __name__ == '__main__':
    xml_file_list = get_xml_files()
    for xml_filedir in xml_file_list:
        print("[+] Working on " + xml_filedir + "...")
        xmlfile = open(xml_filedir,encoding='utf-8')
        xml = xmltodict.parse(xmlfile.read())
        targeturl=xml["xml-report"]["scan-configuration"]["starting-url"]
    #FOR EACH VULNERABILITY
    for vul in xml["xml-report"]["issue-group"]["item"]:
        # EXTRACT VULNERABILITY DETAILS
        csv_line = [targeturl,
                getIssueType(vul["issue-type"]["ref"]),
                vul["severity"],
                vul["cvss-score"], getURL(vul["url"]["ref"]),
                getEntity(vul['entity']['ref']),
                getRemediation(vul['remediation']['ref']), vul['variant-group']['item']['reasoning']['#text']]
        # ADD A NEW ROW TO CSV FILE
        rowlist.append(csv_line)
        # CREATE CSV FILE
        writetoscv(rowlist)

