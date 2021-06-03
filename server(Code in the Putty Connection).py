from flask import Flask
from flask import request
from flaskext.mysql import MySQL

app = Flask(__name__)

mysql = MySQL()
app.config['MYSQL_DATABASE_USER'] = 'admin'
app.config['MYSQL_DATABASE_PASSWORD'] = 'piuser123'
app.config['MYSQL_DATABASE_DB'] = 'datas'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)
conn = mysql.connect()

@app.route('/', methods=['GET'])
def welcome():
    return welcome()

@app.route('/home', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        return handle_post()
    else:
        return get_last_data()

@app.route('/refresh', methods=['GET'])
def refresh():
        return refresh_datas()

def welcome():
    return "<h2 style='text-align:center;'>Welcome to IoT Server...</h2>"

def handle_post():
    data = request.get_data()
    #Splite data
    tmp = str(data).split(':')[1][1:]
    hmd = str(data).split(':')[2][1:]
    cmx = str(data).split(':')[3][1:]
    #trim datas
    tmpIndex = tmp.index("'")
    hmdIndex = hmd.index("'")
    cmxIndex = cmx.index("'")
    #values ready
    newTmp = tmp[:tmpIndex]
    newHmd = hmd[:hmdIndex]
    newCmx = cmx[:cmxIndex]

    print(newTmp, newHmd, newCmx)
    insert_data(int(newTmp), int(newHmd), int(newCmx))

    return request.data

def insert_data(tmp, hmd, cmx):
    sql = "INSERT INTO data(data_tmp, data_hmd, data_mq9) VALUES({}, {}, {})".format(tmp, hmd, cmx)
    cursor = conn.cursor()
    cursor.execute(sql)
    conn.commit()
    print("Data Inserted !")


def get_last_data():
    sql = "SELECT * FROM data ORDER BY data_id DESC"
    cursor = conn.cursor()
    cursor.execute(sql)
    datas = cursor.fetchall()
    return "<div style='width:100%; text-align:center; margin-top:100px;'><h2>Temperature : " + str(datas[0][1]) + "C </h2><h2>Humidity : " + str(datas[0][2]) + "% </h2><h2>Carbonmonoxide : " + str(datas[0][3]) + "% </h2></div>"

def refresh_datas():
    sql = "SELECT * FROM data ORDER BY data_id DESC"
    cursor = conn.cursor()
    cursor.execute(sql)
    datas = cursor.fetchall()
    return str(datas[0][1]) + "," + str(datas[0][2]) + "," + str(datas[0][3])

