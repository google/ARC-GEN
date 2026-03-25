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


def generate(size=None, colors=None):
  """Returns input and output grids according to the given parameters.

  Args:
    size: the width and height of the (square) grid
    colors: the digits representing the colors to be used
  """
  if size is None:
    size = common.randint(2, 3)
    color_list = common.random_colors(3)
    idxs = [common.randint(0, len(color_list) - 1) for _ in range(size * size)]
    colors = [color_list[idx] for idx in idxs]

  grid = common.grid(size, size, 0)
  output = common.grid(2 * size, 2 * size, 0)
  for r in range(size):
    for c in range(size):
      color = colors[r * size + c]
      output[r][c] = grid[r][c] = color
      output[c][2 * size - r - 1] = color
      output[2 * size - r - 1][2 * size - c - 1] = color
      output[2 * size - c - 1][r] = color
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(size=2, colors=[8, 6, 6, 8]),
      generate(size=3, colors=[7, 7, 8, 7, 7, 8, 8, 8, 8]),
      generate(size=3, colors=[6, 9, 9, 6, 4, 4, 6, 4, 4]),
  ]
  test = [
      generate(size=3, colors=[1, 4, 1, 4, 9, 4, 9, 1, 9]),
  ]
  return {"train": train, "test": test}
