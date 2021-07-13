
from database import check_user, create_connection

conn = create_connection(r"mypasswords.db")

if len(check_user(conn)) > 0:
    print("proceed to login")

else:
    print("register")
