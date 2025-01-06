import hashlib
import requests

def normalize_for_hash(t):
    t = str(t) if t is not None else ""
    if len(t) > 500:
        t = t[:500]
    t = t.upper()
    t = ''.join(filter(lambda x: x.isalnum() or x in 'ŻÓŁĆĘŚĄŹŃ', t))
    replacements = {
        'Ż': 'Z', 'Ó': 'O', 'Ł': 'L', 'Ć': 'C', 'Ę': 'E',
        'Ś': 'S', 'Ą': 'A', 'Ź': 'Z', 'Ń': 'N'
    }
    for key, value in replacements.items():
        t = t.replace(key, value)
    return t

def get_normalized_hex_md5(t):
    normalized = normalize_for_hash(t)
    print(normalized)
    md5_hash = hashlib.md5(normalized.encode()).hexdigest().upper()
    return str(md5_hash)

def get_info_from_cek(hash):
    url = f"https://moj.gov.pl/nforms/api/UprawnieniaKierowcow/2.0.10/data/driver-permissions?hashDanychWyszukiwania={hash}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    elif response.status_code == 400:
        print("Driver's license information not found")
    else:
        response.raise_for_status()

def print_dict_nicely(d, indent=0):
    for key, value in d.items():
        if isinstance(value, dict):
            print(' ' * indent + f"{key}:")
            print_dict_nicely(value, indent + 4)
        elif isinstance(value, list):
            print(' ' * indent + f"{key}:")
            for item in value:
                if isinstance(item, dict):
                    print_dict_nicely(item, indent + 4)
                else:
                    print(' ' * (indent + 4) + str(item))
        else:
            print(' ' * indent + f"{key}: {value}")

if __name__ == "__main__":
    first_name = input("Enter first name: ")
    surname = input("Enter surname: ")
    drivers_license_id = input("Enter driver's license ID: ")

    data_to_hash = f"{first_name}{surname}{drivers_license_id}"
    hash_value = get_normalized_hex_md5(data_to_hash)
    print(hash_value)
    info = get_info_from_cek(hash_value)
    if info:
        print_dict_nicely(info)
