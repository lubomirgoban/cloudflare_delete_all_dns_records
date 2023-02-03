import requests


class CFRemove:
    def __init__(self, token, zone_id):
        self.token = token
        self.zone_id = zone_id

    def check_token(self):
        url = "https://api.cloudflare.com/client/v4/user/tokens/verify"

        headers = {
            'Authorization': f'Bearer {self.token}'
        }

        response = requests.request("GET", url, headers=headers)

        return response.json()

    def get_dns_records(self):
        url = f"https://api.cloudflare.com/client/v4/zones/{self.zone_id}/dns_records?per_page=5000"
        headers = {
            'Authorization': f'Bearer {self.token}'
        }
        response = requests.request("GET", url, headers=headers)

        return response.json()

    def delete(self, id):
        url = f"https://api.cloudflare.com/client/v4/zones/{self.zone_id}/dns_records/{id}"
        headers = {
            'Authorization': f'Bearer {self.token}'
        }
        response = requests.request("DELETE", url, headers=headers)
        return response.json()['success']

    def delete_dns_records(self):
        if self.check_token()['success']:
            dns_records = self.get_dns_records()
            count_records = len(dns_records['result'])
            print(f"Count records - {count_records}")
            for dns_record in dns_records['result']:
                result = self.delete(dns_record['id'])
                print(f"Delete {dns_record['id']} - result {result}")
            if count_records < 5000:
                print("All records deleted")
            else:
                print('Removed the first 5000 records. Run the script again')
        else:
            print(f"Invalid API Token. Error : {self.check_token()}")


"""
how to use

CFRemove(token, zone_id).delete_dns_records()
where token = API token with edit permission 
zone_id = copy of zone id from dashboard page

"""

CFRemove(<enter token>, <enter zone_id>).delete_dns_records()
