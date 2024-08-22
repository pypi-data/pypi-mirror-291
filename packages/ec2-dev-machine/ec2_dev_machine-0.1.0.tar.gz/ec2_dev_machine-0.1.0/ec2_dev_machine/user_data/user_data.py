from pathlib import Path

from jinja2 import Template

from ec2_dev_machine.config import UserDataConfig

BASE_PATH = Path(__file__).parent.parent
USER_DATA_PATH = BASE_PATH / "user_data"


def generate_user_data_script(user_data_config: UserDataConfig) -> str:
    with open(USER_DATA_PATH / "setup.sh.template", "r") as f:
        user_data_script_template = Template(f.read())

    user_data_script = user_data_script_template.render(user_data_config.model_dump())

    return user_data_script
