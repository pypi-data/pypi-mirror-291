import os

from .config import template_config

from .generators import (
    generate_cmake,
    generate_header,
    generate_implementation,
    generate_tests,
)


def main():
    config = template_config.Config()

    if not os.path.exists("include"):
        os.makedirs("include")

    if not os.path.exists("src"):
        os.makedirs("src")

    if not os.path.exists("tests"):
        os.makedirs("tests")

    with open("CMakeLists.txt", "w") as f:
        f.write(generate_cmake.generate_cmake())

    with open(f"include/solution_{config.get_problem_number_config()}.h", "w") as f:
        header = generate_header.Header(config)
        f.write(header.get_header_template())

    with open("src/solution.cpp", "w") as f:
        implementation = generate_implementation.Implementation(config)
        f.write(implementation.get_implementation_template())

    with open("tests/tests.cpp", "w") as f:
        tests = generate_tests.Tests(config)
        f.write(tests.get_tests_template())


if __name__ == "__main__":
    main()
