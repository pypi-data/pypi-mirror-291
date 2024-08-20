def generate_cmake():
    CMAKELISTS_TEMPLATE = """# set the project name to the name of the current directory
get_filename_component(PROJECT_NAME ${CMAKE_CURRENT_SOURCE_DIR} NAME)


# set source files
set(SOURCE_DIR "src")
file(GLOB_RECURSE SOURCES "${SOURCE_DIR}/*.cpp")


# set test files
set(TEST_DIR "tests")
file(GLOB_RECURSE TEST_SOURCES "${TEST_DIR}/test*.cpp")

# set include directories
include_directories("include")


include(FetchContent)
        FetchContent_Declare(
          googletest
          URL https://github.com/google/googletest/archive/b514bdc898e2951020cbdca1304b75f5950d1f59.zip
        )
        # For Windows: Prevent overriding the parent project's compiler/linker settings
        set(gtest_force_shared_crt ON CACHE BOOL "" FORCE)
        FetchContent_MakeAvailable(googletest)
        
add_compile_options(-fsanitize=address)
add_link_options(-fsanitize=address)

enable_testing()

include(GoogleTest)

foreach(TEST_SOURCE ${TEST_SOURCES})
    get_filename_component(TEST_NAME ${TEST_SOURCE} NAME_WE)
    add_executable(${PROJECT_NAME}_${TEST_NAME} ${TEST_SOURCE} ${SOURCES})
    target_link_libraries(${PROJECT_NAME}_${TEST_NAME} gtest_main)
    gtest_discover_tests(${PROJECT_NAME}_${TEST_NAME})
endforeach()
"""

    return CMAKELISTS_TEMPLATE
