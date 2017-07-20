import pymysql
import logging

#rds settings
rds_host = "telehealthdb.c3cunddkbk4y.us-east-2.rds.amazonaws.com"
rds_port = 3306
name = 'sa'
password = '12345678'
db_name = 'telehealthdb'

log = logging.getLogger('dbUtil')
log.setLevel(logging.DEBUG)

try:
    conn = pymysql.connect(
        host = rds_host,
        port = rds_port,
        user = name,
        password = password,
        db=db_name,
        connect_timeout=5)

except:
    log.error("ERROR: Unexpected error: Could not connect to MySql instance.")
    

def insert_patient(user_info):
    with conn.cursor() as cur:
        sql = "insert into `Patient` (`name`, `age`, `gender`, `pregnancy`) " + \
              "values (%s, %s, %s, %s)"

        cur.execute(sql, (user_info['user_name'], user_info['user_age'], "F" if user_info['gender'] == "female" else "M",
                           1 if user_info['pregnancy'] else 0))
    conn.commit()
    return None


def get_user_info(user_name):
    with conn.cursor() as cur:
        sql = "select * from Patient where " + \
              "name = %s"

        cur.execute(sql, user_name)
        row = cur.fetchone()
        #rows = cur.fetchall()
        
    conn.commit()        
    
    # (Need Modification) If having multiple names, get the first one
    #for row in rows:
    #    print(row[1])    

    use_mock_user_profile = True
    if use_mock_user_profile:
        return {
            'user_name': user_name,
            'user_age': row[2],
            'gender': "female" if row[3].upper() == "F" else "male",
            'pregnancy': True if row[4] == 1 else False
        }
    else:
        return {
            'user_name': user_name,
            'status': 'not_found'
        }

def get_disease_symptom_name(queryName, isDisease): # queryName could either be disease or symptom; isDisease: boolean
    with conn.cursor() as cur:
        sql = "select symptomName from DiseaseSymptom inner join Symptom on Symptom.symptomId = DiseaseSymptom.symptomId"+\
               " where DiseaseSymptom.diseaseId in (" +\
               "select Disease.diseaseId from Disease left join DiseaseName on Disease.diseaseId = DiseaseName.diseaseId" +\
               " where diseaseName = %s)" if isDisease else "select diseaseName from Disease left join DiseaseName on Disease.diseaseId = DiseaseName.diseaseId" +\
                " where Disease.diseaseId in (" +\
                "select diseaseId from DiseaseSymptom inner join Symptom on Symptom.symptomId = DiseaseSymptom.symptomId" +\
                " where symtomName = %s) and DiseaseName.diseaseNameType = 'C'" 
                
        cur.execute(sql, queryName)
        #row = cur.fetchone()
        rows = cur.fetchall()
        
    conn.commit()  
    
    resultStr = ""
    for row in rows:
        resultStr += ("," if resultStr != "" else "") + row[0]
    
    return "The symptom(s) of {} is {}".format(queryName, resultStr) if isDisease else "The diseases(s) regarding {} is {}".format(queryName, resultStr)


def get_drug_side_effects(drug): # some have same drugName but different manufacturer / brand, which should lead to different side effects
    with conn.cursor() as cur:
        sql = "select distinct(description) from SideEffect where sideEffectId in (" +\
            "select sideEffectId from DrugName inner join DrugSideEffect on DrugSideEffect.drugId = DrugName.drugId "+\
            "where DrugName.drugName = %s)" # temporary select description, later on if data is complete should select SideEffectName instead
    
        cur.execute(sql, drug)
        rows = cur.fetchall()
        
    conn.commit()  
    
    resultStr = ""
    for row in rows:
        resultStr += ("," if resultStr != "" else "") + row[0]

    return "The side effect(s) of {} is {}".format(drug, resultStr)
