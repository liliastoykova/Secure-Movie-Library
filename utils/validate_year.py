from datetime import datetime

def validate_release_year(year: int | None):
    first_movie = 1888
    current_year = datetime.now().year
    if year is None:
        return None
    elif year < first_movie or year > current_year:
        raise ValueError(f"The release year should be between {first_movie} and {current_year}")

    return year