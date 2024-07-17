from rolepermissions.roles import AbstractUserRole


class People(AbstractUserRole):
    available_permissions = {
        'make_transfer': True,
        'receive_transfer': True,
    }


class Shopkeeper(AbstractUserRole):
    available_permissions = {
        'make_transfer': False,
        'receive_transfer': True,
    }
