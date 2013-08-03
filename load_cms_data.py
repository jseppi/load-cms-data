import sys, getopt
import sqlite3
import csv
import os
from create_cms_db import create_cms_db

#TODO: In blog, mention had to save this as CSV because only Excel provided
region_crosswalk_file = 'data/ZipHsaHrr11.csv'
inpatient_file = 'data/Medicare_Provider_Charge_Inpatient_DRG100_FY2011.csv'
outpatient_file = 'data/Medicare_Provider_Charge_Outpatient_APC30_CY2011.csv'

db_name = ''

def print_usage():
    print "Usage: $ python load_cms_data.py -d <sqlitedb>"
    sys.exit(2)

try:
    opts, args = getopt.getopt(sys.argv[1:], 'd:')
except getopt.GetoptError:
    print_usage()

for opt, arg in opts:
    if opt == '-d':
        db_name = arg

if db_name == '':
    print_usage()

if not os.path.isfile(db_name):
    print "Database <" + db_name + "> not found, creating new with same name."
    create_cms_db(db_name)


# ------------------------------------------------------
# First load ZipCode-to-ReferralRegion data from the region crosswalk file

zip_regions = {}
ref_regions = {}
service_regions = {}

# columns = zipcode11 hsanum  hsacity hsastate hrrnum  hrrcity hrrstate
with open(region_crosswalk_file, 'rb') as csvfile:
    r = csv.DictReader(csvfile)
    
    for row in r:
        zip_code = row['zipcode11']
        hsa_id = int(row['hsanum'])
        hrr_id = int(row['hrrnum'])

        zip_regions[zip_code] = {
            'hsa_id': hsa_id,
            'hsa_city': row['hsacity'],
            'hsa_state': row['hsastate'],
            'hrr_id': hrr_id,
            'hrr_city': row['hrrcity'],
            'hrr_state': row['hrrstate']
        }

        service_regions[hsa_id] = {
            'city': row['hsacity'],
            'state': row['hsastate'],
            'zip': zip_code
        }

        ref_regions[hrr_id] = {
            'city': row['hrrcity'],
            'state': row['hrrstate'],
            'zip': zip_code
        }

# ------------------------------------------------------
# Next, load the drgs and inpatient payment info from the inpatient_file

drgs = {}
providers = {}
inpatient_payments = {}

# inpatient_columns = DRG Definition,Provider Id,Provider Name,Provider Street Address,
#   Provider City,Provider State,Provider Zip Code,
#   Hospital Referral Region Description, 
#   Total Discharges , Average Covered Charges , Average Total Payments

with open(inpatient_file, 'rb') as csvfile:
    r = csv.reader(csvfile)
    r.next()  # Skip the header row

    curr_inpatient_payment_id = 0
    for row in r:
        drg_defn = row[0]
        drg_id = int(drg_defn.split(' - ')[0])
        drg_name = drg_defn.split(' - ')[1]
        
        drgs[drg_id] = { 'name': drg_name }

        provider_id = int(row[1])
        provider_name = row[2]
        provider_street = row[3]
        provider_city = row[4]
        provider_state = row[5]
        provider_zip = row[6]

        # unused: ref_region_name = row[7]

        providers[provider_id] = {
            'name': provider_name,
            'street': provider_street,
            'city': provider_city,
            'state': provider_state,
            'zip': provider_zip
        }

        num_discharged = int(row[8])
        avg_covered = float(row[9])
        avg_payment = float(row[10])

        inpatient_payments[curr_inpatient_payment_id] = {
            'drg_id': drg_id,
            'provider_id': provider_id,
            'num_discharged': num_discharged,
            'avg_covered': avg_covered,
            'avg_payment': avg_payment
        }

        curr_inpatient_payment_id += 1
        
# ------------------------------------------------------
# Then load the apcs and outpatient payment info from the outpatient_file

apcs = {}
outpatient_payments = {}

# outpatient_columns = APC,Provider Id,Provider Name,Provider Street Address,
#   Provider City,Provider State,Provider Zip Code,Hospital Referral Region Description,
#   Outpatient Services,Average Estimated Submitted Charges,Average Total Payments
with open(outpatient_file, 'rb') as csvfile:
    r = csv.reader(csvfile)
    r.next()  # Skip the header row
    
    curr_outpatient_payment_id = 0
    for row in r:
        apc_defn = row[0]
        apc_id = int(apc_defn.split(' - ')[0])
        apc_name = apc_defn.split(' - ')[1]

        apcs[apc_id] = { 'name': apc_name }

        provider_id = int(row[1])
        provider_name = row[2]
        provider_street = row[3]
        provider_city = row[4]
        provider_state = row[5]
        provider_zip = row[6]

        providers[provider_id] = {
            'name': provider_name,
            'street': provider_street,
            'city': provider_city,
            'state': provider_state,
            'zip': provider_zip
        }

        # unused: ref_region_name = row[7]

        num_discharged = int(row[8])
        avg_covered = float(row[9])
        avg_payment = float(row[10])

        outpatient_payments[curr_outpatient_payment_id] = {
            'apc_id': apc_id,
            'provider_id': provider_id,
            'num_discharged': num_discharged,
            'avg_covered': avg_covered,
            'avg_payment': avg_payment
        }

        curr_outpatient_payment_id += 1

# ------------------------------------------------------
# Finally, write it all to the database

with sqlite3.connect(db_name) as conn:
    # zip_regions = {}
    # ref_regions = {}
    # service_regions = {}
    # providers = {}
    # drgs = {}
    # inpatient_payments = {}
    # apcs = {}
    # outpatient_payments = {}
    pass