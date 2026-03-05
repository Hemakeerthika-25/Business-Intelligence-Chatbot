from fuzzywuzzy import process


def match_column(user_input, columns):

    best_match, score = process.extractOne(user_input, columns)

    if score > 60:
        return best_match

    return None


def detect_groupby(user_input, columns):

    for col in columns:
        if col.lower() in user_input.lower():
            return col

    return None