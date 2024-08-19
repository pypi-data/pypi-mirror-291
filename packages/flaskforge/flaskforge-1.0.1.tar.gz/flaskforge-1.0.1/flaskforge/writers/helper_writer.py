import os

from flaskforge.utils.commons import join_path
from .base_writer import AbstractWriter


class HelperWriter(AbstractWriter):
    """
    A writer for generating helper utility files.

    This class inherits from `AbstractWriter` and is responsible for creating
    and writing helper utility files to the specified directory.

    Attributes:
        type (str): The type of writer, set to "helper".
    """

    type = "helper"

    def __init__(self, args: object, **kwargs):
        """
        Initialize the HelperWriter with project-specific details.

        Args:
            args (object): Arguments object containing project details.
            **kwargs: Additional keyword arguments.

        TODO:
            - Validate the `args` object to ensure it contains the necessary attributes.
        """
        self.args = args
        self.project = self.args.project

        self.project_path = join_path(self.project_root, self.project)
        self.helper_path = join_path(self.project_path, "utils")
        self.helper = join_path(self.package_root, "bases", "base_helper.py")

    def write_source(self):
        """
        Create the helper utility directory and write the helper source file.

        If the helper directory does not exist, it is created. Then, the
        helper source file is written using the source code from the base helper.

        TODO:
            - Add error handling for directory creation and file writing operations.
            - Implement logging to track the creation and writing process.
        """
        if not os.path.exists(self.helper_path):
            os.makedirs(self.helper_path)

        gitignore = f"""
*.pyc
__pycache__
"""

        self.write(join_path(self.helper_path, "helper.py"), self.get_source())
        self.write(join_path(self.project_path, ".gitignore"), gitignore)

    def get_source(self) -> str:
        """
        Retrieve the source code for the helper utility.

        Reads the source code from the base helper file and formats it.

        Returns:
            str: The formatted source code.

        TODO:
            - Handle cases where the base helper file might not exist or is inaccessible.
            - Consider adding more robust error handling for file reading operations.
        """
        with open(self.helper) as reader:
            source_code = reader.read()

        return self.format(source_code)
