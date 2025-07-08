
import kfp
import mlrun
from kfp import dsl

import os
import sys
print(os.getcwd())
print(kfp.__version__)

# current_dir = os.path.dirname(os.path.abspath(__file__))
# parent_dir = os.path.join(current_dir, os.pardir)
# sys.path.insert(0, parent_dir)
# parent_dir = os.path.join(parent_dir, os.pardir)
# sys.path.insert(0, parent_dir)
# print(f'parent dir = {parent_dir}')

from src import printdummy
printdummy.print_dummy()

from src.sub import printdummy
printdummy.print_dummy()

@kfp.dsl.pipeline()
def pipeline(generate_clients_and_agents: bool = True
):
    # Get the project:
    project = mlrun.get_current_project()

    with dsl.Condition(generate_clients_and_agents == True) as generate_data_condition:
        frun = project.run_function("printdummy")

    another_run = project.run_function("another-dummy")