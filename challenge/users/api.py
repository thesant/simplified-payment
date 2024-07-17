from ninja import Router
from challenge.users.models import User
from challenge.users.schemas import UserSchema, TypeUserSchema
from django.contrib.auth.hashers import make_password
from django.core.exceptions import ValidationError
from rolepermissions.roles import assign_role

users_router = Router()


@users_router.post('/', response={200: dict, 400: dict, 500: dict})
def create_user(request, type_user_schema: TypeUserSchema):
    user = User(**type_user_schema.user.dict())
    user.password = make_password(type_user_schema.user.password)
    try:
        user.full_clean()
        user.save()
    except ValidationError as e:
        return 400, {'errors': e.message_dict}
    except Exception as e:
        return 500, {'errors': 'Error internal server'}
    assign_role(user, type_user_schema.type_user.type)
    return 200, {'user_id': user.id}
