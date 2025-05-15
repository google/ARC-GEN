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
    color_list = common.random_colors(4)
    colors = [color_list[common.randint(0, 3)] for _ in range(size * size)]

  grid, output = common.grid(size, size), common.grid(size, 2 * size)
  for r in range(size):
    for c in range(size):
      color = colors[r * size + c]
      output[2 * size - r - 1][c] = output[r][c] = grid[r][c] = color
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(colors=[9, 1, 4, 9, 1, 4, 2, 1, 1]),
      generate(colors=[4, 8, 4, 7, 6, 7, 8, 7, 8]),
      generate(colors=[7, 7, 7, 9, 5, 5, 5, 1, 7]),
      generate(colors=[2, 6, 9, 2, 6, 9, 2, 9, 2]),
  ]
  test = [
      generate(colors=[2, 9, 2, 8, 5, 2, 2, 2, 8]),
  ]
  return {"train": train, "test": test}
