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


def generate(colors=None, values=None, size=3):
  """Returns input and output grids according to the given parameters.

  Args:
    colors: a list of digits representing different colors
    values: a list of color indices for all cells in the grid
    size: the width and height of the (square) grid
  """
  if colors is None:
    variety = common.randint(3, 3)
    colors = common.random_colors(variety)
    values = common.choices(range(variety), k=size * size)

  grid = common.grid(size, size)
  for r in range(size):
    for c in range(size):
      grid[r][c] = colors[values[r * size + c]]
  output = [row[::-1] for row in grid[::-1]]
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(colors=[2, 1, 8], values=[0, 0, 1, 0, 1, 0, 0, 2, 1]),
      generate(colors=[9, 2, 4], values=[0, 1, 2, 1, 2, 2, 1, 0, 1]),
      generate(colors=[8, 5, 7], values=[0, 0, 0, 1, 1, 0, 0, 1, 1]),
      generate(colors=[3, 2, 9], values=[0, 1, 2, 2, 2, 2, 1, 0, 0]),
  ]
  test = [
      generate(colors=[6, 4, 7], values=[0, 1, 1, 0, 0, 1, 1, 0, 2]),
  ]
  return {"train": train, "test": test}
