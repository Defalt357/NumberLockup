import requests

class PhoneLookupError(Exception):
    """Exceção personalizada para erros de consulta de número de telefone."""
    pass

class PhoneInfo:
    def __init__(self, number, international_format, local_format, country, location, carrier, line_type):
        self.number = number
        self.international_format = international_format
        self.local_format = local_format
        self.country = country
        self.location = location
        self.carrier = carrier
        self.line_type = line_type

    def __str__(self):
        return (f"Número: {self.number}\n"
                f"Formato Internacional: {self.international_format}\n"
                f"Formato Local: {self.local_format}\n"
                f"País: {self.country}\n"
                f"Localidade: {self.location}\n"
                f"Operadora: {self.carrier}\n"
                f"Linha de Tipo: {self.line_type}")

def get_phone_info(phone_number, api_key):
    url = f"http://apilayer.net/api/validate?access_key={api_key}&number={phone_number}"

    try:
        response = requests.get(url)
        response.raise_for_status()  # Lança uma exceção para códigos de status HTTP 4xx/5xx
        data = response.json()

        if data['valid']:
            return PhoneInfo(
                number=data['number'],
                international_format=data['international_format'],
                local_format=data['local_format'],
                country=data['country_name'],
                location=data['location'],
                carrier=data['carrier'],
                line_type=data['line_type']
            )
        else:
            raise PhoneLookupError("Número inválido ou não encontrado.")

    except requests.exceptions.HTTPError as http_err:
        raise PhoneLookupError(f"Erro HTTP: {http_err}")
    except requests.exceptions.RequestException as req_err:
        raise PhoneLookupError(f"Erro de requisição: {req_err}")
    except KeyError:
        raise PhoneLookupError("Resposta inesperada da API. Verifique o formato da resposta.")

def main():
    # Substitua pela sua chave de API do Numverify
    api_key = '54077286e9bac2a86ea63c88a7eaf41c'
    phone_number = input("Digite o número de telefone com o código do país: ")

    try:
        phone_info = get_phone_info(phone_number, api_key)
        print("\nInformações do número:\n")
        print(phone_info)
    except PhoneLookupError as e:
        print(f"Erro ao buscar informações do número: {e}")

if __name__ == "__main__":
    main()


