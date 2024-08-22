
class Customer(object):

    def __init__(self):

        self.id = None
        self.merchant_customer_id = None
        self.merchant_customer_created_at = None
        self.first_name = None
        self.last_name = None
        self.gender = None
        self.date_of_birth = None
        self.email = None
        self.nationality = None
        self.country = None
        self.created_at = None
        self.updated_at = None
        self.document = None # document_number, document_type
        self.phone = None # country_code, number
        self.billing_address = None # address_line1, address_line2, city, country, state, zip_code, neighborhood
        self.shipping_address = None # address_line1, address_line2, city, country, state, zip_code, neighborhood
        self.metadata = None
