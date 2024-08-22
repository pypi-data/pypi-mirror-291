# __init__.py
from .image import *
from .lotto import *
from .names import *
from .file import *

__all__ = [
    "show_image",
    "get_one_number",
    "get_human_name",
    "get_social_security_number",
    "get_school_name",
    "get_country_name",
    "get_robot_name",
    "get_vehicle_company",
    "get_color_name",
    "get_colors",
    "get_one_set",
    "get_one_set_sorted",
    "get_one_set_string",
    "get_one_set_string_bracket",
    "get_some_sets",
    "get_file_name",
    "get_text"
]

# __all__ = image.__all__ + lotto.__all__ + names.__all__

__version__ = '0.0.14'