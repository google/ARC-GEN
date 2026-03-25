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


def generate(horizon=None, cyan=None, blues=None, extra_rows=None,
             extra_cols=None, extra_colors=None):
  """Returns input and output grids according to the given parameters.

  Args:
    horizon: The row of the horizon.
    cyan: The length of the cyan tips.
    blues: The lengths of the blue pillars.
    extra_rows: Extra rows for the ambiguous / broken case.
    extra_cols: Extra columns for the ambiguous / broken case.
    extra_colors: Extra colors for the ambiguous / broken case.
  """

  if horizon is None:
    num_blues = common.randint(3, 7)
    size, cyan = 2 * num_blues + 1, (num_blues + 1) // 2
    horizon = common.randint(cyan, (size + 1) // 2)
    blues = [common.randint(1, size - horizon - 1) for _ in range(num_blues)]

  size = 2 * len(blues) + 1
  grid, output = common.grids(size, size, 7)
  for c in range(0, size, 2):
    output[horizon - 1][c] = grid[horizon - 1][c] = 2
    output[horizon][c] = grid[horizon][c] = 5
  for i, blue in enumerate(blues):
    col = 2 * i + 1
    for r in range(blue):
      grid[size - 1 - r][col] = 1
      output[horizon + r][col] = 1
    for r in range(cyan):
      grid[size - 1 - blue - r][col] = 8
      output[horizon - 1 - r][col] = 8
    for r in range(horizon + blue, size):
      output[r][col] = 9
  if extra_rows:  # Handles an ambiguous / broken case.
    for row, col, color in zip(extra_rows, extra_cols, extra_colors):
      grid[row][col] = color
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(horizon=3, cyan=3, blues=[4, 1, 3, 2, 5]),
      generate(horizon=5, cyan=2, blues=[1, 3, 2, 2]),
      generate(horizon=7, cyan=3, blues=[2, 3, 1, 2, 4, 2],
               extra_rows=[8], extra_cols=[7], extra_colors=[7]),
  ]
  test = [
      generate(horizon=6, cyan=4, blues=[5, 1, 2, 3, 2, 1, 4]),
  ]
  return {"train": train, "test": test}
