from utils.safe_route import check_connection

@check_connection
class ClientService:
    def get(self, bd, hd):
        ...