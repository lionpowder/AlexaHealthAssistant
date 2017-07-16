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
    # with conn.cursor() as cur:
        #sql = "insert into `Patient` (`name`, `age`, `gender`, `pregnancy`) " + \
        #      "values (%s, %s, %s, %s)"

        #cur.execute(sql, (name, age, gender, 1 if pregnancy else 0))
    #conn.commit()
    return None


def get_user_info(user_name):
    return {
        'user_name': user_name,
        'user_age': 24,
        'gender': "M",
        'pregnancy': False
    }


def get_drug_side_effects(user_info, drug):

    # Hey, Hsuan-Heng, if you prefer, you can fill in the API here.

    return "the side effect of {} is bla bla bla".format(drug)