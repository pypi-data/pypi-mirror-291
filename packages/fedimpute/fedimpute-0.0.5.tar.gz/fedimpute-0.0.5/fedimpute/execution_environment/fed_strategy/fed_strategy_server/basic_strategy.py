from typing import List, Tuple, Union
from copy import deepcopy
from collections import OrderedDict
import numpy as np


class CentralStrategyServer:

    def __init__(self):
        self.initial_impute = 'central'
        self.name = 'central'
        self.fine_tune_epochs = 0

    def aggregate_parameters(
            self, local_model_parameters: List[OrderedDict], fit_res: List[dict], params: dict, *args, **kwargs
    ) -> Tuple[List[OrderedDict], dict]:
        """
        Aggregate local models
        :param local_model_parameters: List of local model parameters
        :param fit_res: List of fit results of local training
            - sample_size: int - number of samples used for training
        :param params: dictionary for information
        :param args: other params list
        :param kwargs: other params dict
        :return: List of aggregated model parameters, dict of aggregated results
        """
        central_model_params = local_model_parameters[-1]

        agg_model_parameters = [deepcopy(central_model_params) for _ in range(len(local_model_parameters))]
        agg_res = {}

        return agg_model_parameters, agg_res

    def fit_instruction(self, params_list: List[dict]) -> List[dict]:
        fit_instructions = []
        for _ in range(len(params_list) - 1):
            fit_instructions.append({'fit_model': False})

        fit_instructions.append({'fit_model': True})

        return fit_instructions

    def update_instruction(self, params: dict) -> dict:

        return {}


class LocalStrategyServer:

    def __init__(self):
        self.name = 'local'
        self.initial_impute = 'local'
        self.fine_tune_epochs = 0

    def aggregate_parameters(
            self, local_model_parameters: List[OrderedDict], fit_res: List[dict], params: dict, *args, **kwargs
    ) -> Tuple[List[Union[OrderedDict, None]], dict]:
        """
        Aggregate local models
        :param local_model_parameters: List of local model parameters
        :param fit_res: List of fit results of local training
            - sample_size: int - number of samples used for training
        :param params: dictionary for information
        :param args: other params list
        :param kwargs: other params dict
        :return: List of aggregated model parameters, dict of aggregated results
        """
        return [None for _ in range(len(local_model_parameters))], {}


    def fit_instruction(self, params_list: List[dict]) -> List[dict]:

        return [{'fit_model': True} for _ in range(len(params_list))]

    def update_instruction(self, params: dict) -> dict:
        return {}


class SimpleAvgStrategyServer:

    def __init__(self):
        self.name = 'fedavg'
        self.initial_impute = 'fedavg'
        self.fine_tune_epochs = 0

    def aggregate_parameters(
            self, local_model_parameters: List[OrderedDict], fit_res: List[dict], params: dict, *args, **kwargs
    ) -> Tuple[List[OrderedDict], dict]:
        """
        Aggregate local models
        :param local_model_parameters: List of local model parameters
        :param fit_res: List of fit results of local training
            - sample_size: int - number of samples used for training
        :param params: dictionary for information
        :param args: other params list
        :param kwargs: other params dict
        :return: List of aggregated model parameters, dict of aggregated results
        """

        # federated averaging implementation
        averaged_model_state_dict = OrderedDict([])  # global parameters
        sample_sizes = [item['sample_size'] for item in fit_res]
        normalized_coefficient = [size / sum(sample_sizes) for size in sample_sizes]

        for it, local_model_state_dict in enumerate(local_model_parameters):
            for key in local_model_state_dict.keys():
                if it == 0:
                    averaged_model_state_dict[key] = normalized_coefficient[it] * local_model_state_dict[key]
                else:
                    averaged_model_state_dict[key] += normalized_coefficient[it] * local_model_state_dict[key]

        # copy parameters for each client
        agg_model_parameters = [deepcopy(averaged_model_state_dict) for _ in range(len(local_model_parameters))]
        agg_res = {}

        return agg_model_parameters, agg_res

    def fit_instruction(self, params_list: List[dict]) -> List[dict]:

        return [{'fit_model': True} for _ in range(len(params_list))]

    def update_instruction(self, params: dict) -> dict:

        return {}


class FedTreeStrategyServer:

    def __init__(self):
        self.name = 'fedtree'
        self.initial_impute = 'fedavg'
        self.fine_tune_epochs = 0

    def aggregate_parameters(
            self, local_model_parameters: List[OrderedDict], fit_res: List[dict], params: dict, *args, **kwargs
    ) -> Tuple[List[OrderedDict], dict]:
        """
        Aggregate local models
        :param local_model_parameters: List of local model parameters
        :param fit_res: List of fit results of local training
            - sample_size: int - number of samples used for training
        :param params: dictionary for information
        :param args: other params list
        :param kwargs: other params dict
        :return: List of aggregated model parameters, dict of aggregated results
        """

        # federated tree sampling strategy
        sample_sizes = [item['sample_size'] for item in fit_res]
        sample_fracs = [size / sum(sample_sizes) for size in sample_sizes]

        np.random.seed(1203401)
        # all local trees
        global_trees = []
        for local_model_state_dict, sample_frac in zip(local_model_parameters, sample_fracs):
            local_trees = local_model_state_dict['estimators']
            sampled_trees = np.random.choice(local_trees, int(len(local_trees) * sample_frac), replace=False)
            global_trees.extend(sampled_trees)

        global_params = OrderedDict({"estimators": global_trees})
        # copy parameters for each client
        agg_model_parameters = [deepcopy(global_params) for _ in range(len(local_model_parameters))]
        agg_res = {}

        return agg_model_parameters, agg_res

    def fit_instruction(self, params_list: List[dict]) -> List[dict]:

        return [{'fit_model': True} for _ in range(len(params_list))]

    def update_instruction(self, params: dict) -> dict:

        return {}