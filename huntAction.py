from dataclasses import dataclass, field,fields


@dataclass
class HuntAction:
    description:str = field(default="Hunt")
    action:str = field(default="hunt")




    