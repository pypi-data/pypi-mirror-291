
class Payment(object):

    def __init__(self):

        self.account_id = None
        self.description = None
        self.additional_data = None # order (...), airline (...), seller_details (...)
        self.country = None
        self.merchant_order_id = None
        self.merchant_reference = None
        self.amount = None # currency, value
        self.customer_payer = None # customer ...
        self.checkout = None # session
        self.country = None
        self.workflow = None
        self.payment_method = None # token, vaulted_token, type, detail [card (...), ticket (...), wallet (...)]
        self.metadata = None # [key, value]
        self.callback_url = None
        self.fraud_screening = None #stand_alone