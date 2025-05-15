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


def generate(width=None, height=None, rows=None, cols=None, colors=None, size=9,
             minisize=3):
  """Returns input and output grids according to the given parameters.

  Args:
    width: the width of the input grid
    height: the height of the input grid
    rows: a list of vertical coordinates where pixels should be placed
    cols: a list of horizontal coordinates where pixels should be placed
    colors: a list of digits representing the colors to be used
    size: the width and height of the (square) grid
    minisize: the width and height of the (square) sprites
  """
  if width is None:
    colors = [common.random_color(exclude=[common.gray()]) for _ in range(size)]
    while True:
      width, height = common.randint(14, 16), common.randint(14, 16)
      rows = [common.randint(0, height - minisize) for _ in range(size)]
      cols = [common.randint(0, width - minisize) for _ in range(size)]
      lengths = [3] * size
      if not common.overlaps(rows, cols, lengths, lengths, 1): break

  grid = common.grid(width, height, common.black())
  output = common.grid(size, size, common.gray())
  for idx in range(len(colors)):
    row, col, color = rows[idx], cols[idx], colors[idx]
    for dc in range(minisize):
      for dr in range(minisize):
        grid[row + dr][col + dc] = common.gray()
    r, c = [], []
    r, c = (r if idx != 0 else [0, 0, 1]), (c if idx != 0 else [0, 1, 0])
    r, c = (r if idx != 1 else [0, 0, 0, 1]), (c if idx != 1 else [0, 1, 2, 1])
    r, c = (r if idx != 2 else [0, 0, 1]), (c if idx != 2 else [1, 2, 2])
    r, c = (r if idx != 3 else [0, 1, 1, 2]), (c if idx != 3 else [0, 0, 1, 0])
    r, c = (r if idx != 5 else [0, 1, 1, 2]), (c if idx != 5 else [2, 1, 2, 2])
    r, c = (r if idx != 6 else [1, 2, 2]), (c if idx != 6 else [0, 0, 1])
    r, c = (r if idx != 7 else [1, 2, 2, 2]), (c if idx != 7 else [1, 0, 1, 2])
    r, c = (r if idx != 8 else [1, 2, 2]), (c if idx != 8 else [2, 1, 2])
    for dr, dc in zip(r, c):
      grid[row + dr][col + dc] = color
      output[minisize * (idx // 3) + dr][minisize * (idx % 3) + dc] = color
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(width=14, height=14, rows=[11, 1, 7, 3, 5, 9, 0, 6, 11],
               cols=[10, 8, 1, 2, 6, 6, 0, 10, 0],
               colors=[6, 2, 1, 2, 5, 3, 8, 4, 9]),
      generate(width=14, height=16, rows=[12, 8, 2, 9, 8, 0, 1, 13, 5],
               cols=[4, 1, 5, 10, 6, 11, 1, 9, 10],
               colors=[7, 1, 8, 6, 5, 4, 3, 2, 9]),
  ]
  test = [
      generate(width=15, height=16, rows=[10, 2, 10, 1, 5, 7, 0, 6, 12],
               cols=[11, 5, 1, 1, 10, 6, 10, 2, 6],
               colors=[3, 2, 4, 1, 5, 1, 6, 8, 7]),
  ]
  return {"train": train, "test": test}
