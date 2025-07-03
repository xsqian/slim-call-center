# Copyright 2023 Iguazio
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
import os
from pathlib import Path
import boto3
import mlrun

###########################
import os
import sys
import sqlalchemy
print(f'sqlalchemy version = {sqlalchemy.__version__}')
current_dir = os.path.dirname(os.path.abspath(__file__))
print(f'current dir = {current_dir}')
sys.path.insert(0, current_dir)
parent_dir = os.path.join(current_dir, os.pardir)
sys.path.insert(0, parent_dir)
parent_dir = os.path.join(parent_dir, os.pardir)
sys.path.insert(0, parent_dir)
print(f'parent dir = {parent_dir}')
print(f"Python version: {sys.version}")
print("sys.path:", sys.path)
print("PYTHONPATH (from environment):", os.environ.get('PYTHONPATH'))
###########################

from src.calls_analysis.db_management import create_tables
from src.common import ProjectSecrets

CE_MODE = mlrun.mlconf.is_ce_mode()

def setup(
    project: mlrun.projects.MlrunProject,
) -> mlrun.projects.MlrunProject:
    """
    Creating the project for the demo. This function is expected to call automatically when calling the function
    `mlrun.get_or_create_project`.

    :param project: The project to set up.

    :returns: A fully prepared project for this demo.
    """

    # Unpack parameters:
    source = project.get_param(key="source")
    default_image = project.get_param(key="default_image", default=None)
    build_image = project.get_param(key="build_image", default=False)
    default_image_name = project.get_param(key="default_image_name", default=f'.mlrun-project-image-{project.name}')
    print(f'default_image_name before = {default_image_name}')
    
    # Set the project git source:
    if source:
        print(f"Project Source: {source}")
        project.set_source(source=source, pull_at_runtime=True)

    # Set default image:
    if default_image:
        project.set_default_image(default_image)

    # Build the image:
    if build_image:
        print("Building default image for the demo:")
        default_image_name = _build_image(project=project)
    print(f'default_image_name after = {default_image_name}')

    # Refresh MLRun hub to the most up-to-date version:
    mlrun.get_run_db().get_hub_catalog(source_name="default", force_refresh=True)

    # Set the functions:
    _set_functions(project=project)


    # Set the workflows:
    _set_workflows(project=project, image=default_image_name)

    # Save and return the project:
    project.save()
    return project

def _build_image(project: mlrun.projects.MlrunProject):
    config = {
        "base_image": "mlrun/mlrun-kfp",
    }
    
    commands = [
        'python --version',
        'pip install SQLAlchemy==2.0.31',
        'pip list | grep SQLAlchemy'
    ]

    # Build the image
    result = project.build_image(
        base_image=config["base_image"],
        commands=commands,
        set_as_default=True,
        overwrite_build_params=True
    )
    print(f"build result = {result}")
    default_image_name = result.outputs["image"]
    return default_image_name


def _set_function(
        project: mlrun.projects.MlrunProject,
        func: str,
        name: str,
        kind: str,
        node_name: str = None,
        with_repo: bool = None,
        image: str = None,
        node_selector: dict = None,
        apply_auto_mount: bool = True,
):
    # Set the given function:

    mlrun_function = project.set_function(
        func=func, name=name, kind=kind, with_repo=with_repo, image=image,
    )

    # Save:
    mlrun_function.save()


def _set_functions(
    project: mlrun.projects.MlrunProject,
):

    # Conversation generator:
    _set_function(
        project=project,
        func="./src/printdummy.py",
        name="dummy",
        kind="job",
        apply_auto_mount=True,
    )


def _set_workflows(project: mlrun.projects.MlrunProject, image:str):
    project.set_workflow(
        name="dummy", workflow_path="./src/workflows/dummy.py", image=image
    )
