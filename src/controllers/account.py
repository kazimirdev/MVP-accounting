from flask import Blueprint, request, jsonify
from lxml import etree

from src.config import xml_file
from src.controllers.io import parse_xml, write_xml, next_gen_id


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
    return jsonify(accounts)


# Route to add a new account
@account_bp.route('/', methods=['POST'])
def add_account():
    tree = parse_xml(xml_file)
    root = tree.getroot()
    accounts_element = root.find('Accounts')

    new_account_id = next_gen_id(elements=accounts_element,
                                 type_element="Account")
    account_name = request.args.get('accountName')
    account_type = request.args.get('accountType')
    balance = request.args.get('balance')

    new_account = etree.SubElement(accounts_element, 'Account')
    etree.SubElement(new_account, 'AccountID').text = str(new_account_id)
    etree.SubElement(new_account, 'AccountName').text = account_name
    etree.SubElement(new_account, 'AccountType').text = account_type
    etree.SubElement(new_account, 'Balance').text = str(balance)

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


@account_bp.route('/<int:account_id>', methods=['PUT'])
def update_account_balance(account_id: int):
    new_balance = request.args.get('balance')
    tree = parse_xml(xml_file)
    root = tree.getroot()
    accounts_element = root.find('Accounts')

    for account in accounts_element.findall('Account'):
        if account.findtext('AccountID') == str(account_id):
            account.find('Balance').text = str(new_balance)
            write_xml(tree, xml_file)
            return jsonify({'message': f'Account ID {account_id} balance updated.'})

    return jsonify({'message': f'Account ID {account_id} not found.'}), 404