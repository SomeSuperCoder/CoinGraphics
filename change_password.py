def search(list_: list[str], query: str) -> list[str]:
    result = []

    for i in list_:
        i2 = i.lower()
        query = query.lower()

        if query in i2:
            result.append(i)

    return result


if __name__ == "__main__":
    print(search(["Capybara", "Bara"], "bara"))


