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
    color_list = common.random_colors(3, exclude=[common.gray()])
    colors = [color_list[common.randint(0, 2)] for _ in range(size * size)]

  grid, output = common.grids(3 * size + 2, size)
  for c in range(size, 3 * size + 2, size + 1):
    for r in range(size):
      output[r][c] = grid[r][c] = common.gray()
  for r in range(size):
    for c in range(size):
      output[r][c] = grid[r][c] = colors[r * size + c]
      output[c][2 * size - r] = colors[r * size + c]
      output[size - 1 - r][3 * size + 1 - c] = colors[r * size + c]
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(colors=[1, 1, 2, 4, 1, 1, 4, 4, 1]),
      generate(colors=[6, 3, 3, 6, 3, 3, 6, 3, 2]),
      generate(colors=[2, 7, 8, 7, 7, 8, 8, 8, 8]),
  ]
  test = [
      generate(colors=[3, 3, 9, 9, 9, 9, 2, 9, 9]),
  ]
  return {"train": train, "test": test}
