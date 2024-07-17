from ninja import NinjaAPI

from challenge.users.api import users_router
from challenge.payment.api import payment_router

# from users.api import users_router
api = NinjaAPI()
api.add_router('users/', users_router)
api.add_router('payment/', payment_router)
