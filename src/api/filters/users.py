# # stdlib
# from typing import Optional

# # third party
# # from fastapi_filter import Filter
# from fastapi_filter.contrib.sqlalchemy import Filter

# # marsdevs
# from api.models import user as m_user


# class UserFilter(Filter):
#     is_active: Optional[bool]
#     role: Optional[m_user.Role]

#     class Constants:
#         # pass
#         model = m_user.User  # Associate the filter with the User model
#         # search_model_fields = ["profile__name", "email"]
