# Copyright 2026 Google LLC
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


def generate(colors=None):
  """Returns input and output grids according to the given parameters.

  Args:
    colors: A list of colors to use.
  """

  if colors is None:
    colors = common.random_colors(5)

  grid, output = common.grid(5, 5), common.grid(3, 3)
  grid[0][0] = grid[4][4] = output[0][0] = output[2][2] = colors[0]
  grid[1][1] = grid[3][3] = output[0][1] = output[2][1] = colors[1]
  grid[0][4] = grid[4][0] = output[0][2] = output[2][0] = colors[2]
  grid[1][3] = grid[3][1] = output[1][0] = output[1][2] = colors[4]
  grid[2][2] = output[1][1] = colors[3]
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(colors=[6, 2, 7, 3, 4]),
      generate(colors=[1, 5, 9, 7, 8]),
      generate(colors=[2, 3, 1, 4, 6]),
  ]
  test = [
      generate(colors=[7, 6, 5, 2, 4]),
  ]
  return {"train": train, "test": test}
