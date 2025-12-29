from functions.get_files_info import get_files_info


def test():
    root = get_files_info("calculator", ".")
    print("Result for current directory:")
    print(root)

    pkg = get_files_info("calculator", "pkg")
    print("Result for 'pkg' directory:")
    print(pkg)

    bin = get_files_info("calculator", "/bin")
    print("Result for '/bin' directory:")
    print(f"    {bin}")

    external = get_files_info("calculator", "../")
    print("Result for '../' directory:")
    print(f"    {external}")


if __name__ == "__main__":
    test()
