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


def generate(row=None, col=None, dirs=None, color=None, size=9):
  """Returns input and output grids according to the given parameters.

  Args:
    row: a vertical coordinate where the square should be placed
    col: a horizontal coordinate where the square should be placed
    dirs: a list of integers representing which directions to sprout
    color: the integer used to color the square & sprouts
    size: the width and height of the (square) grid
  """
  if row is None:
    row, col = common.randint(1, size - 3), common.randint(1, size - 3)
    num_dirs = common.randint(1, 3)
    dirs = common.sample(range(4), num_dirs)
    color = common.random_color(exclude=[common.red()])

  def is_valid(r, c):
    return r >= 0 and r < size and c >= 0 and c < size

  grid, output = common.grids(size, size)
  deltas = [(-1, -1), (-1, 1), (1, 1), (1, -1)]
  for delta_idx in range(len(deltas)):
    dr, dc = deltas[delta_idx]
    r, c = row + (dr + 1) // 2, col + (dc + 1) // 2
    output[r][c] = grid[r][c] = color
    if delta_idx not in dirs: continue
    grid[r][c] = common.red()
    drew = True
    while drew:
      drew = False
      if is_valid(r, c): output[r][c], drew = color, True
      if is_valid(r + dr, c): output[r + dr][c], drew = color, True
      if is_valid(r, c + dc): output[r][c + dc], drew = color, True
      r, c = r + dr, c + dc
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(row=4, col=2, dirs=[1], color=4),
      generate(row=1, col=2, dirs=[2], color=3),
      generate(row=3, col=3, dirs=[1, 3], color=6),
      generate(row=3, col=3, dirs=[0, 1, 3], color=7),
  ]
  test = [
      generate(row=2, col=5, dirs=[0, 1, 2], color=8),
  ]
  return {"train": train, "test": test}
 