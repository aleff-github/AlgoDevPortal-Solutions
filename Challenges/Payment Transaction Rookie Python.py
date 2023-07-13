from algosdk import *
from algosdk.v2client.algod import AlgodClient
from algosdk.future import transaction

from utils import validate, print_error, algod_token, algod_server

# DO NOT CHANGE
challenge_id = "3474867148855516251"
client = AlgodClient(algod_token, algod_server)
txids = []

# TODO: Paste your secret key here. You can find it underneath the code editor.
secret_key = ""

# Get the address from the secret key
addr = account.address_from_private_key(secret_key)

snd_addr = addr
print(f"Sender: {snd_addr}")
rcv_addr = addr
print(f"Receiver: {rcv_addr}")

# TODO: Get the suggested parameters from the Algod server.
params = client.suggested_params()
amt = 1000000
pay_type = "pay"
fee = 1000

# TODO: Create a payment transaction from you to you for 1 Algo
# hint: From and To should be your `addr` and 1 Algo is 1m microAlgos
ptxn = transaction.PaymentTxn(sender=snd_addr,
                              sp=params,
                              receiver=rcv_addr,
                              amt=amt)
print("Payment transaction created.")

# TODO: Sign the transaction.
signed = ptxn.sign(secret_key)
print("Payment signed.")

# Send the transaction, returns the transaction id for
# the first transaction in the group
try:
	# Send the transaction to the network
	# this returns the first transaction id in the group
	txId = client.send_transaction(signed)
	print("Transaction sent.")

	# Add txid to list to be validated later
	txids.append(txId)
	print("Appended txid")

	# Wait for the transaction to be confirmed.
	result = transaction.wait_for_confirmation(client, txId, 2)
	print("Transaction confirmed")

	# Log out the confirmed round
	print(f"Confirmed round: {result['confirmed-round']}")

except error.AlgodHTTPError as err:
	print_error(str(err))

except:
    print("Generic Exception")

print("Verifying the challenge...")
if validate(challenge_id, txids):
    print(
        "Transactions validated! Please return to the developer portal to collect your badge. :)"
    )
else:
    print(
        "Something went wrong :( Check the error message, update the code and try again!"
    )
