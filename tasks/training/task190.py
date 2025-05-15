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


def generate(row=None, col=None, dirs=None, color=None, size=10):
  """Returns input and output grids according to the given parameters.

  Args:
    row: a vertical coordinate where the box should be placed
    col: a horizontal coordinate where the box should be placed
    dirs: a list of integers representing the directions to be used
    color: a digit representing a color to be used
    size: the width and height of the (square) grid
  """
  if row is None:
    row, col = common.randint(2, size - 4), common.randint(2, size - 4)
    color = common.random_color()
    dirs = common.sample([0, 1, 2, 3], common.randint(1, 3))

  grid, output = common.grids(size, size)
  for dr, dc in [(0, 0), (0, 1), (1, 0), (1, 1)]:
    output[row + dr][col + dc] = grid[row + dr][col + dc] = color
  for d in dirs:
    dr, dc = 1 if d in [2, 3] else -1, 1 if d in [1, 2] else -1
    r, c = row + (2 if dr == 1 else -1), col + (2 if dc == 1 else -1)
    grid[r][c] = color
    while r >= 0 and r < size and c >= 0 and c < size:
      output[r][c], r, c = color, r + dr, c + dc
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(row=2, col=2, dirs=[2], color=3),
      generate(row=2, col=4, dirs=[1, 2], color=4),
      generate(row=3, col=4, dirs=[1, 3], color=7),
  ]
  test = [
      generate(row=4, col=3, dirs=[1, 2, 3], color=8),
  ]
  return {"train": train, "test": test}
