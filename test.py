import pymysql
  
def mysqlconnect():
    # To connect MySQL database
    conn = pymysql.connect(
            host ="awseb-e-qc6idp2hcz-stack-awsebrdsdatabase-zkebuinx4tlr.cq087g9hv6sl.us-east-2.rds.amazonaws.com",
            user ="AnjaliK",
            passwd ="cs3481234!",
            db='ebdb'
        )
      
    cur = conn.cursor()
    cur.execute("select * from timezone;")
    output = cur.fetchall()
    print(output)
      
    # To close the connection
    conn.close()
  
# Driver Code
if __name__ == "__main__" :
    mysqlconnect()