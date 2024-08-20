import leetcode_template.config.template_config as template_config


class Implementation:
    def __init__(self, config: template_config.Config):
        self.config = config

    def get_implementation_template(self):
        IMPLEMENTATION_TEMPLATE = f"""#include "solution_{self.config.get_problem_number_config()}.h"

using namespace std;

{self.config.get_impl_function_declaration()} {{
    // your code here
    
    return {self.config.get_return_type_config()}();
}}
"""
        return IMPLEMENTATION_TEMPLATE
