class System:
    def __init__(self, data: dict, base_url: str) -> None:
        self.name = data.get("name")
        self.full_name = data.get("fullname")
        self.hardware_type = data.get("hardwareType")
        self.manufacturer = data.get("manufacturer")
        self.release_year = data.get("releaseYear")
        self.visible = data.get("visible") == "true"
        self.total_games = data.get("totalGames")
        self.visible_games = data.get("visibleGames")
        self.favorite_games = data.get("favoriteGames")
        self.hidden_games = data.get("hiddenGames")
        self.logo_url = None
        if logo := data.get("logo"):
            self.logo_url = f"{base_url}{logo}"

    def __eq__(self, obj):
        if isinstance(obj, System):
            return self.name == obj.name
