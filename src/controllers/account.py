from flask import Blueprint, request, jsonify
from lxml import etree

from src.config import xml_file
from src.controllers.io import parse_xml, write_xml


account_bp = Blueprint('account', __name__)


# Route to get all accounts
@account_bp.route('/', methods=['GET'])
def get_accounts():
    tree = parse_xml(xml_file)
    root = tree.getroot()
    accounts_element = root.find('Accounts')
    accounts = []
    for account in accounts_element.findall('Account'):
        accounts.append({
            'AccountID': account.findtext('AccountID'),
            'AccountName': account.findtext('AccountName'),
            'AccountType': account.findtext('AccountType'),
            'Balance': account.findtext('Balance')
        })
    print(accounts)
    return jsonify(accounts)


# Route to add a new account
@account_bp.route('/', methods=['POST'])
def add_account():
    data = request.json
    tree = parse_xml(xml_file)
    root = tree.getroot()
    accounts_element = root.find('Accounts')

    new_account = etree.SubElement(accounts_element, 'Account')
    etree.SubElement(new_account, 'AccountID').text = str(data['AccountID'])
    etree.SubElement(new_account, 'AccountName').text = data['AccountName']
    etree.SubElement(new_account, 'AccountType').text = data['AccountType']
    etree.SubElement(new_account, 'Balance').text = str(data['Balance'])

    write_xml(tree, xml_file)
    return jsonify({'message': 'Account added successfully'})


# Route to delete an account
@account_bp.route('/<int:account_id>', methods=['DELETE'])
def delete_account(account_id: int):
    tree = parse_xml(xml_file)
    root = tree.getroot()
    accounts_element = root.find('Accounts')

    # Remove account
    for account in accounts_element.findall('Account'):
        if account.findtext('AccountID') == str(account_id):
            accounts_element.remove(account)

            # Remove associated transactions
            transactions_element = root.find('Transactions')
            for transaction in transactions_element.findall('Transaction'):
                if transaction.findtext('AccountID') == str(account_id):
                    transactions_element.remove(transaction)

            write_xml(tree, xml_file)
            return jsonify({'message': f'Account ID {account_id} and associated transactions deleted.'})
    return jsonify({'message': f'Account ID {account_id} not found.'}), 404
