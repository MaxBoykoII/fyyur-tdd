import enum


class Genres(enum.Enum):
    alternative = "Alternative"
    blues = "Blues"
    classical = "Classical"
    country = "Country"
    electronic = "Electronic"
    folk = "Folk"
    funk = "Funk"
    hip_hop = "Hip-Hop"
    heavy_metal = "Heavy Metal"
    instrumental = "Instrumental"
    jazz = "Jazz"
    musical_theatre = "Musical Theatre"
    pop = "Pop"
    punk = "Punk"
    r_b = "R&B"
    reggae = "Reggae"
    rock_n_roll = "Rock n Roll"
    soul = "Soul"
    other = "Other"


genres_list = [genre.value for genre in Genres]
