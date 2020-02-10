import os
from bs4 import BeautifulSoup
import csv
import requests
import zipfile



def update_result(link):

    url = link
    target_path = '/home/pgarcias01/mysite/D_lotfac.zip'
    response = requests.get(url, stream=True)
    handle = open(target_path, "wb")
    for chunk in response.iter_content(chunk_size=512):
        if chunk:  # filter out keep-alive new chunks
            handle.write(chunk)
    handle.close()
    with zipfile.ZipFile(target_path) as zf:
        zf.extractall('/home/pgarcias01/mysite/')

    # Creating paths
    base_path = os.getcwd()
    csv_path = base_path.replace('lotto','/home/pgarcias01/mysite/lotto_files/csv')
    html_path = base_path.replace('lotto','/home/pgarcias01/mysite/lotto_files/html')



    html_file = '/home/pgarcias01/mysite/d_lotfac.htm'
    csv_file = open('/home/pgarcias01/mysite/lotofacil.csv'.format(csv_path=csv_path),'w')


    def html_parse_func():
        # Parse the html file
        with open(html_file, 'rb') as html:
            soup = BeautifulSoup(html, 'html.parser', from_encoding='latin-1')

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
            ed = sd + 34
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
            count = 19
            while True:
                if i[18] == '0':
                    count += 4
                    break
                if i[count] in list_estados:
                    count = count+5
                    break
                count += 1
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
