import leetcode_template.config.template_config as template_config


class Tests:
    def __init__(self, config: template_config.Config):
        self.config = config
        self.TEST_TEMPLATE = f"""#include "solution_{self.config.get_problem_number_config()}.h"
#include <gtest/gtest.h>

#define SUITE_NAME Test{self.config.get_problem_number_config()}

using namespace std;

"""

    def get_tests_template(self):
        tests = self.TEST_TEMPLATE
        for test_arr in self.config.get_test_cases_config():
            tests += f"""TEST(SUITE_NAME, {test_arr["testName"]}) {{
  {"\n  ".join(test_arr["input"])}

  ASSERT_EQ(Solution::{self.config.get_function_name_config()}({", ".join(test_arr["inputParams"])}), {test_arr["expectedOutput"]}) << "Assertion Failed";
}}

"""

        return tests
