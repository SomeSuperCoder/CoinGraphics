
def search(the_dict: dict[str, str], query: str, search_sig_int) -> list[str]:
    result = []
    for obj in list(the_dict.values()):
        id = obj["id"]

        name2 = f"{obj.get('name')} {obj.get('id')}".lower()
        query = query.lower()

        if query in name2:
            result.append(id)
        if search_sig_int.val:
            return

    return result
