from dataclasses import dataclass, field, asdict
from typing import Set
from .role import Role


@dataclass
class Usuario:
    id: str
    discord_id: str = field(default=None)
    roles: Set[Role] = field(default_factory=set)

    def __post_init__(self):
        self.validate()

    def validate(self):
        if self.id == '':
            raise Exception('Id nao pode ser vazio')

    def grant_role(self, role: Role):
        self.roles.add(role)

    def revoke_role(self, role: Role):
        if role in self.roles:
            self.roles.remove(role)

    def subscribe(self, discord_id):
        if discord_id == '' or discord_id is None:
            raise Exception('Discord Id invalido')
        self.discord_id = discord_id

    def to_dict(self):
        return {
            '_id': self.id,
            'discord_id': self.discord_id,
            'roles': [role.name for role in self.roles]
        }

    @classmethod
    def from_dic(cls, result):
        return cls(id=result['_id'],
                   discord_id=result['discord_id'],
                   roles={Role[role] for role in result['roles']})
