"""
This file is a typical example of a script used to run a LTL experiment. Read the comments in the file for more
explanations
"""

import logging.config
import os

from pypet import Environment
from pypet import pypetconstants

from ltl.optimizees.optimizee import Optimizee
from ltl.optimizers.optimizer import Optimizer, OptimizerParameters
from ltl.paths import Paths
# We first setup the logger and read the logging config which controls the verbosity and destination of the logs from
# various parts of the code.
from ltl.recorder import Recorder

from ltl.logging_tools import create_shared_logger_data, configure_loggers

logger = logging.getLogger('bin.ltl-optimizee-optimizer')


def main():
    # TODO when using the template: Give some *meaningful* name here
    name = 'LTL'

    # TODO when using the template: make a path.conf file and write the root path there
    try:
        with open('bin/path.conf') as f:
            root_dir_path = f.read().strip()
    except FileNotFoundError:
        raise FileNotFoundError(
            "You have not set the root path to store your results."
            " Write the path to a path.conf text file in the bin directory"
            " before running the simulation"
        )
    paths = Paths(name, dict(run_no='test'), root_dir_path=root_dir_path)

    # Load the logging config which tells us where and what to log (loglevel, destination)

    print("All output logs can be found in directory ", paths.logs_path)

    traj_file = os.path.join(paths.output_dir_path, 'data.h5')

    # Create an environment that handles running our simulation
    # This initializes a PyPet environment. See Pypet documentation for more details on environment and trajectory.
    # Uncomment 'freeze_input', 'multipproc', 'use_scoop' and 'wrap_mode' lines to disable running the experiment
    # across cores and nodes.
    env = Environment(trajectory=name, filename=traj_file, file_title='{} data'.format(name),
                      comment='{} data'.format(name),
                      add_time=True,
                      freeze_input=True,
                      multiproc=True,
                      use_scoop=True,
                      wrap_mode=pypetconstants.WRAP_MODE_LOCAL,
                      automatic_storing=True,
                      log_stdout=False,  # Sends stdout to logs
                      )
    create_shared_logger_data(logger_names=['bin', 'optimizers'],
                              log_levels=['INFO', 'INFO'],
                              log_to_consoles=[True, True],
                              sim_name=name,
                              log_directory=paths.logs_path)
    configure_loggers()

    # Get the trajectory from the environment.
    traj = env.trajectory

    ## Innerloop simulator
    # TODO when using the template: Change the optimizee to the appropriate Optimizee class
    optimizee = Optimizee(traj)

    ## Outerloop optimizer initialization
    # TODO when using the template: Change the optimizer to the appropriate Optimizer class
    # and use the right value for optimizee_fitness_weights. Length is the number of dimensions of fitness, and
    # negative value implies minimization and vice versa
    optimizer_parameters = OptimizerParameters()
    optimizer = Optimizer(traj, optimizee.create_individual, (1.0,), optimizer_parameters)

    # Add post processing
    env.add_postprocessing(optimizer.post_process)

    # Add Recorder
    # TODO: Change the names, ids and parameters passed in
    recorder = Recorder(trajectory=traj, optimizee_name='optimizee', optimizee_parameters=dict(),
                        optimizer_name=optimizer.__class__.__name__, optimizer_parameters=dict())
    recorder.start()

    # Run the simulation with all parameter combinations
    env.run(optimizee.simulate)

    ## Outerloop optimizer end
    optimizer.end(traj)

    recorder.end()

    # Finally disable logging and close all log-files
    env.disable_logging()


if __name__ == '__main__':
    main()
