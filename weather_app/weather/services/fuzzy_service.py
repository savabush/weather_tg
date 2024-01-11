from fuzzywuzzy import process


class FuzzyService:

    @classmethod
    def get_most_similar(cls, choices: list[str], text: str) -> str | None:
        extracted: tuple[str] = process.extractOne(text, choices)

        # Check if coincidence is more than 80%
        return extracted[0] if extracted[1] > 80 else None
