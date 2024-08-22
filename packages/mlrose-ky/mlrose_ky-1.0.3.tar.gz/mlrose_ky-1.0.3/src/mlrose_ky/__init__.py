"""MLROSe initialization file."""

# Authors: Genevieve Hayes (modified by Andrew Rollings, Kyle Nakamura)
# License: BSD 3-clause

from .algorithms.ga import genetic_alg
from .algorithms.sa import simulated_annealing
from .algorithms.hc import hill_climb
from .algorithms.rhc import random_hill_climb
from .algorithms.gd import gradient_descent
from .algorithms.mimic import mimic
from .algorithms.decay import GeometricDecay, ArithmeticDecay, ExponentialDecay, CustomDecay
from .algorithms.crossovers import OnePointCrossover, UniformCrossover, TSPCrossover
from .algorithms.mutators import SingleGeneMutator, DiscreteGeneMutator, GeneSwapMutator, SingleShiftMutator

from .fitness import (
    OneMax,
    FlipFlop,
    FourPeaks,
    SixPeaks,
    ContinuousPeaks,
    Knapsack,
    TravellingSalesperson,
    Queens,
    MaxKColor,
    CustomFitness,
)

from .neural import NeuralNetwork, LinearRegression, LogisticRegression, NNClassifier, nn_core
from .neural.activation import identity, relu, leaky_relu, sigmoid, softmax, tanh
from .neural.fitness import NetworkWeights
from .neural.utils.weights import flatten_weights, unflatten_weights

from .gridsearch import GridSearchMixin

from .opt_probs import DiscreteOpt, ContinuousOpt, KnapsackOpt, TSPOpt, QueensOpt, FlipFlopOpt, MaxKColorOpt

from .runners import GARunner, MIMICRunner, RHCRunner, SARunner, NNGSRunner, SKMLPRunner, build_data_filename

from .generators import MaxKColorGenerator, QueensGenerator, FlipFlopGenerator, TSPGenerator, KnapsackGenerator, ContinuousPeaksGenerator

from .samples import SyntheticDataGenerator, plot_synthetic_dataset
