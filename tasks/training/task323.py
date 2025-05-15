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


def generate(row=None, col=None, size=13):
  """Returns input and output grids according to the given parameters.

  Args:
    row: a vertical coordinate where the pixel should be placed
    col: a horizontal coordinate where the pixel should be placed
    size: the width and height of the (square) grid
  """
  if row is None:
    row, col = common.randint(0, size - 1), common.randint(0, size - 1)

  grid, output = common.grids(size, size)
  output[row][col] = grid[row][col] = common.cyan()
  for dr, dc in [(-1, 1), (1, -1)]:
    v, h, r, c = 2, 0, row, col
    while True:
      if v:
        r, v = r + dr, v - 1
        if r < 0 or r >= size: break
        output[r][c] = common.gray()
        if not v: h = 2
      else:
        c, h = c + dc, h - 1
        if c < 0 or c >= size: break
        output[r][c] = common.gray()
        if not h: v = 2
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(row=3, col=4),
      generate(row=7, col=6),
  ]
  test = [
      generate(row=5, col=5),
  ]
  return {"train": train, "test": test}
