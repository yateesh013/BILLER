import sqlite3 as s3

path="sales.db"

def default():
    file=s3.connect(path)
    f=file.cursor()
    query1=f'''create table if not exists sales([bill] text,[item] text,[quantity] int,[price] int,[type] text)'''
    query2=f'''create table if not exists info([item] text,[price] int)'''
    f.execute(query1)
    f.execute(query2)
    file.commit()
    file.close()


def save(my_list):
    file=s3.connect(path)
    f=file.cursor()
    for i in my_list:
        query=f'''insert into sales values("{i[0]}","{i[1]}","{i[2]}","{i[3]}","{i[4]}")'''
        f.execute(query)
        file.commit()
    file.close()     


def delete(mylist):
    file=s3.connect(path)
    f=file.cursor()
    query=f'''delete from sales where bill="{mylist[0][0]}"'''
    f.execute(query)
    file.commit()
    file.close()


def search(id):
    file=s3.connect(path)
    f=file.cursor()
    query=f'''select * from sales where bill="{id}"'''
    f.execute(query)
    op=f.fetchall()
    return op

def getdata(name):
    file=s3.connect(path)
    f=file.cursor()
    query=f'''select * from info where item="{name}"'''
    f.execute(query)
    op=f.fetchall()
    file.commit()
    file.close
    return op[0][1]


def calc():
    file=s3.connect(path)
    f=file.cursor()
    query=f'''select * from sales'''
    f.execute(query)
    op=f.fetchall()
    file.commit()
    file.close()
    cash=0
    upi=0
    for i in op:
        if i[4]=="CASH":
            cash+=i[3]
        else:
            upi+=i[3]
    
    return [cash,upi]

#default()
    

#edit_count("bonda",20)


#print(getdata("bonda",count=False))


#print(calc())


#save([["1","hello","36","588"],["2","hello","36","588"],["3","he","362","58"]])

#delete([["1","hello","36","588"],["2","hello","36","588"],["3","he","362","58"]])

#search(3)
