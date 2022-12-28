#%%
from googletrans import Translator
import requests
import pandas as pd
import re
from datetime import datetime
import threading

translator = Translator()



main_data=[]

page=14
def germen_to_english(german):
    clean_text = re.sub(r"<.*>",'',german)
    return translator.translate(clean_text, dest='en', src='auto').text


u = 'https://www.kununu.com/middlewares/profiles/de/catalent-pharma-solutions1/e3c23200-3c1a-4ca0-8e28-adc7d813cb40/reviews?reviewType=employees&urlParams=sort%3Dnewest&sort=newest&page='
def t(u,page_num):
    url=u+str(page_num)
    print(page_num)
    data__=requests.get(url).json()



    reviews_=data__['reviews']
    for r in reviews_:
        
        data={}
        data['ratings']=''
        data['Atributes']=''
        data['Discription']=''
        try:
            data['Title']=germen_to_english(r.get('title',""))
        except:
            data['Title']=r.get('title',"")

        data['Score']=r.get('score',"")
        data['Company Name']=r['company']['name']
        data['City']=r['company'] ['location']['city']
        data['Country']=r['company']['location']
        data['State']=r['company'] ['location']['state']
        data['Area']=r['department']
        data['Recommended']=r['recommended']
        data['Position']=r['position']
        temp=r['createdAt'].split("T")[0]
        tem2=datetime.strptime(temp,"%Y-%m-%d")
        data['Month']=tem2.strftime("%B")
        data['Year']=tem2.year
        


                        
        data['type']=r.get('type',"") 
        arr = []
        for rating in r['ratings']:
            try:

                data[rating['id']+"_text"]=germen_to_english(rating.get('text',''))
            except:
                data[rating['id']+"_text"]=rating.get('text','')
            data['ratings']+=rating['id']+":"+str(rating['score'])+"\n"
            arr.append(rating['id'])
            # data['Atributes']+=rating['id']+",\n"
        data['ratings'] = data['ratings'].strip()
        data['Atributes'] = ",\n".join(arr)
            
        for text in r['texts']:
            try:
                data['Discription']+=text['id'].replace("positive","I like the employer").replace("negative","I think it's bad about the employer").replace("suggestion","suggestions for improvement")+"\n"+germen_to_english(text['text'])+'\n'
            except:
                data['Discription']+=text['id']+"\n"+text['text']+'\n'

            



        main_data.append(data)


th = []
for x in range(1,page+1):

    thread = threading.Thread(target=t,args=(u,x,))
    thread.start()
    th.append(thread)


for c in th:
    c.join()



#%%
df=pd.DataFrame(main_data)
df.to_excel("Data.xlsx",index=False)


# %%
