from person_database.province import Province
from person_database.city import City
import random
from person_database.person import Person
import string
from person_database.organization import Organization
from person_database.producer import Producer

from policy_database.ramo import Ramo
from policy_database.product import Product
from policy_database.policy import Policy
from policy_database.certificate import Certificate
from policy_database.coverage import Coverage
from policy_database.receipt import Receipt
from siniester_database.siniester import Siniester
from siniester_database.siniester_detail import SiniesterDetail


random.seed(42)

def save(path, text):
    with open(path, "w+") as f:
        f.write(text)

def load_person_database(province_range, city_range, person_range, organization_range, producer_range):
    provinces = []
    cities = []
    persons = []
    organizations = []
    producers = []
    
    #Provincias
    text = ''
    for p in range(0, province_range+1):
        province = Province(p, "Provincia {}".format(p))
        provinces.append(province)
        text += "Insert into provincias values({}, '{}'); \n".format(province.id, province.name)

    save("./data/persons/provincias.txt", text)

    #Ciudades
    text = ''
    for c in range(0, city_range+1):
        city = City()
        city.id = c
        city.name = "Ciudad {}".format(c)
        city.province_id = random.randint(0, province_range)
        cities.append(city)

        text += "Insert into ciudades values({}, '{}', {}) ;\n".format(city.id, city.name, city.province_id)

    save("./data/persons/ciudades.txt", text)

    #Personas
    text = ''
    for p in range(0, person_range+1):
        person = Person()
        person.id = p
        person.dni = random.randint(20000000, 50000000) 
        person.name = "Persona {}".format(p)
        person.address = "Calle {} - {}".format(random.choice(string.ascii_letters), random.randint(0, 1000)) 
        person.city_id = random.randint(0, city_range)
        person.birthdate = "{}/{}/{}".format(random.randint(1, 28), random.randint(1, 12), random.randint(1940, 2000))

        persons.append(person)

        text += "Insert into Personas values({}, {}, '{}', '{}', {}, '{}') ;\n".format(person.id, 
                                                                                       person.dni, 
                                                                                       person.name, 
                                                                                       person.address, 
                                                                                       person.city_id, 
                                                                                       person.birthdate)
                
    save("./data/persons/personas.txt", text)

    #Organizaciones
    text = ''
    for o in range(0, organization_range+1):
        organization = Organization()

        organization.id = o
        organization.name = "Empresa nro {}".format(o)
        organization.address = "Calle {} - {}".format(random.choice(string.ascii_letters), random.randint(0, 1000))
        organization.city_id = random.randint(0, city_range)

        organizations.append(organization)

        text += "Insert into Organizador values({},'{}','{}',{}) ;\n".format(organization.id,
                                                                              organization.name,
                                                                              organization.address,
                                                                              organization.city_id)
    
    save("./data/persons/organizaciones.txt", text)

    #Productores
    text = ''
    for p in range(0, producer_range + 1):

        producer = Producer(p, random.randint(0, organization_range));
        producers.append(producer)

        text += "Insert into Productor values({}, {}) ;\n".format(producer.person_id, producer.organization_id)
    
    save("./data/persons/productores.txt",text)

    return provinces, cities, persons, organizations, producers



def load_policy_database(ramo_range, product_range, policy_range, person_range, producer_range,
                         coverage_range, receipt_range):

    ramos = []
    products = []
    policies = []
    certificates = []
    coverages = []
    receipts = []

    text = ''
    for r in range(0, ramo_range+1):
        ramo = Ramo(r, "Ramo {}".format(r))

        ramos.append(ramo)

        text += "Insert into Ramo values({}, '{}') ;\n".format(ramo.id, ramo.description)

    save("./data/policies/ramos.txt", text)
    
    text = ''
    for p in range(0, product_range+1):

        product = Product()
        product.id = p
        product.ramo_id = random.randint(0, ramo_range)
        product.description = "Producto {}".format(p)

        products.append(product)

        text += "Insert into Producto values({}, {}, '{}') ;\n".format(product.ramo_id, 
                                                                               product.id, 
                                                                               product.description)
    save("./data/policies/products.txt", text)

    text = ''
    for c in range(0, coverage_range+1):

        coverage = Coverage()
        
        coverage.id = c

        random_product = random.choice(products)
        coverage.ramo_id = random_product.ramo_id
        coverage.product_id = random_product.id

        coverage.description = "Cobertura {}".format(c)
        coverage.min_sum = random.randint(5000, 10000)
        coverage.max_sum = random.randint(20000, 100000)

        coverages.append(coverage)

        text += "Insert into cobertura values({}, {}, {}, '{}', {}, {}) ;\n".format(coverage.id,
                                                                                    coverage.ramo_id,
                                                                                    coverage.product_id,
                                                                                    coverage.description,
                                                                                    coverage.min_sum,
                                                                                    coverage.max_sum)                                                                                 
    save("./data/policies/coverturas.txt", text)  

    text = ''
    for p in range(0, policy_range+1):

        policy = Policy()
        policy.id = p

        random_coverage = random.choice(coverages)
        policy.ramo_id = random_coverage.ramo_id
        policy.product_id = random_coverage.product_id

        policy.person_id = random.randint(0, person_range)
        policy.producer_id = random.randint(0, producer_range)

        day, month, year = random.randint(1, 28), random.randint(1, 12), random.randint(2010, 2020)
        policy.start_date = "{}/{}/{}".format(day, month, year)
        policy.end_date = "{}/{}/{}".format(day, month, year + 5)   # <-- Asumimos que las polizas vencen en 5 años

        policies.append(policy)

        text += "Insert into poliza values({}, {}, {}, {}, {}, '{}', '{}') ;\n".format(policy.id, 
                                                                                       policy.ramo_id, 
                                                                                       policy.product_id,
                                                                                       policy.person_id,
                                                                                       policy.producer_id,
                                                                                       policy.start_date,
                                                                                       policy.end_date)
    save("./data/policies/policies.txt", text)

    text = ''
    c = -1
    for policy in policies:
        c += 1
        certificate = Certificate()
        certificate.id = c
        certificate.policy_id = policy.id 
        certificate.product_id = policy.product_id
        certificate.ramo_id = policy.ramo_id
        
        random_coverage = random.choice(coverages)
        certificate.coverage_id = random_coverage.id

        certificate.sum_assured = random.randint(5000, 20000)
        certificate.description = "Certificado {}".format(c)

        certificates.append(certificate)

        text += "Insert into certificados values({}, {}, {}, {}, {}, '{}') ;\n".format(certificate.policy_id,
                                                                                       certificate.ramo_id,
                                                                                       certificate.product_id,
                                                                                       certificate.id,
                                                                                       certificate.coverage_id,
                                                                                       certificate.sum_assured,
                                                                                       certificate.description)                                                                                 
    save("./data/policies/certificados.txt", text)  


    text = ''
    for c in range(0, receipt_range+1):

        receipt = Receipt()
        
        receipt.id = c

        random_policy = random.choice(policies)
        receipt.policy_id = random_policy.id
        receipt.ramo_id = random_policy.ramo_id
        receipt.product_id = random_policy.product_id

        receipt.amount = random.randint(5000, 20000)

        receipts.append(receipt)

        text +="Insert into Recibos values({}, {}, {}, {}, {}) ;\n".format(receipt.id,
                                                                           receipt.policy_id,
                                                                           receipt.ramo_id,
                                                                           receipt.product_id,
                                                                           receipt.amount)                                                                                   
    save("./data/policies/recibos.txt", text)  

    return ramos, products, policies, certificates, coverages, receipts

    

def load_siniester_database(siniester_range, policies, cities, persons, certificates):

    siniesters = []

    text = ''
    for s in range(0, siniester_range+1):

        siniester = Siniester()
        
        siniester.id = s

        random_policy = random.choice(policies)
        siniester.policy_id = random_policy.id
        siniester.ramo_id = random_policy.ramo_id
        siniester.product_id = random_policy.product_id

        day, month, year = random.randint(1, 28), random.randint(1, 12), random.randint(2010, 2020)
        siniester.date = "{}/{}/{}".format(day, month, year)

        siniester.address = "Calle {} - {}".format(random.choice(string.ascii_letters), random.randint(0, 1000))
        
        random_city = random.choice(cities)
        siniester.city_id = random_city.id

        random_person = random.choice(persons)
        siniester.person_id = random_person.id

        siniesters.append(siniester)

        text += "Insert into siniestros values({}, {}, {}, {}, {}) ;\n".format(siniester.id,
                                                                               siniester.policy_id,
                                                                               siniester.ramo_id,
                                                                               siniester.product_id,
                                                                               siniester.date,
                                                                               siniester.address,
                                                                               siniester.city_id,
                                                                               siniester.person_id)
    save("./data/siniesters/siniestros.txt", text)  

    siniester_details = []
    text = ''
    for s in siniesters:

        siniester_detail = SiniesterDetail()

        certificate = [c for c in certificates if c.policy_id == s.policy_id 
                                                and c.product_id == s.product_id 
                                                and c.ramo_id == s.ramo_id].pop()

        siniester_detail.policy_id = certificate.policy_id
        siniester_detail.ramo_id = certificate.ramo_id
        siniester_detail.product_id = certificate.product_id
        
        siniester_detail.certify_id = certificate.id
        siniester_detail.description = 'Descripcion del siniestro nro {}'.format(s.id)
        siniester_detail.amount = random.randint(5000, 20000)

        siniester_details.append(siniester_detail)

        text += "Insert into detalle_siniestro values({}, {}, {}, {}, {}, {}) ;\n".format(siniester_detail.policy_id,
                                                                                          siniester_detail.ramo_id,
                                                                                          siniester_detail.product_id,
                                                                                          siniester_detail.certify_id,
                                                                                          siniester_detail.description,
                                                                                          siniester_detail.amount)
    save("./data/siniesters/detalle_siniestros.txt", text)  
        
    return siniesters, siniester_details





SiniesterDetail
