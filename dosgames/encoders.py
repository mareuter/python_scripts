import dataclasses


@dataclasses.dataclass
class GameInformation:
    key: str
    full_name: str
    directory: str
    executable: str
    categories: list
    media: list
    media_type: str
    media_only: bool
    extra_profiles: list

    def listing(self) -> str:
        return f"{self.key}: {self.full_name}"


def decode_game_information(dct):
    return GameInformation(
        dct["key"],
        dct["full_name"],
        dct["directory"],
        dct["executable"],
        dct["categories"],
        dct.get("media", None),
        dct.get("media_type", None),
        dct.get("media_only", False),
        dct.get("extra_profiles", None),
    )
