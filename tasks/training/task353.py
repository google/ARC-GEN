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


def generate(width=None, height=None, rows=None, cols=None):
  """Returns input and output grids according to the given parameters.

  Args:
    width: the width of the grid
    height: the height of the grid
    rows: a list of vertical coordinates where pixels should be placed
    cols: a list of horizontal coordinates where pixels should be placed
  """
  if width is None:
    while True:
      width = common.randint(3, 12)
      height = width + common.randint(0, 2)
      row, col = common.randint(0, height - 1), common.randint(0, width - 1)
      pixels = []
      for r in range(height):
        for c in range(width):
          if abs(r - row) <= 1 and abs(c - col) <= 1: continue  # too close
          if r == row or c == col or r - c == row - col or r + c == row + col:
            pixels.append((r, c))
      if pixels: break
    pixel = pixels[common.randint(0, len(pixels) - 1)]
    rows = [row, pixel[0]]
    cols = [col, pixel[1]]

  grid, output = common.grids(width, height)
  output[rows[1]][cols[1]] = grid[rows[1]][cols[1]] = common.yellow()
  grid[rows[0]][cols[0]] = common.green()
  rows[0] += 1 if rows[0] < rows[1] else 0
  rows[0] -= 1 if rows[0] > rows[1] else 0
  cols[0] += 1 if cols[0] < cols[1] else 0
  cols[0] -= 1 if cols[0] > cols[1] else 0
  output[rows[0]][cols[0]] = common.green()
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(width=3, height=3, rows=[0, 2], cols=[0, 2]),
      generate(width=3, height=5, rows=[1, 1], cols=[0, 2]),
      generate(width=5, height=5, rows=[2, 2], cols=[1, 4]),
      generate(width=7, height=7, rows=[1, 4], cols=[1, 4]),
      generate(width=10, height=10, rows=[7, 2], cols=[2, 2]),
      generate(width=11, height=11, rows=[2, 9], cols=[3, 3]),
      generate(width=3, height=3, rows=[0, 2], cols=[2, 0]),
  ]
  test = [
      generate(width=11, height=11, rows=[2, 8], cols=[3, 3]),
      generate(width=3, height=3, rows=[2, 0], cols=[2, 0]),
  ]
  return {"train": train, "test": test}
