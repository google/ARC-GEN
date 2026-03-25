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


def generate(colors=None, cols=None, size=10):
  """Returns input and output grids according to the given parameters.

  Args:
    colors: a pair of digits representing two different colors
    cols: a list of horizontal coordinates where pixels should be placed
    size: the width and height of the (square) grid
  """
  if colors is None:
    colors = common.random_colors(2)
    cols = [common.randint(2, size - 3) for _ in range(2)]

  grid, output = common.grids(size, size)
  grid[2][cols[0]] = colors[0]
  grid[size - 3][cols[1]] = colors[1]
  for r in range(0, size // 2):
    output[r][0] = output[r][size - 1] = colors[0]
    output[0][r] = output[0][size - 1 - r] = colors[0]
    output[2][r] = output[2][size - 1 - r] = colors[0]
    output[size - 1 - r][0] = output[size - 1 - r][size - 1] = colors[1]
    output[size - 1][r] = output[size - 1][size - 1 - r] = colors[1]
    output[size - 3][r] = output[size - 3][size - 1 - r] = colors[1]
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(colors=[6, 7], cols=[2, 7]),
      generate(colors=[1, 4], cols=[6, 5]),
  ]
  test = [
      generate(colors=[2, 8], cols=[4, 6]),
  ]
  return {"train": train, "test": test}
