class MapType(Enum):
    ENTITY,
    BLOCK

class Mapping:
    def __init__(self, owner: MapType, subcommand: str, translatable: str):
        this.owner = owner
        this.subcommand = subcommand
        this.translatable = translatable
        
class Mappings:
    def __init__(self, mappings=[]):
        self.mappings = mappings
        
    def get_translatable(self, owner: MapType, subcommand: str):
        bucket = [i for i in self.mappings if i.owner == owner and i.subcommand == subcommand]
        return bucket[0] if len(bucket) > 0 else None