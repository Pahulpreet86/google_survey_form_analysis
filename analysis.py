import pandas as pd
import pickle



#Note all question in the survey should end with "?"
def question_list(df):
#find questions ---------------
    columns=list(df.columns.unique())
    questions=[]
    for column_name in columns:
        if column_name.find("?")!=-1:
            questions.append(column_name)
    return questions


def overall(df):
    questions=question_list(df)
    
#map options
    overall_wise={}
    for question in questions:
        string=""
        for option in df[question]:
            string=string+str(option)+","
        string=string.replace(", " , ",").split(",")
        
        count={}
        for words in string:
            if words in count:
                count[words]=count[words]+1
            else:
                count[words]=1
                
        count.pop("")#redundant
        
        for key in count.keys():
            count[key]=round((count[key]/len(string)),2)
        overall_wise[question]=count
    
    with open("overall.pkl", 'wb') as f:
        pickle.dump(overall_wise, f)
    

def region_wise(df):
    questions=question_list(df)
    region=list(df.groupby('Region').groups.keys())
#map options
    region_wise={}
    for state in region:
        overall={}
        df_region=df[df["Region"]==state]
        for question in questions:
            string=""
            for option in df_region[question]:
                string=string+str(option)+","
            string=string.replace(", " , ",").split(",")
        
            count={}
            for words in string:
                if words in count:
                    count[words]=count[words]+1
                else:
                    count[words]=1
                
            count.pop("")#redundant
            for key in count.keys():
                count[key]=round((count[key]/len(string)),2)
            overall[question]=count
        region_wise[state]=overall
    
    with open("statwise.pkl", 'wb') as f:
        pickle.dump(region_wise, f)


def qualification_wise(df):
    questions=question_list(df)
    qualifications=list(df.groupby('Qualification').groups.keys())
#map options
    qualification_wise={}
    for qualification in qualifications:
        overall={}
        df_qualification=df[df["Qualification"]==qualification]
        for question in questions:
            string=""
            for option in df_qualification[question]:
                string=string+str(option)+","
            string=string.replace(", " , ",").split(",")
        
            count={}
            for words in string:
                if words in count:
                    count[words]=count[words]+1
                else:
                    count[words]=1
                
            count.pop("")#redundant
            for key in count.keys():
                count[key]=round((count[key]/len(string)),2)
            overall[question]=count
        qualification_wise[qualification]=overall
    
    with open("qualificationwise.pkl", 'wb') as f:
        pickle.dump(qualification_wise, f)


def analysis(df):
    overall(df)
    qualification_wise(df)
    region_wise(df)