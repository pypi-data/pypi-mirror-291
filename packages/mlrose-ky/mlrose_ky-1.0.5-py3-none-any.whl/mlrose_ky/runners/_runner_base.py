"""Base class for managing and running optimization experiments with logging, error handling, and result saving."""

from abc import ABC, abstractmethod
import time
import os
import logging
import itertools as it
from typing import Any

import numpy as np
import pandas as pd
import pickle as pk
import inspect as lk
import signal
import multiprocessing
import ctypes

from mlrose_ky.decorators import get_short_name
from mlrose_ky.runners.utils import build_data_filename


class _RunnerBase(ABC):
    """
    Abstract base class for running and managing optimization experiments.

    This class provides a framework for setting up, running, and managing the lifecycle
    of optimization experiments. It handles tasks such as logging, error handling,
    signal interruption, dynamic naming, and result saving to both pickle and CSV files.
    The class is designed to be extended by concrete subclasses that implement the
    `run` method, which defines the specific behavior of the experiment.

    Attributes
    ----------
    _abort_flag : multiprocessing.Value
        A flag used to signal if the experiment should be aborted.
    _spawn_count : multiprocessing.Value
        A counter to track the number of active spawns of the runner.
    _replay_mode : multiprocessing.Value
        A flag to indicate if replay mode is enabled, which reuses previous results.
    _original_sigint_handler : Any
        The original signal handler for SIGINT, used to restore it after interruption.
    _sigint_params : tuple[int, Any] | None
        Parameters captured when a SIGINT is received to allow for graceful shutdown.

    Parameters
    ----------
    problem : Any
        The optimization problem to be solved.
    experiment_name : str
        A name for the experiment, used for logging and file naming.
    seed : int
        A random seed to ensure reproducibility.
    iteration_list : list[int]
        A list of iteration numbers at which to capture results.
    max_attempts : int, optional
        The maximum number of attempts allowed per iteration (default is 500).
    generate_curves : bool, optional
        Whether to generate and save fitness curves (default is True).
    output_directory : str | None, optional
        The directory where results will be saved. If None, results are not saved (default is None).
    copy_zero_curve_fitness_from_first : bool, optional
        Whether to copy the fitness value from the first curve to the zeroth iteration (default is False).
    replay : bool, optional
        Whether to enable replay mode, which reuses previous results if available (default is False).
    override_ctrl_c_handler : bool, optional
        Whether to override the Ctrl-C handler to enable graceful shutdown (default is True).
    **kwargs : Any
        Additional keyword arguments passed to the algorithm.
    """

    _abort_flag: multiprocessing.Value = multiprocessing.Value(ctypes.c_bool)
    _spawn_count: multiprocessing.Value = multiprocessing.Value(ctypes.c_uint)
    _replay_mode: multiprocessing.Value = multiprocessing.Value(ctypes.c_bool)
    _original_sigint_handler: Any = None
    _sigint_params: tuple[int, Any] = None

    @classmethod
    def get_runner_name(cls) -> str:
        """
        Get a short name for the runner class.

        Returns
        -------
        str
            Short name of the runner class.
        """
        runner_name = get_short_name(cls)
        return runner_name

    def get_dynamic_runner_name(self) -> str:
        """
        Get the dynamic name of the runner, if set, otherwise return the default runner name.

        Returns
        -------
        str
            Dynamic or default runner name.
        """
        dynamic_runner_name = self._dynamic_short_name or self.get_runner_name()
        if not dynamic_runner_name:
            raise ValueError("dynamic_runner_name is None")
        return dynamic_runner_name

    def set_dynamic_runner_name(self, name: str) -> None:
        """
        Set a dynamic runner name.

        Parameters
        ----------
        name : str
            The dynamic name to set for the runner.
        """
        self._dynamic_short_name = name

    @staticmethod
    def _print_banner(text: str) -> None:
        """
        Print a banner with the provided text.

        Parameters
        ----------
        text : str
            The text to display in the banner.
        """
        logging.info("*" * len(text))
        logging.info(text)
        logging.info("*" * len(text))

    @staticmethod
    def _sanitize_value(value: Any) -> str:
        """
        Sanitize the value for logging purposes.

        Parameters
        ----------
        value : Any
            The value to sanitize.

        Returns
        -------
        str
            The sanitized string representation of the value.
        """
        if isinstance(value, (tuple, list)):
            sanitized_value = str(value)
        elif isinstance(value, np.ndarray):
            sanitized_value = str(list(value))
        elif callable(value):
            sanitized_value = get_short_name(value)
        else:
            sanitized_value = str(value)  # Handle non-callable types like floats, ints, etc.
        return sanitized_value

    @abstractmethod
    def run(self) -> None:
        """
        Abstract method to be implemented by subclasses.
        """
        pass

    def __init__(
        self,
        problem: Any,
        experiment_name: str,
        seed: int,
        iteration_list: list[int],
        max_attempts: int = 500,
        generate_curves: bool = True,
        output_directory: str = None,
        copy_zero_curve_fitness_from_first: bool = False,
        replay: bool = False,
        override_ctrl_c_handler: bool = True,
        **kwargs: Any,
    ) -> None:
        self.problem = problem
        self.seed = seed
        self.iteration_list = iteration_list
        self.max_attempts = max_attempts
        self.generate_curves = generate_curves
        self.parameter_description_dict: dict[str, str] = {}
        self.override_ctrl_c_handler = override_ctrl_c_handler

        self.run_stats_df: pd.DataFrame | None = None
        self.curves_df: pd.DataFrame | None = None
        self._raw_run_stats: list[dict[str, Any]] = []
        self._fitness_curves: list[dict[str, Any]] = []
        self._curve_base = 0
        self._copy_zero_curve_fitness_from_first = copy_zero_curve_fitness_from_first
        self._copy_zero_curve_fitness_from_first_original = copy_zero_curve_fitness_from_first
        self._extra_args = kwargs
        self._output_directory: str | None = output_directory
        self._dynamic_short_name: str | None = None
        self._experiment_name: str = experiment_name
        self._current_logged_algorithm_args: dict[str, Any] = {}
        self._run_start_time: float | None = None
        self._iteration_times: list[float] = []
        self._first_curve_synthesized = False
        if replay:
            self.set_replay_mode()
        self._increment_spawn_count()

    def _increment_spawn_count(self) -> None:
        """
        Increment the spawn count for the runner.
        """
        with self._spawn_count.get_lock():
            self._spawn_count.value += 1

    def _decrement_spawn_count(self) -> None:
        """
        Decrement the spawn count for the runner.
        """
        with self._spawn_count.get_lock():
            self._spawn_count.value -= 1

    def get_spawn_count(self) -> int:
        """
        Get the current spawn count for the runner.

        Returns
        -------
        int
            The current spawn count.
        """
        self._print_banner(f"*** Spawn Count Remaining: {self._spawn_count.value} ***")
        return self._spawn_count.value

    def abort(self) -> None:
        """
        Set the abort flag to True, indicating the runner should stop execution.
        """
        self._print_banner("*** ABORTING ***")
        with self._abort_flag.get_lock():
            self._abort_flag.value = True

    def has_aborted(self) -> bool:
        """
        Check if the abort flag is set.

        Returns
        -------
        bool
            True if the runner has been aborted, False otherwise.
        """
        return self._abort_flag.value

    def set_replay_mode(self, value: bool = True) -> None:
        """
        Set the replay mode for the runner.

        Parameters
        ----------
        value : bool, optional
            Whether to enable replay mode, by default True.
        """
        with self._replay_mode.get_lock():
            self._replay_mode.value = value

    def replay_mode(self) -> bool:
        """
        Check if replay mode is enabled.

        Returns
        -------
        bool
            True if replay mode is enabled, False otherwise.
        """
        return self._replay_mode.value

    def _setup(self) -> None:
        """
        Set up the runner before starting an experiment.
        """
        self._raw_run_stats = []
        self._fitness_curves = []
        self._curve_base = 0

        self._iteration_times = []
        self._copy_zero_curve_fitness_from_first = self._copy_zero_curve_fitness_from_first_original
        self._current_logged_algorithm_args.clear()
        if self._output_directory is not None:
            if not os.path.exists(self._output_directory):
                os.makedirs(self._output_directory)

        # Set up Ctrl-C handler
        if self.override_ctrl_c_handler:
            if self._original_sigint_handler is None:
                self._original_sigint_handler = signal.getsignal(signal.SIGINT)
                signal.signal(signal.SIGINT, self._ctrl_c_handler)

    def _ctrl_c_handler(self, sig: int, frame: Any) -> None:
        """
        Ctrl-C signal handler to save progress on interruption.

        Parameters
        ----------
        sig : int
            Signal number.
        frame : Any
            Current stack frame.
        """
        logging.info("Interrupted - saving progress so far")
        self._sigint_params = (sig, frame)
        self.abort()

    def _tear_down(self) -> None:
        """
        Tear down the runner after finishing an experiment.
        """
        if not self.override_ctrl_c_handler:
            return
        try:
            # Restore Ctrl-C handler
            self._decrement_spawn_count()
            if self._original_sigint_handler is not None:
                signal.signal(signal.SIGINT, self._original_sigint_handler)
                if self.has_aborted() and self.get_spawn_count() == 0:
                    sig, frame = self._sigint_params
                    self._original_sigint_handler(sig, frame)
        except (ValueError, TypeError, AttributeError, Exception) as e:
            logging.error(f"Problem restoring SIGINT handler: {e}")

    def log_current_argument(self, arg_name: str, arg_value: Any) -> None:
        """
        Log the current argument being passed to the algorithm.

        Parameters
        ----------
        arg_name : str
            The name of the argument.
        arg_value : Any
            The value of the argument.
        """
        self._current_logged_algorithm_args[arg_name] = arg_value

    def run_experiment(self, algorithm: Any, **kwargs: Any) -> tuple[pd.DataFrame | None, pd.DataFrame | None]:
        """
        Run the experiment using the provided algorithm.

        Parameters
        ----------
        algorithm : Any
            The algorithm to run.
        **kwargs : Any
            Additional keyword arguments for the algorithm.

        Returns
        -------
        tuple[pd.DataFrame | None, pd.DataFrame | None]
            The run statistics DataFrame and fitness curves DataFrame.
        """
        self._setup()
        # Extract loop params
        values = [([(k, v) for v in vs]) for (k, (n, vs)) in kwargs.items() if vs is not None]
        self.parameter_description_dict = {k: n for (k, (n, vs)) in kwargs.items() if vs is not None}
        value_sets = list(it.product(*values))

        logging.info(f"Running {self.get_dynamic_runner_name()}")
        run_start = time.perf_counter()
        for value_set in value_sets:
            total_args = dict(value_set)
            if "max_iters" not in total_args:
                total_args["max_iters"] = int(max(self.iteration_list))

            self._run_one_experiment(algorithm, total_args)

        run_end = time.perf_counter()
        logging.info(f"Run time: {run_end - run_start:.2f} seconds")

        self._create_and_save_run_data_frames(final_save=True)
        self._tear_down()

        return self.run_stats_df, self.curves_df

    def _run_one_experiment(self, algorithm: Any, total_args: dict[str, Any], **params: Any) -> None:
        """
        Run a single experiment iteration.

        Parameters
        ----------
        algorithm : Any
            The algorithm to run.
        total_args : dict[str, Any]
            The total arguments to pass to the algorithm.
        **params : Any
            Additional parameters for the experiment.
        """
        if self._extra_args:
            total_args.update(self._extra_args)
        total_args.update(params)

        user_info = [(k, v) for k, v in total_args.items()]
        self._invoke_algorithm(
            algorithm=algorithm,
            problem=self.problem,
            max_attempts=self.max_attempts,
            curve=self.generate_curves,
            user_info=user_info,
            **total_args,
        )

    def _create_and_save_run_data_frames(self, extra_data_frames: dict[str, pd.DataFrame] = None, final_save: bool = False) -> None:
        """
        Create and save the run statistics and fitness curves as DataFrames.

        Parameters
        ----------
        extra_data_frames : dict[str, pd.DataFrame], optional
            Additional data frames to save, by default None.
        final_save : bool, optional
            Whether this is the final save, by default False.
        """
        self.run_stats_df = pd.DataFrame(self._raw_run_stats)
        self.curves_df = pd.DataFrame(self._fitness_curves)
        if self._output_directory:
            if not self.run_stats_df.empty:
                self._dump_df_to_disk(self.run_stats_df, df_name="run_stats_df", final_save=final_save)
            if self.generate_curves and not self.curves_df.empty:
                self._dump_df_to_disk(self.curves_df, df_name="curves_df", final_save=final_save)
            if isinstance(extra_data_frames, dict):
                for name, df in extra_data_frames.items():
                    self._dump_df_to_disk(df, df_name=name, final_save=final_save)

    def _dump_df_to_disk(self, df: pd.DataFrame, df_name: str, final_save: bool = False) -> None:
        """
        Dump the DataFrame to disk as both pickle and CSV files.

        Parameters
        ----------
        df : pd.DataFrame
            The DataFrame to save.
        df_name : str
            The name of the DataFrame.
        final_save : bool, optional
            Whether this is the final save, by default False.
        """
        filename_root = self._dump_pickle_to_disk(object_to_pickle=df, name=df_name)
        df.to_csv(f"{filename_root}.csv")
        if final_save:
            logging.info(f"Saved: [{filename_root}.csv]")

    def _get_pickle_filename_root(self, name: str) -> str:
        """
        Get the root filename for the pickle file.

        Parameters
        ----------
        name : str
            The name of the DataFrame.

        Returns
        -------
        str
            The root filename for the pickle file.
        """
        filename_root = build_data_filename(
            output_directory=self._output_directory,
            runner_name=self.get_dynamic_runner_name(),
            experiment_name=self._experiment_name,
            df_name=name,
        )
        return filename_root

    def _dump_pickle_to_disk(self, object_to_pickle: Any, name: str, final_save: bool = False) -> str | None:
        """
        Dump an object to disk as a pickle file.

        Parameters
        ----------
        object_to_pickle : Any
            The object to pickle.
        name : str
            The name of the object.
        final_save : bool, optional
            Whether this is the final save, by default False.

        Returns
        -------
        str | None
            The root filename for the pickle file.
        """
        if self._output_directory is None:
            return None
        filename_root = self._get_pickle_filename_root(name)
        pk.dump(object_to_pickle, open(f"{filename_root}.p", "wb"))
        if final_save:
            logging.info(f"Saved: [{filename_root}.p]")
        return filename_root

    def _load_pickles(self) -> bool:
        """
        Load the fitness curves and run statistics DataFrames from pickle files.

        Returns
        -------
        bool
            True if both DataFrames were successfully loaded, False otherwise.
        """
        curves_df_filename = f"{self._get_pickle_filename_root('curves_df')}.p"
        run_stats_df_filename = f"{self._get_pickle_filename_root('run_stats_df')}.p"

        self.curves_df = None
        self.run_stats_df = None

        if os.path.exists(curves_df_filename):
            with open(curves_df_filename, "rb") as pickle_file:
                try:
                    self.curves_df = pk.load(pickle_file)
                except (OSError, IOError, pk.PickleError):
                    pass

        if os.path.exists(run_stats_df_filename):
            with open(run_stats_df_filename, "rb") as pickle_file:
                try:
                    self.run_stats_df = pk.load(pickle_file)
                except (OSError, IOError, pk.PickleError):
                    pass

        return self.curves_df is not None and self.run_stats_df is not None

    def _invoke_algorithm(
        self,
        algorithm: Any,
        problem: Any,
        max_attempts: int,
        curve: bool,
        user_info: list[tuple[str, Any]],
        additional_algorithm_args: dict[str, Any] = None,
        **total_args: Any,
    ) -> tuple[None, None, None] | None:
        """
        Invoke the algorithm with the provided parameters.

        Parameters
        ----------
        algorithm : Any
            The algorithm to run.
        problem : Any
            The problem instance to solve.
        max_attempts : int
            The maximum number of attempts allowed.
        curve : bool
            Whether to generate fitness curves.
        user_info : list[tuple[str, Any]]
            Additional user information to log.
        additional_algorithm_args : dict[str, Any] | None, optional
            Additional arguments for the algorithm, by default None.
        **total_args : Any
            Total arguments to pass to the algorithm.

        Returns
        -------
        tuple[None, None, None] | None
            None if the algorithm was run, or the loaded pickles if replay mode was enabled.
        """
        self._current_logged_algorithm_args.update(total_args)
        if additional_algorithm_args is not None:
            self._current_logged_algorithm_args.update(additional_algorithm_args)

        if self.replay_mode() and self._load_pickles():
            return None, None, None

        self._print_banner("*** Run START ***")
        np.random.seed(self.seed)

        valid_args = [k for k in lk.signature(algorithm).parameters]
        args_to_pass = {k: v for k, v in total_args.items() if k in valid_args}

        self.start_run_timing()
        problem.reset()
        result = algorithm(
            problem=problem,
            max_attempts=max_attempts,
            curve=curve,
            random_state=self.seed,
            state_fitness_callback=self.save_state,
            callback_user_info=user_info,
            **args_to_pass,
        )

        self._print_banner("*** Run END ***")
        self._curve_base = len(self._fitness_curves)

        return result

    def start_run_timing(self) -> None:
        """
        Start timing the experiment run.
        """
        self._run_start_time = time.perf_counter()

    @staticmethod
    def _create_curve_stat(
        iteration: int, curve_value: tuple[float, int] | dict[str, Any], curve_data: dict[str, Any], t: float = None
    ) -> dict[str, Any]:
        """
        Create a single fitness curve statistic.

        Parameters
        ----------
        iteration : int
            The iteration number.
        curve_value : tuple[float, int] | dict[str, Any]
            The curve value containing fitness and evaluations.
        curve_data : dict[str, Any]
            Additional data to log.
        t : float | None, optional
            Time elapsed, by default None.

        Returns
        -------
        dict[str, Any]
            The fitness curve statistic as a dictionary.
        """
        curve_fitness_value, curve_feval_value = curve_value
        curve_stat = {"Iteration": iteration, "Time": t, "Fitness": curve_fitness_value, "FEvals": curve_feval_value}

        curve_stat.update(curve_data)
        if isinstance(curve_value, dict):
            curve_stat.update(curve_value)

        return curve_stat

    def save_state(
        self,
        iteration: int,
        state: Any,
        fitness: float,
        user_data: list[tuple[str, Any]],
        attempt: int = 0,
        done: bool = False,
        curve: list[tuple[float, int]] = None,
        fitness_evaluations: int = None,
    ) -> bool:
        """
        Save the state of the experiment during execution.

        Parameters
        ----------
        iteration : int
            The current iteration number.
        state : Any
            The current state of the problem.
        fitness : float
            The fitness value of the state.
        user_data : list[tuple[str, Any]]
            Additional user data to log.
        attempt : int, optional
            The current attempt number, by default 0.
        done : bool, optional
            Whether the experiment is done, by default False.
        curve : list[tuple[float, int]] | None, optional
            The fitness curve, by default None.
        fitness_evaluations : int | None, optional
            The number of fitness evaluations, by default None.

        Returns
        -------
        bool
            True if the experiment should continue, False otherwise.
        """
        # Log iteration timing
        end = time.perf_counter()
        t = end - self._run_start_time
        self._iteration_times.append(t)

        if iteration > 0 and iteration not in self.iteration_list and not done:
            return True

        display_data = {**self._current_logged_algorithm_args}
        if user_data:
            display_data.update({n: v for n, v in user_data})
            data_desc = ", ".join([f"{n}:[{get_short_name(v)}]" for n, v in display_data.items()])
            logging.debug(data_desc)
        logging.debug(
            f"runner_name:[{self.get_dynamic_runner_name()}], experiment_name:[{self._experiment_name}], "
            + ("" if attempt is None else f"attempt:[{attempt}], ")
            + f"iteration:[{iteration}], done:[{done}], "
            f"time:[{t:.2f}], fitness:[{fitness:.4f}]"
        )

        state_string = str(state).replace("\n", "//")[:200]
        logging.debug(f"\t{state_string}...")
        logging.debug("")

        # noinspection PyMissingOrEmptyDocstring
        def get_description(name: str) -> str:
            return name if name not in self.parameter_description_dict else self.parameter_description_dict[name]

        # noinspection PyMissingOrEmptyDocstring
        def get_info(val: Any) -> dict[str, Any]:
            return val.get_info__(t) if hasattr(val, "get_info__") else {}

        current_iteration_stats = {str(get_description(k)): self._sanitize_value(v) for k, v in self._current_logged_algorithm_args.items()}
        current_iteration_stats.update({str(get_description(k)): self._sanitize_value(v) for k, v in user_data})

        additional_info = {
            k: self._sanitize_value(v)
            for info_dict in (get_info(v) for v in current_iteration_stats.values())
            for k, v in info_dict.items()
        }

        if iteration > 0:
            remaining_iterations = [i for i in self.iteration_list if i >= iteration]
            iterations = [min(remaining_iterations)] if not done else remaining_iterations
        else:
            iterations = [0]

        for i in iterations:
            run_stat = {"Iteration": i, "Fitness": fitness, "FEvals": fitness_evaluations, "Time": t, "State": self._sanitize_value(state)}
            run_stat.update(additional_info)
            run_stat.update(current_iteration_stats)
            self._raw_run_stats.append(run_stat)

        if self.generate_curves and iteration == 0:
            # Capture first fitness value for iteration 0 if not already captured.
            if not curve:
                curve = [(fitness, fitness_evaluations)]
                self._first_curve_synthesized = True

        if self.generate_curves and curve:  # and (done or iteration == max(self.iteration_list)):
            curve_stats_saved = len(self._fitness_curves)
            total_curve_stats = self._curve_base + len(curve)
            curve_stats_to_save = total_curve_stats - curve_stats_saved
            if self._first_curve_synthesized:
                curve_stats_to_save += 1
            ix_end = iteration + 1
            ix_start = ix_end - curve_stats_to_save
            if ix_start < 0:
                ix_start = 0

            curve_tuples = list(zip(range(ix_start, ix_end), curve[-curve_stats_to_save:]))

            curve_stats = [
                self._create_curve_stat(iteration=ix, curve_value=f, curve_data=current_iteration_stats, t=self._iteration_times[ix])
                for ix, f in curve_tuples
            ]

            self._fitness_curves.extend(curve_stats)

            if self._copy_zero_curve_fitness_from_first and len(self._fitness_curves) > 1:
                self._fitness_curves[0]["Fitness"] = self._fitness_curves[1]["Fitness"]
                self._copy_zero_curve_fitness_from_first = False
            self._create_and_save_run_data_frames()

        return not (self.has_aborted() or done)
