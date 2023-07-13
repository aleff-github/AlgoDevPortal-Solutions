from algosdk import *
from algosdk.v2client.algod import AlgodClient
from algosdk.atomic_transaction_composer import *
from algosdk.future import transaction

from utils import (
    validate,
    print_error,
    faucet_addr,
    usdc_asa_id,
    algod_token,
    algod_server,
)


# DO NOT CHANGE
challenge_id = "3475013087686335165"
client = AlgodClient(algod_token, algod_server)
txids = []

# TODO: Paste your secret key here. You can find it underneath the code editor.
secret_key = ""

# Get the address from the secret key
addr = account.address_from_private_key(secret_key)

# Create a TransactionSigner object we'll use later
signer = AccountTransactionSigner(secret_key)

# Get the suggested parameters from the Algod server.
# These include current fee levels and suggested first/last rounds.
sp = client.suggested_params()

atc = AtomicTransactionComposer()
atc.add_transaction(
    TransactionWithSigner(
        txn=transaction.PaymentTxn(
            sender=addr,  # TODO: set to your address
            receiver=faucet_addr,  # TODO: set to the faucet_address we're importing from utils
            amt=int(1e6),  # 1 algo
            sp=sp,
        ),
        signer=signer,
    )
)

# Opt into usdc_asa_id
atc.add_transaction(
    TransactionWithSigner(
        txn=transaction.AssetTransferTxn(
            sender=addr,  # TODO: set to your address
            receiver=addr,  # TODO: set to your address
            index=usdc_asa_id,  # TODO: set to the asset id of USDC on testnet (imported from utils)
            amt=0,
            sp=sp,
        ),
        signer=signer,
    )
)

try:
    result = atc.execute(client, 2)
    txids = result.tx_ids
    print(f"Confirmed in round {result.confirmed_round}")
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