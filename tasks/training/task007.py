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


def generate(colors=None, diags=None, size=7, num=3):
  """Returns input and output grids according to the given parameters.

  Args:
    colors: a list of digits representing different colors
    diags: a list of diagonal indices where the striped colors will be shown
    size: the width and height of the (square) grid
    num: the number of stripes in the grid
  """
  if colors is None:
    diags = [common.choice(range(s, 2 * size - 1, num)) for s in range(num)]
    colors = common.random_colors(num)

  grid, output = common.grids(size, size)
  for c in range(size):
    for r in range(size):
      diag = c + r
      color = colors[diag % len(colors)]
      output[r][c] = color
      grid[r][c] = color if diag in diags else common.black()
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(colors=[2, 8, 3], diags=[0, 1, 2]),
      generate(colors=[2, 4, 1], diags=[8, 9, 10]),
      generate(colors=[4, 8, 3], diags=[4, 5, 9]),
  ]
  test = [
      generate(colors=[2, 1, 4], diags=[1, 6, 11]),
  ]
  return {"train": train, "test": test}
