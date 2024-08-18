from types import NoneType
from typing import Tuple, Union

import torch

from FunctionEncoder import BaseDataset


class FixedDataset(BaseDataset):
    def __init__(self,
                 xs:torch.tensor,
                 ys:torch.tensor,
                 n_functions_per_sample:int,
                 n_examples_per_sample:int,
                 n_points_per_sample:int,
                 device:str="auto"):
        assert len(xs.shape) == 3, f"xs must be a 3D tensor, the first dim corresponds to functions, the second to data points, the third to input size. Got shape: {xs.shape}"
        assert len(ys.shape) == 3, f"ys must be a 3D tensor, the first dim corresponds to functions, the second to data points, the third to output size. Got shape: {ys.shape}"
        assert xs.shape[0] == ys.shape[0], f"xs and ys must have the same number of functions. Got xs.shape[0]: {xs.shape[0]}, ys.shape[0]: {ys.shape[0]}"
        assert xs.shape[1] == ys.shape[1], f"xs and ys must have the same number of data points. Got xs.shape[1]: {xs.shape[1]}, ys.shape[1]: {ys.shape[1]}"
        super().__init__(input_size=(xs.shape[2],),
                         output_size=(ys.shape[2],),
                         total_n_functions=xs.shape[0],
                         total_n_samples_per_function=xs.shape[1],
                         data_type="deterministic",
                         n_functions_per_sample=n_functions_per_sample,
                         n_examples_per_sample=n_examples_per_sample,
                         n_points_per_sample=n_points_per_sample,
                         device=device,
                         )
        self.xs = xs.to(self.device)
        self.ys = ys.to(self.device)


    def sample(self) -> Tuple[ torch.tensor,
                                                                torch.tensor, 
                                                                torch.tensor, 
                                                                torch.tensor, 
                                                                dict]:
        function_indicies = torch.randint(0, self.n_functions, (self.n_functions_per_sample,), device=self.device)
        example_indicies = torch.randint(0, self.n_samples_per_function, (self.n_examples_per_sample,), device=self.device)
        point_indicies = torch.randint(0, self.n_points_per_sample, (self.n_points_per_sample,), device=self.device)
        examples_xs = self.xs[function_indicies][:, example_indicies]
        examples_ys = self.ys[function_indicies][:, example_indicies]
        xs = self.xs[function_indicies][:, point_indicies]
        ys = self.ys[function_indicies][:, point_indicies]

        info = {} # nothing interesting here
        return examples_xs, examples_ys, xs, ys, info


