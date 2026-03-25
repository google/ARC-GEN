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
    colors: The colors of the grid.
  """

  if colors is None:
    colors = common.sample(list(range(10)), 5)

  grid, output = common.grids(1, 5)
  for i in range(5):
    output[i][0] = grid[i][0] = colors[i]
  output[0][0] = grid[1][0]
  output[1][0] = grid[0][0]
  output[3][0] = grid[4][0]
  output[4][0] = grid[3][0]
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(colors=[9, 0, 1, 6, 8]),
      generate(colors=[4, 3, 6, 2, 8]),
  ]
  test = [
      generate(colors=[4, 5, 6, 7, 2]),
  ]
  return {"train": train, "test": test}
