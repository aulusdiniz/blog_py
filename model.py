import web, datetime

# you need to have the mysql configured.
db = web.database(dbn='mysql', db='blog', user='root', passwd='123456')

def get_posts():
    return db.select('entries', order='id DESC')

def get_post(id):
    try:
        return db.select('entries', where='id=$id', vars=locals())[0]
    except IndexError:
        return None

def new_post(title, text, userid):
    db.insert('entries', title=title, content=text, posted_on=datetime.datetime.utcnow(), posted_by_user=userid)

def del_post(id):
    db.delete('entries', where="id=$id", vars=locals())

def update_post(id, title, text):
    db.update('entries', where="id=$id", vars=locals(),
        title=title, content=text)

def get_logins():
    return db.select('logins', order='id DESC')

def get_login(user):
    try:
        return db.select('logins', where='user=$user', vars=locals())[0]
    except IndexError:
        return None

def new_login(user, passwd):
    db.insert('logins', user=user, passwd=passwd)
