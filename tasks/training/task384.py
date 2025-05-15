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


def generate(rows=None, cols=None, row=None, col=None, size=9):
  """Returns input and output grids according to the given parameters.

  Args:
    rows: a list of vertical coordinates where pixels should be placed
    cols: a list of horizontal coordinates where pixels should be placed
    row: a vertical offset for the submarine
    col: a horizontal offset for the submarine
    size: the width and height of the (square) grid
  """
  if rows is None:
    width, height = common.randint(3, 5), common.randint(3, 4)
    num_pixels = common.randint(width * height // 4, 3 * width * height // 4)
    while True:
      pixels = common.sample(common.all_pixels(width, height), num_pixels)
      if common.diagonally_connected(pixels): break
    rows, cols = zip(*pixels)
    rows, cols = [r - min(rows) for r in rows], [c - min(cols) for c in cols]
    row, col = common.randint(1, height - 2), common.randint(1, width - 2)

  width, height = max(cols) + 1, max(rows) + 1
  grid = common.grid(size, size)
  output = common.grid(2 * width, 2 * height)
  for r, c in zip(rows, cols):
    grid[row + r][col + c] = common.yellow()
    for dr, dc in [(0, 0), (0, 1), (1, 0), (1, 1)]:
      output[2 * r + dr][2 * c + dc] = common.yellow()
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(rows=[0, 0, 1, 1, 1, 1, 2, 2], cols=[1, 2, 0, 1, 2, 3, 1, 2],
               row=2, col=1),
      generate(rows=[0, 1, 1, 2], cols=[1, 0, 1, 2], row=1, col=3),
      generate(rows=[0, 1, 1, 2, 3, 3], cols=[1, 0, 1, 1, 1, 2], row=4, col=1),
  ]
  test = [
      generate(rows=[0, 0, 1, 1, 1, 2, 2], cols=[1, 3, 0, 2, 4, 1, 3], row=1,
               col=3),
  ]
  return {"train": train, "test": test}
