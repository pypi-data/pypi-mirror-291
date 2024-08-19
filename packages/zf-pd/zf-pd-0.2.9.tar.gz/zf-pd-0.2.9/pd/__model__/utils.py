def parse_str_list_int(ctx, param, value) -> list[int]:
    if not value:
        return []
    delim = ' '
    if ',' in value:
        delim = ','
    elif 'x' in value:
        delim = 'x'
    return [int(s) for s in value.split(delim)]