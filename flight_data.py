class FlightData:

    def __init__(self, price=0, origin_city=0, origin_airport=0, destination_city=0, destination_airport=0, out_date=0,
                 return_date=0):
        self.price = price
        self.origin_city = origin_city
        self.origin_airport = origin_airport
        self.destination_city = destination_city
        self.destination_airport = destination_airport
        self.out_date = out_date
        self.return_date = return_date
