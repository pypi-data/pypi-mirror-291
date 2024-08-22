class Game:
    def __init__(self, data: dict, base_url: str) -> None:
        self.id = data.get("id")
        self.path = data.get("path")
        self.name = data.get("name")
        self.system_name = data.get("systemName")
        self.rating = data.get("rating")
        self.favorite = data.get("favorite") == "true"
        self.hidden = data.get("hidden") == "true"
        self.image_id = data.get("image")
        self.image_url = f"{base_url}{self.image_id}" if self.image_id else None

    def __eq__(self, obj):
        if isinstance(obj, Game):
            return self.id == obj.id
