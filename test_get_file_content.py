from functions.get_file_content import get_file_content


def test():
    result = get_file_content("calculator", "lorem.txt")
    tail_line = result.split("[")[-1]
    print(f"{len(result)}-- {tail_line}")
    print("")

    result = get_file_content("calculator", "main.py")
    # tail_line = result.split("[")[-1]
    print(result)
    print("")

    result = get_file_content("calculator", "pkg/calculator.py")
    # tail_line = result.split("[")[-1]
    print(result)
    print("")

    bin = get_file_content("calculator", "/bin/cat")
    print(bin)
    print("")

    bin = get_file_content("calculator", "pkg/does_not_exist.py")
    print(bin)

    # bin = get_files_info("calculator", "/bin")
    # print("Result for '/bin' directory:")
    # print(f"    {bin}")

    # external = get_files_info("calculator", "../")
    # print("Result for '../' directory:")
    # print(f"    {external}")


if __name__ == "__main__":
    test()
