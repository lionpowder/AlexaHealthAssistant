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
    # hey Hannah, feel free to modify this function.

    # with conn.cursor() as cur:
        #sql = "insert into `Patient` (`name`, `age`, `gender`, `pregnancy`) " + \
        #      "values (%s, %s, %s, %s)"

        #cur.execute(sql, (name, age, gender, 1 if pregnancy else 0))
    #conn.commit()
    return None


def get_user_info(user_name):

    # Hey, Hannah, below is the mock code for getting the user info from DB.
    # If you prefer, you can fill in the API here.
    # basically, return the user_age, gender etc if the user_name exist in DB
    # otherwise just return {'user_name':user_name', 'status':'not_found'}

    use_mock_user_profile = True
    if use_mock_user_profile:
        return {
            'user_name': user_name,
            'user_age': 24,
            'gender': "M",
            'pregnancy': False
        }
    else:
        return {
            'user_name': user_name,
            'status': 'not_found'
        }


def get_drug_side_effects(user_info, drug):

    # Hey, Hsuan-Heng, if you prefer, you can fill in the API here.

    return "the side effect of {} is bla bla bla".format(drug)