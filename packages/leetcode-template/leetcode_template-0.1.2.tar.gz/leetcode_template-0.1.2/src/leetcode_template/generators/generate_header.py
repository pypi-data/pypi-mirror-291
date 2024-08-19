import leetcode_template.config.template_config as template_config


class Header:
    def __init__(self, config: template_config.Config):
        self.config = config

    def get_header_template(self):
        HEADER_TEMPLATE = f"""
#ifndef SOLUTION_{self.config.get_problem_number_config()}_H

{self.config.get_include_list()}


class Solution {{
public:
  static {self.config.get_function_signature()};
}};

#endif // SOLUTION_{self.config.get_problem_number_config()}_H

"""
        return HEADER_TEMPLATE
