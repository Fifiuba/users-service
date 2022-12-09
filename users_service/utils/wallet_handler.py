from users_service.utils.wallet import Wallet


def init_wallet():
  
    from users_service.utils.wallet import Wallet
    global wallet
    wallet = Wallet()

def get_wallet():
    try:
        yield wallet
    finally:
        wallet