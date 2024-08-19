import os
import subprocess
import tempfile
from typing import Optional

from .latex import recipe_to_latex
from .models import Recipe


def recipe_to_pdf(recipe, source_date_epoch: Optional[str] = "0") -> bytes:
    """
    Converts a `Recipe` object to a PDF using LaTeX and returns the PDF content as bytes.

    Args:
        recipe (Recipe): The `Recipe` object to be converted to PDF.
        source_date_epoch (Optional[str]): The value for SOURCE_DATE_EPOCH to enforce reproducible builds. Defaults to "0".

    Returns:
        bytes: The generated PDF content as bytes.
    """
    latex_content = recipe_to_latex(recipe)
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_file = os.path.join(temp_dir, 'recipe.tex')
        with open(temp_file, 'w') as f:
            f.write(latex_content)
        
        env = os.environ.copy()
        env["SOURCE_DATE_EPOCH"] = source_date_epoch
        env["FORCE_SOURCE_DATE"] = "1"
        
        subprocess_args = ["lualatex", "--shell-escape", temp_file, "-output-directory", temp_dir]
        subprocess.run(
            subprocess_args,
            cwd=temp_dir,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            env=env,
        )
        
        pdf_file = os.path.join(temp_dir, 'recipe.pdf')
        with open(pdf_file, 'rb') as f:
            return f.read()
