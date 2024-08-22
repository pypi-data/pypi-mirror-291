"""
GridSearchMixin: A mixin providing grid search functionality for a neural network runner.

This mixin allows for parameter optimization through grid search, leveraging scikit-learn's
GridSearchCV for cross-validated search over parameter grids.
"""

import inspect
import numpy as np
import sklearn.metrics as skmt
import sklearn.model_selection as skms
from typing import Callable, Any


class GridSearchMixin:
    """
    A mixin class providing grid search capabilities using scikit-learn's GridSearchCV.

    Attributes
    ----------
    scorer_method : Callable
        The scoring method used for evaluating model performance during grid search.
    params : inspect.Signature
        The signature of the scoring method, used for validation and handling of additional arguments.
    get_y_argmax : bool
        Flag indicating whether to apply argmax to predictions and ground truths before scoring.
    """

    def __init__(self, scorer_method: Callable = None) -> None:
        """
        Initializes the GridSearchMixin with a specified scoring method.

        Parameters
        ----------
        scorer_method : Callable, optional
            A custom scoring method for evaluating the model. Defaults to balanced accuracy.
        """
        self.scorer_method: Callable = skmt.balanced_accuracy_score if scorer_method is None else scorer_method
        self.params: inspect.Signature = inspect.signature(self.scorer_method)
        self.get_y_argmax: bool = False

    def perform_grid_search(
        self, classifier: Any, x_train: np.ndarray, y_train: np.ndarray, cv: int, parameters: dict, n_jobs: int = 1, verbose: bool = False
    ) -> skms.GridSearchCV:
        """
        Perform grid search with cross-validation on the provided classifier.

        Parameters
        ----------
        classifier : Any
            The machine learning model or pipeline to optimize.
        x_train : np.ndarray
            Training data features.
        y_train : np.ndarray
            Training data labels.
        cv : int
            Number of cross-validation folds.
        parameters : dict
            Dictionary with parameters names as keys and lists of parameter settings to try as values.
        n_jobs : int, optional
            Number of jobs to run in parallel. Defaults to 1.
        verbose : bool, optional
            Whether to display verbose output during grid search. Defaults to False.

        Returns
        -------
        skms.GridSearchCV
            The fitted GridSearchCV object containing the results of the grid search.
        """
        scorer = self.make_scorer()
        search_results = skms.GridSearchCV(
            classifier, parameters, cv=cv, scoring=scorer, n_jobs=n_jobs, return_train_score=True, verbose=verbose
        )
        search_results.fit(x_train, y_train)
        return search_results

    def make_scorer(self) -> Callable:
        """
        Create a custom scorer function using the provided scoring method.

        Returns
        -------
        Callable
            A scorer callable suitable for use with scikit-learn's GridSearchCV.
        """
        return skmt.make_scorer(self._grid_search_score_intercept)

    def score(self, **kwargs: Any) -> float:
        """
        Calculate the score using the scoring method.

        Parameters
        ----------
        kwargs : dict
            Additional arguments to pass to the scoring method.

        Returns
        -------
        float
            The score calculated by the scoring method.
        """
        return self._grid_search_score_intercept(**kwargs)

    def _grid_search_score_intercept(self, y_pred: np.ndarray, y_true: np.ndarray, **kwargs: Any) -> float:
        """
        Intercept method for handling grid search scoring, accommodating special cases for prediction and true values.

        Parameters
        ----------
        y_pred : np.ndarray
            The predicted labels.
        y_true : np.ndarray
            The true labels.
        kwargs : dict
            Additional arguments to pass to the scoring method.

        Returns
        -------
        float
            The calculated score based on the predictions and true values.
        """
        cleaned_kwargs = {k: v for k, v in kwargs.items() if k in self.params.parameters}

        # Handle potential multi-class/multi-label cases
        if not self.get_y_argmax and y_pred.ndim > 1 and y_true.ndim > 1:
            try:
                return self.scorer_method(y_pred=y_pred, y_true=y_true, **cleaned_kwargs)
            except TypeError:
                self.get_y_argmax = True

        if self.get_y_argmax:
            y_pred = y_pred.argmax(axis=1)
            y_true = y_true.argmax(axis=1)

        try:
            return self.scorer_method(y_pred=y_pred, y_true=y_true, **cleaned_kwargs)
        except TypeError as e:
            raise ValueError(f"Error during scoring with method {self.scorer_method.__name__}: {e}") from e
