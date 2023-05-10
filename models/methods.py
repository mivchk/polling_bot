import psycopg2

conn = psycopg2.connect(dbname='postgres',
                        user='postgres',
                        password='8150',
                        host='localhost',
                        port="5432")

cursor = conn.cursor()


def insert_cus(customer_id, gender, age):
    statement = "insert into customers(customer_id, gender, age) " \
                "values (%s, %s, %s)" \
                "on conflict (customer_id) do nothing "
    record = (customer_id, gender, age)
    cursor.execute(statement, record)
    conn.commit()


def insert_fp(cust_id, is_alc, like_k, cook_k, know_rec):
    statement = "insert into first_poll(customer_id, is_alc, like_k, cook_k, know_rec) " \
                "values (%s, %s, %s, %s, %s)" \
                "on conflict (customer_id) do nothing "
    record = (cust_id, is_alc, like_k, cook_k, know_rec)
    cursor.execute(statement, record)
    conn.commit()


def get_data(cid):
    statement = "select customer_id from customers where customer_id = %s"
    cursor.execute(statement, (cid,))
    result = cursor.fetchall()
    return result
