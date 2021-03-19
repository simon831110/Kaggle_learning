import stateee
import csv

state=[]
state_dic={}
with open('./state.csv','r') as f:
    lines = csv.reader(f)
    for i in lines:
        state.append(i)                 #(1,0)(1,1)(3,2)(3,3)
state_dic["IE_state"]=state[1][0]
state_dic["IE_num"]=state[1][1]
state_dic["Chrome_state"]=state[3][2]
state_dic["Chrome_num"]=state[3][3]



stateee.main(state_dic)
