def search(the_dict: dict[str, str], query: str) -> list[str]:
    result = []

    for id, name in the_dict.items():
        name2 = name.lower()
        query = query.lower()

        if query in name2:
            result.append(id)

    return result


if __name__ == "__main__":
    print(search(["Capybara", "Bara"], "bara"))


