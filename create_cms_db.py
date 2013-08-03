import sys, getopt
import sqlite3


def create_cms_db(outfile_name):
    with sqlite3.connect(outfile_name) as conn:

        cursor = conn.cursor()


        cursor.execute("""CREATE TABLE zip_regions (
            id INTEGER PRIMARY KEY
            , zip VARCHAR(5)
            , hsa_id INTEGER
            , hsa_city VARCHAR(40)
            , hsa_state VARCHAR(2)
            , hrr_id INTEGER
            , hrr_city VARCHAR(40)
            , hrr_state VARCHAR(2)
            )""")

        cursor.execute("""CREATE TABLE ref_regions (
            id INTEGER PRIMARY KEY
            , state VARCHAR(2)
            , city VARCHAR(40)
            , zip VARCHAR(5)
            )""")

        cursor.execute("""CREATE TABLE service_regions (
            id INTEGER PRIMARY KEY
            , state VARCHAR(2)
            , city VARCHAR(40)
            , zip VARCHAR(5)
            )""")

        cursor.execute("""CREATE TABLE drgs (
            id INTEGER PRIMARY KEY
            , name VARCHAR(60)
            )""")

        cursor.execute("""CREATE TABLE apcs (
            id INTEGER PRIMARY KEY
            , name VARCHAR(60)
            )""")

        cursor.execute("""CREATE TABLE providers (
            id INTEGER PRIMARY KEY
            , name VARCHAR(60)
            , street VARCHAR(100)
            , city VARCHAR(40)
            , state VARCHAR(2)
            , zip VARCHAR(5)
            )""")
            #, hrr_id INTEGER #TODO: actually should use zip_regions lookup
            #, hsa_id INTEGER #TODO: actually should use zip_regions lookup

        cursor.execute("""CREATE TABLE inpatient_payment_info (
            id INTEGER PRIMARY KEY
            , drg_id INTEGER NOT NULL
            , provider_id INTEGER NOT NULL
            , num_discharged INTEGER NULL
            , avg_covered REAL NULL
            , avg_payment REAL NULL
            )""")

        cursor.execute("""CREATE TABLE outpatient_payment_info (
            id INTEGER PRIMARY KEY
            , apc_id INTEGER NOT NULL
            , provider_id INTEGER NOT NULL
            , num_discharged INTEGER NULL
            , avg_covered REAL NULL
            , avg_payment REAL NULL
            )""")

        cursor.close()

    return

if __name__ == '__main__':
    
    outfile_name = ''

    def print_usage():
        print "Usage: $ python create_cms_db.py -o <outputdb>"
        sys.exit(2)

    try:
        opts, args = getopt.getopt(sys.argv[1:], 'o:')
    except getopt.GetoptError:
        print_usage()

    for opt, arg in opts:
        if opt == '-o':
            outfile_name = arg

    if outfile_name == '':
        print_usage()

    print "Creating new db: " + outfile_name

    create_cms_db(outfile_name)


