# Copyright 2025 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Generator."""

import common


def generate(colors=None, size=3):
  """Returns input and output grids according to the given parameters.

  Args:
    colors: a list of digits representing colors to be used
    size: the width and height of the (square) grid
  """
  if colors is None:
    color_list = common.random_colors(3)
    colors = [color_list[common.randint(0, 2)] for _ in range(size * size)]

  grid, output = common.grids(size, size)
  for r in range(size):
    for c in range(size):
      output[r][c] = grid[r][c] = colors[r * size + c]
  output = common.transpose(output)
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(colors=[2, 2, 1, 1, 5, 1, 5, 2, 2]),
      generate(colors=[2, 2, 5, 6, 2, 2, 5, 5, 5]),
      generate(colors=[9, 9, 5, 5, 5, 8, 5, 8, 9]),
      generate(colors=[2, 6, 6, 2, 1, 1, 2, 6, 2]),
  ]
  test = [
      generate(colors=[9, 3, 4, 9, 4, 4, 9, 3, 4]),
  ]
  return {"train": train, "test": test}
