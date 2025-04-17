import json

from ..account_management_config import TRANSFERS_STORE_FILE
from ..account_management_exception import AccountManagementException

def save_transfer_request(new_transfer_request):
    try:
        with open(TRANSFERS_STORE_FILE, "r", encoding="utf-8", newline="") as file:
            transfer_store = json.load(file)
    except FileNotFoundError:
        transfer_store = []
    except json.JSONDecodeError as ex:
        raise AccountManagementException("JSON Decode Error - Wrong JSON Format") from ex
    for transfer in transfer_store:
        if (transfer["from_iban"] == new_transfer_request.from_iban and
                transfer["to_iban"] == new_transfer_request.to_iban and
                transfer["transfer_date"] == new_transfer_request.transfer_date and
                transfer["transfer_amount"] == new_transfer_request.transfer_amount and
                transfer["transfer_concept"] == new_transfer_request.transfer_concept and
                transfer["transfer_type"] == new_transfer_request.transfer_type):
            raise AccountManagementException("Duplicated transfer in transfer list")
    transfer_store.append(new_transfer_request.to_json())
    try:
        with open(TRANSFERS_STORE_FILE, "w", encoding="utf-8", newline="") as file:
            json.dump(transfer_store, file, indent=2)
    except FileNotFoundError as ex:
        raise AccountManagementException("Wrong file  or file path") from ex
    except json.JSONDecodeError as ex:
        raise AccountManagementException("JSON Decode Error - Wrong JSON Format") from ex


def get_deposit_iban_and_amount(input_deposit):
    try:
        deposit_iban = input_deposit["IBAN"]
        deposit_amount = input_deposit["AMOUNT"]
    except KeyError as e:
        raise AccountManagementException("Error - Invalid Key in JSON") from e
    return deposit_amount, deposit_iban


def input_deposit_json_store(input_file):
    try:
        with open(input_file, "r", encoding="utf-8", newline="") as file:
            input_deposit = json.load(file)
    except FileNotFoundError as ex:
        raise AccountManagementException("Error: file input not found") from ex
    except json.JSONDecodeError as ex:
        raise AccountManagementException("JSON Decode Error - Wrong JSON Format") from ex
    # comprobar valores del fichero
    deposit_amount, deposit_iban = get_deposit_iban_and_amount(input_deposit)
    return deposit_amount, deposit_iban