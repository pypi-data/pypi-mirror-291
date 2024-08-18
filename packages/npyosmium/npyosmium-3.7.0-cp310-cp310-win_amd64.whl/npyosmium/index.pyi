from typing import List

import npyosmium.osm

class LocationTable:
    def clear(self) -> None: ...
    def get(self, id: int) -> npyosmium.osm.Location: ...
    def set(self, id: int, loc: npyosmium.osm.Location) -> None: ...
    def used_memory(self) -> int: ...

def create_map(map_type: str) -> LocationTable: ...
def map_types() -> List[str]: ...
