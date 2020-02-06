import os
import shutil
from bs4 import BeautifulSoup
import csv
import requests
import zipfile
from datetime import datetime as dt, timedelta



def update_result():
    days_of_draw = [1,3,5]
    f = open('lastupdate.txt', 'r')
    load = f.read()
    f.close()
    load = dt.strptime(load, '%Y-%m-%d')
    date_read = load.date()
    day_read = load.isoweekday()
    now_date = dt.now().date()
    now_time = dt.now().time()
    now = dt.now()
    day_now = now.isoweekday()

    while True:
        if (now_date.isoweekday() in days_of_draw) and (now_time.hour >= 20) and (now_date != date_read):
            gerar_db(now_date)
            break
        else:
            for x in range(1,5):
                aux = (now_date - timedelta(days=x))
                aux_day_week = aux.isoweekday()
                if ((aux_day_week in days_of_draw) and (aux != date_read)):
                    gerar_db(aux)
                    break
            break


def gerar_db(date= dt.today()):

    url = 'http://www1.caixa.gov.br/loterias/_arquivos/loterias/D_lotfac.zip'
    target_path = 'D_lotfac.zip'

    response = requests.get(url, stream=True)
    handle = open(target_path, "wb")
    for chunk in response.iter_content(chunk_size=512):
        if chunk:  # filter out keep-alive new chunks
            handle.write(chunk)
    handle.close()
    with zipfile.ZipFile(target_path) as zf:
        zf.extractall()

    # Creating paths
    base_path = os.getcwd()
    csv_path = base_path.replace('lotto','lotto_files/csv')
    html_path = base_path.replace('lotto','lotto_files/html')



    html_file = html_path + '/' + 'D_LOTFAC.HTM'
    csv_file = open('{csv_path}/lotofacil.csv'.format(csv_path=csv_path),'w')


    def dwn_unzip_func():
        # checking for zip file and deleting if exists
        if os.path.isfile(lotto_zip) == True:
            print("Deleting previous vertion of " + lotto_zip + "\n")
            os.remove(lotto_zip)

        # checking for data directory and deleting if exists
        if os.path.isdir("data") == True:
            shutil.rmtree("data")

        # downloading file using wget
        # should figure out how via python
        os.system("wget {url}".format(url = url))

        # unziping data to data directory
        # should figure out using python
        os.system("unzip {zip} -d data".format(zip = lotto_zip))


    def html_parse_func():
        # Parse the html file
        html = open(html_file,'r')
        soup = BeautifulSoup(html, 'html.parser')

        html_list = []
        for i in soup.find_all('td'):
            line = str(i)
            if '<td rowspan="' in line:
                html_list.append(line)

        raw_text = soup.get_text()

        html_dict = {}
        x = 0
        for i in raw_text.split():
            x = x + 1
            tmp_dict = {x:i}
            html_dict.update(tmp_dict)


        date_list = []
        for i in html_dict:
            v = html_dict[i]
            if '/' in v:
                date_list.append(i)


        master_list = []
        for d in date_list:
            sd = int(d) -1
            ed = sd + 31
            tmp_list = []
            for d in range(sd,ed):
                if (d <= 10) or (d>= 25):
                    v = html_dict[d]
                    tmp_list.append(v.strip())
            master_list.append(tmp_list)

        def date_func(i):
            nw = i.split('/')[2] + '-' + i.split('/')[1] + '-' + i.split('/')[0]
            return nw

        def num_func(i):
            if 'Valor' in i:
                return 1
            else:
                return i

        list_estados = ["AC","AL","AP","AM","BA","CE","DF","ES","GO","MA","MT","MS","MG","PA","PB","PR","PE","PI","RJ","RN","RS","RO","RR","SC","SP","SE","TO",'XX']
        writer = csv.writer(csv_file, delimiter=',', quoting=csv.QUOTE_MINIMAL)
        writer.writerow(['game','date','1','2','3','4','5','6','7','8','9','10','11','12','13','14','15','P15','P14','P13','P12','P11'])
        for i in master_list:
            num = int(num_func(i[0]))
            date = date_func(i[1])
            n1 = i[2].strip('\n')
            n2 = i[3].strip('\n')
            n3 = i[4].strip('\n')
            n4 = i[5].strip('\n')
            n5 = i[6].strip('\n')
            n6 = i[7].strip('\n')
            n7 = i[8].strip('\n')
            n8 = i[9].strip('\n')
            n9 = i[10].strip('\n')
            n10 = i[11].strip('\n')
            n11 = i[12].strip('\n')
            n12 = i[13].strip('\n')
            n13 = i[14].strip('\n')
            n14 = i[15].strip('\n')
            n15 = i[16].strip('\n')
            if ((i[19] in list_estados) or (i[18] == '0')):
                count = 24
            elif i[21] in list_estados:
                count = 26
            else:
                count = 25
            p15 = i[count].strip('\n')
            p14 = i[(count + 1)].strip('\n')
            p13 = i[(count + 2)].strip('\n')
            p12 = i[(count + 3)].strip('\n')
            p11 = i[(count + 4)].strip('\n')
            #print num,date,n1,n2,n3,n4,n5,n6,n7,n8,n9,n10,n11,n12,n13,n14,n15
            writer.writerow([int(num),date,int(n1),int(n2),int(n3),int(n4),int(n5),int(n6),int(n7),
                             int(n8),int(n9),int(n10),int(n11),int(n12),int(n13),int(n14),int(n15),p15,p14,
                             p13,p12,p11])



    # calling parse function
    html_parse_func()
    f = open('lastupdate.txt', 'w')
    f.write(date.strftime('%Y-%m-%d'))