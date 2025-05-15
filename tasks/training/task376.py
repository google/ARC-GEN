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


def generate(stretch=None, color=None, width=17):
  """Returns input and output grids according to the given parameters.

  Args:
    stretch: how much to stretch the middle bit
    color: a digit representing a color to be used
    width: the width of the grid
  """
  if stretch is None:
    stretch = common.randint(1, 4)
    color = common.random_color()

  grid = common.grid(width, 2 + stretch)
  output = common.grid(width, 5 + 4 * stretch)
  for c in range(width):
    if c % 4 == 0:
      output[stretch + 1][c] = grid[stretch + 1][c] = color
      output[3 * (stretch + 1)][c] = color
      continue
    if c % 4 == 2:
      output[0][c] = grid[0][c] = color
      output[2 * (stretch + 1)][c] = color
      output[4 * (stretch + 1)][c] = color
      continue
    for r in range(1, stretch + 1):
      output[r][c] = grid[r][c] = color
      output[r + stretch + 1][c] = color
      output[r + 2 * (stretch + 1)][c] = color
      output[r + 3 * (stretch + 1)][c] = color
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(stretch=1, color=8),
      generate(stretch=2, color=2),
  ]
  test = [
      generate(stretch=3, color=3),
  ]
  return {"train": train, "test": test}
