from load import load_person_database
from load import load_policy_database
from load import load_siniester_database


if __name__ == '__main__':

    person_range = 10000
    producer_range = 250
    policy_range = 10000
    #----------------
    #   Person DB
    #----------------
    
    provinces, cities, persons, organizations, producers = load_person_database(province_range=23, 
                                                                                city_range=200, 
                                                                                person_range=person_range, 
                                                                                organization_range=producer_range, 
                                                                                producer_range=producer_range)

    #----------------
    #   Policy DB
    #----------------

    ramos, products, policies, certificates, coverages, receipts = load_policy_database(ramo_range=50, 
                                                                                        product_range=50, 
                                                                                        policy_range=policy_range,
                                                                                        person_range=person_range,
                                                                                        producer_range=producer_range,
                                                                                        certificate_range = 1000,
                                                                                        coverage_range=20,
                                                                                        receipt_range=1000)

    siniesters = load_siniester_database(siniester_range=200, 
                                         policies=policies, 
                                         cities=cities, 
                                         persons=persons)


    print('Ok :)')

