import requests
import json
import pymysql
from bs4 import BeautifulSoup

conn=pymysql.connect(
    user='root',
    passwd='Myeddie0409!',
    host='localhost',
    db='cm'
)
cur= conn.cursor()
nums=[]
doctors=requests.get('https://www.cmcseoul.or.kr/api/doctor?deptCd=201&orderType=dept&fsexamflag=A').json()
for dc in doctors:
    nums.append(dc['drNo'])
doctors=[]
for num in nums:
    doctor=requests.get('https://www.cmcseoul.or.kr/api/doctor/201/'+num).json()
    name=doctor['drName']
    detail=doctor['doctorDetail']
    recordlist=detail['doctorRecordList']
    deptlist=doctor['doctorDept']
    
    education=[]
    career=[]
    activity=[]
    major=deptlist['nuSpecial']
    for record in recordlist:
        if record['recordTypeText']=='학력':
            education.append(record['recordContent'])
        elif record['recordTypeText']=='학회활동':
            activity.append(record['recordContent'])
        #elif record['recordTypeText']=='연구분야':
        #    major.append(record['recordContent'])
        else:
            career.append(record['recordContent'])
    if len(activity)==0:
        activity.append('학회활동 없음')
    if len(major)==0:
        major.append('연구분야 없음')
    thesislist=detail['doctorThesisList']
    thesis=[]
    for dic in thesislist:
        thesis.append(dic['title'])
    doctor=[]
    doctor.append(name)
    doctor.append('가톨릭성모병원')
    doctor.append(major)
    doctor.append(career)
    doctor.append(education)
    doctor.append(len(thesis))
    doctor.append(thesis)
    doctors.append(doctor)
tostrings=[]
tostring=[]
for doctor in doctors:
    tostring=[]
    for infos in doctor:
        if type(infos)==type(tostring):
           string=''
           for i in range(len(infos)):
               string+=infos[i]
               if i!=len(infos)-1:
                   string+=','
        else:
            string=infos
        tostring.append(string)
    #print(tostring)
    tostrings.append(tostring)
#for tostring in tostrings:
    #print(tostring)
doctor=tostrings[9]
for doctor in tostrings:
    cur.execute("INSERT INTO doctors VALUES (%s,%s,%s,%s,%s,%s,%s);",(doctor[0],doctor[1],doctor[2],doctor[3],doctor[4],doctor[5],doctor[6]))
conn.commit()
//침투시도
