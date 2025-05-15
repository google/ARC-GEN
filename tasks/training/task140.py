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
    colors: a list of digits representing the colors to be used
    size: the width and height of the (square) grid
  """
  if colors is None:
    colors = [common.randint(0, 9) for _ in range(6)]

  grid, output = common.grids(size, size)
  output[2][2] = grid[0][0] = colors[0]
  output[2][1] = grid[0][1] = colors[1]
  output[2][0] = grid[0][2] = colors[2]
  output[1][2] = grid[1][0] = colors[3]
  output[1][1] = grid[1][1] = colors[4]
  output[0][2] = grid[2][0] = colors[5]
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(colors=[3, 3, 8, 3, 7, 5]),
      generate(colors=[5, 5, 2, 1, 0, 0]),
  ]
  test = [
      generate(colors=[6, 3, 5, 6, 8, 4]),
  ]
  return {"train": train, "test": test}
