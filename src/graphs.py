import matplotlib
import matplotlib.pyplot as plt
import numpy as np
from numpy import arange
import urllib
import csv

matplotlib.use('Agg')
data = csv.reader(open('traffic_accident.csv'))
header=data.next()
data=list(data)
#First Graph - How many accidents happe in one month - Histogram
#Second Graph - Accident type frequency - Histogram
#Third Graph - light condition and road geometry - Scatter plot
#Forth Graph - Speed Zone - Pie Chart
#Fifth Graph - Person (not)injuried and (not)killed

Month_dict={}#First Graph,store each month;s number of accident
Type_dict={}#Second Graph,store the type of car accident
Light_dict={}#Third Graph
Road_dict={}#Third Graph
Speed_dict={}
Injure_dict={}#Store the number of people injured in each speed zone
death_dict={}#Number of people killed by traffic accident
month=''
for num in data:
  n=0
  while(n<len(header)):
    if header[n]=='ACCIDENTDATE' :
      month=num[n].replace("/","")
      if month[-1]=='5': #Data for 2015
        if month[-6]=='0': #Jan to Sep
          if month[-5] in Month_dict.keys():
            Month_dict[month[-5]]+=1
          else:
            Month_dict[month[-5]]=1
        else: # Oct to Dec
          i = month[-6] + month[-5]
          if i in Month_dict.keys():
            Month_dict[i]+=1
          else:
            Month_dict[i]=1
    if header[n]=='Accident Type Desc':
      if(num[n] in Type_dict.keys()):
        Type_dict[num[n]]+=1
      else:
        Type_dict[num[n]]=1
    if header[n]=='Light Condition Desc':
      if(num[n] in Light_dict.keys()):
        Light_dict[num[n]]+=1
      else:
        Light_dict[num[n]]=1
    if header[n]=='Road Geometry Desc':
      if(num[n] in Road_dict.keys()):
           Road_dict[num[n]]+=1
      else:
           Road_dict[num[n]]=1
    if header[n]== 'SPEED_ZONE':
      if(num[n] in Speed_dict.keys()):
           Speed_dict[num[n]]+=1
      else:
           Speed_dict[num[n]]=1
      if(num[n] in Injure_dict.keys()):
          Injure_dict[num[n]].append(num[20])
      else:
          Injure_dict[num[n]]=[]
      if(num[n] in death_dict.keys()):
          death_dict[num[n]].append(num[21])
      else:
          death_dict[num[n]]=[]
    n+=1

#First Graph - Histogram - in 2015, each month's accident
Month = ['Jan','Feb','Mar','Apr','May','Jun',
         'Jul','Aug','Sep','Oct','Nov','Dec']
Value=[]
n=1
while(n<=12):
    Value.append(Month_dict[str(n)])
    n+=1

plt.bar(arange(len(Value)),Value,color='g')
plt.xticks(arange(len(Month)),Month, rotation=30)
plt.title("Number Of Accidents In Each Month\nIn 2015\n",fontsize=15, ha="center",color='g' )

plt.show()

#Second Graph - Histogram
Type=[]
Value=[]
for keys in Type_dict.keys():
  Type.append(keys)
for value in Type:
  Value.append(Type_dict[value])

plt.bar(arange(len(Value)),Value,width=0.8)
plt.xticks(arange(len(Type)),Type, rotation=30)
plt.show()

#Third - Pie chart - Speed Zone
Speed=[]
Value=[]
for keys in Speed_dict.keys():
  Speed.append(keys)
for value in Speed:
  Value.append(Speed_dict[value])
cmap = plt.cm.prism
colors = cmap(np.linspace(0, 1, len(Value)))
plt.figure(figsize=(7,7))
plt.pie(Value,explode=None,labels=Speed,colors=colors)
plt.axis('equal')
plt.show()

#Forth - Line chart - Connection between road geometry and light conditions
#Print Histogram for Road Geometry First
Road = []
Value=[]
for keys in Road_dict.keys():
  Road.append(keys)
for value in Road:
  Value.append(Road_dict[value])

plt.barh(arange(len(Value)),Value)
plt.yticks(arange(len(Road)),Road)
plt.show()

Light=[]
for keys in Light_dict.keys():
    Light.append(keys)

#For each consition,show each of their connection with light condition
Road=['Cross intersection','Not at intersection','T intersection']
Cross_dict={}
Not_dict={}
T_dict={}

for num in data:
    if num[25]=='Cross intersection':
        if num[15] in Cross_dict.keys():
            Cross_dict[num[15]]+=1
        else:
            Cross_dict[num[15]]=1
    if num[25]=='Not at intersection':
        if num[15] in Not_dict.keys():
            Not_dict[num[15]]+=1
        else:
            Not_dict[num[15]]=1
    if num[25] == 'T intersection':
        if num[15] in T_dict.keys():
            T_dict[num[15]]+=1
        else:
            T_dict[num[15]]=1

Cross=[]
Not=[]
T=[]
for n in Light:
    Cross.append(Cross_dict[n])
    Not.append(Not_dict[n])
    T.append(T_dict[n])

plt.plot(Cross,linewidth=3.0,label='Cross intersection')
plt.plot(Not,'g-',linewidth=3.0,label='Not at intersection')
plt.plot(T,'r-',linewidth=3.0,label='T intersection')
plt.legend()
plt.xticks(arange(len(Light)),Light, rotation=30)
plt.ylabel("Number of accidents")
plt.grid(True)
plt.show()


#Fifth - Line chart- Connection between number of people injuried and speed zone
Speed = map(int, Speed)
Speed.sort()#Sort speed zone into ascending order

people=[]#Number of people injured
#First print average number of people injuried in each speed zone
for i in Speed:
    num=0
    for k in Injure_dict[str(i)]:
        num+=int(k)
    people.append(num)


plt.xticks(range(len(Speed)),Speed,rotation='0' )
plt.plot(people)
plt.title("Number Of People Injured In Different Speed Zone\nFrom 2015 to 2016\n",
          fontsize=15, ha="center",color='g')
plt.grid(True)
plt.show()

#Then print the maximum number of people get injured in each speed zone
maxi=[]#Maximum number of people injured
for i in Speed:
    num=0
    for k in Injure_dict[str(i)]:
      if int(k) > num:
          num=int(k)
    maxi.append(num)

plt.xticks(range(len(Speed)),Speed,rotation='0' )
plt.plot(maxi)
plt.grid(True)
plt.title("Maximum Number Of People Injured In Different Speed Zone\nFrom 2015 to 2016\n",
          fontsize=15, ha="center",color='g')
plt.show()

#Number of people death in each speed zone
death=[]
for i in Speed:
    num=0
    for k in death_dict[str(i)]:
        num+=int(k)
    death.append(num)

plt.xticks(range(len(Speed)),Speed,rotation='0' )
plt.plot(death)
plt.grid(True)
plt.title("Number Of People Killed Under Different Speed Zone\nFrom 2015 to 2016\n",
          fontsize=15, ha="center",color='r')
plt.show()