from typing import List, Optional

from mlflow.entities.auth_enums import SubjectType
from mlflow.pydantic_v1 import BaseModel, Field, SecretStr, constr


class UserInfo(BaseModel):
    user_id: constr(strict=True, min_length=1)
    email: Optional[str] = None
    user_type: SubjectType = SubjectType.user
    tenant_name: constr(strict=True, min_length=1)
    roles: List[str] = Field(default_factory=list)  # these are roles from auth server
    groups: List[str] = Field(
        default_factory=list
    )  # this is for team -  shall be populated in sfy-server from teams table
    is_super_admin: bool = False
    token: SecretStr

    def to_sfy_user_info_format(self):
        return {
            "userName": self.user_id,
            "email": self.email,
            "userType": self.user_type.value,
            "tenantName": self.tenant_name,
            "roles": self.roles,
            "groups": self.groups,
        }

    @classmethod
    def from_sfy_user_info_format(cls, user_dict: dict, token: str):
        return cls(
            user_id=user_dict["userName"],
            email=user_dict.get("email"),
            user_type=SubjectType[user_dict["userType"]],
            tenant_name=user_dict["tenantName"],
            roles=user_dict["roles"],
            token=token,
        )

    def __hash__(self):
        hashable_dict = {
            key: tuple(value) if isinstance(value, list) else value
            for key, value in self.__dict__.items()
        }
        return hash(tuple(sorted(hashable_dict.items())))
