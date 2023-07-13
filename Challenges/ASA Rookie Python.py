from algosdk import *
from algosdk.v2client.algod import AlgodClient
from algosdk.future import transaction

from utils import validate, print_error, algod_server, algod_token


# DO NOT CHANGE
challenge_id = "3475011828333590772"
client = AlgodClient(algod_token, algod_server)

txids = []

# TODO: Paste your secret key here. You can find it underneath the code editor.
secret_key = ""

# Get the address from the secret key
addr = account.address_from_private_key(secret_key)

# Get the suggested parameters from the Algod server.
# These include current fee levels and suggested first/last rounds.
sp = client.suggested_params()


# TODO: Create a payment transaction from you to you using the `acct` variable defined above
# The asset should have a total supply of 1 but have 100 total units
# The asset should have the name `Task Asset`
txn = transaction.AssetCreateTxn(
    sender=addr,  # TODO: Sender, should be your addr
    sp=sp,  # Suggested params we got above

    total=100,  # TODO: Total number of units (100)
    decimals=2,  # TODO: Total number of decimals (2)
    asset_name="Task Asset",  # TODO: The name of the asset (the string 'Task Asset' )

    reserve=addr,  # TODO: Should be your address
    clawback=addr,  # TODO: Should be your address
    freeze=addr,  # TODO: Should be your address
    manager=addr,  # TODO: Should be your address

    unit_name=None,  # The unit name of the asset (can leave blank for this task)
    url=None,  # The url of the asset (can leave blank for this task, for an NFT this might be an IPFS uri)

    default_frozen=False,  # Default frozen, leave false
)

# Sign the transaction.
# returns a SignedTxn object containing the bytes to be sent to the network
signed = txn.sign(secret_key)

# Send the transaction, returns the transaction id for
# the first transaction in the group

try:
    # Send the transaction to the network
    # this returns the first transaction id in the group
    txId = client.send_transaction(signed)

    # Add txid to list to be validated later
    txids.append(txId)

    # Wait for the transaction to be confirmed.
    result = transaction.wait_for_confirmation(client, txId, 2)

    # Log out the confirmed round
    print(f"Confirmed round: {result['confirmed-round']}")
    print(f"Created Asset: {result['asset-index']}")

except error.AlgodHTTPError as err:
    print_error(str(err))

else:
    print("Verifying the challenge...")
    if validate(challenge_id, txids):
        print("Transactions validated! Please return to the developer portal to collect your badge. :)")
    else:
        print(
            "Something went wrong :( Check the error message, update the code and try again!"
        )