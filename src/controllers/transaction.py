from flask import Blueprint, request, jsonify
from lxml import etree

from src.config import xml_file
from src.controllers.io import parse_xml, write_xml, next_gen_id


transaction_bp = Blueprint('transaction', __name__)


# Route to get all transactions
@transaction_bp.route('/', methods=['GET'])
def get_transactions():
    tree = parse_xml(xml_file)
    root = tree.getroot()
    transactions_element = root.find('Transactions')
    transactions = []
    for transaction in transactions_element.findall('Transaction'):
        transactions.append({
            'TransactionID': transaction.findtext('TransactionID'),
            'Date': transaction.findtext('Date'),
            'Description': transaction.findtext('Description'),
            'Amount': transaction.findtext('Amount'),
            'AccountID': transaction.findtext('AccountID'),
            'Type': transaction.findtext('Type')
        })
    return jsonify(transactions)


# Route to add a new transaction
@transaction_bp.route('/', methods=['POST'])
def add_transaction():
    tree = parse_xml(xml_file)
    root = tree.getroot()
    transactions_element = root.find('Transactions')

    new_transaction_id = next_gen_id(elements=transactions_element,
                                     type_element="Transaction")
    date = request.args.get('date')
    description = request.args.get('description')
    amount = request.args.get('amount')
    account_id = request.args.get('accountID')
    transaction_type = request.args.get('type')

    new_transaction = etree.SubElement(transactions_element, 'Transaction')
    etree.SubElement(new_transaction, 'TransactionID').text = str(new_transaction_id)
    etree.SubElement(new_transaction, 'Date').text = date
    etree.SubElement(new_transaction, 'Description').text = description
    etree.SubElement(new_transaction, 'Amount').text = str(amount)
    etree.SubElement(new_transaction, 'AccountID').text = str(account_id)
    etree.SubElement(new_transaction, 'Type').text = transaction_type

    write_xml(tree, xml_file)
    return jsonify({'message': 'Transaction added successfully', 'TransactionID': new_transaction_id})


# Route to delete a transaction
@transaction_bp.route('/<int:transaction_id>', methods=['DELETE'])
def delete_transaction(transaction_id: int):
    tree = parse_xml(xml_file)
    root = tree.getroot()
    transactions_element = root.find('Transactions')

    for transaction in transactions_element.findall('Transaction'):
        if transaction.findtext('TransactionID') == str(transaction_id):
            transactions_element.remove(transaction)
            write_xml(tree, xml_file)
            return jsonify({'message': f'Transaction ID {transaction_id} deleted.'})
    return jsonify({'message': f'Transaction ID {transaction_id} not found.'}), 404
