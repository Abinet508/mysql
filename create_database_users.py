import mysql.connector
import sys, csv, random, string, argparse
class DatabaseUsers():
    def __init__(self, args):
        if len(args) == 0:
            print("No arguments passed")
            sys.exit(1)
        elif len(args) < 5 or len(args) > 5:
            print("Invalid number of arguments")
            sys.exit(1)
        else:
            self.db_host=args["db_host"]
            self.db_port=args["db_port"]
            self.admin_user=args["admin_user"]
            self.admin_pass=args["admin_pass"]
            self.list_of_usernamesFile=args["list_of_usernamesFile"]
            print(self.db_host, self.db_port, self.admin_user, self.admin_pass, self.list_of_usernamesFile)
            print(self.db_host, self.db_port, self.admin_user, self.admin_pass, self.list_of_usernamesFile)
            self.list_of_usernames=[]
            self.Connection=mysql.connector.connect(host=self.db_host, port=self.db_port, user=self.admin_user, passwd=self.admin_pass)
            self.cursor=self.Connection.cursor()
        
            
    # Read the csv file
    def read_csv_file(self):
        with open(f"{self.list_of_usernamesFile}", "r") as f:
            reader = csv.reader(f)
            for row in reader:
                self.list_of_usernames.append(row[0])
    
    # Create a cursor
    def create_cursor(self):
        self.cursor=self.connection.cursor()

    # Create a database
    def create_database(self):    
        return self.cursor.execute("CREATE DATABASE {}".format(self.db_host))

   # Generate a random password
    def generate_random_password(self):
        return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(10))

    # Create a user
    def create_user(self):
        for username in self.list_of_usernames:
            self.cursor.execute("CREATE USER '{}'@'{}' IDENTIFIED BY '{}'".format(username,self.db_host, self.generate_random_password()))
            self.cursor.execute("GRANT ALL PRIVILEGES ON *.* TO '{}'@'{}'".format(username,self.db_host))
            self.cursor.execute("FLUSH PRIVILEGES")

    # Close the cursor  
    def close_cursor(self):
        self.cursor.close()

    # Close the connection
    def close_connection(self):
        self.Connection.close()
       
# Path: create_database_users.py
if __name__ == "__main__":
    MyArgs = argparse.ArgumentParser()
    MyArgs.add_argument("--db_host", help="database host")
    MyArgs.add_argument("--db_port",help="database port")
    MyArgs.add_argument("--admin_user",help="admin user")
    MyArgs.add_argument("--admin_pass",help="admin password")
    MyArgs.add_argument("--list_of_usernamesFile",help="list of usernames file")

    Myobject=DatabaseUsers(dict((MyArgs.parse_args()._get_kwargs())))
    Myobject.read_csv_file()
    Myobject.create_user()
    Myobject.close_cursor()
    Myobject.close_connection()
