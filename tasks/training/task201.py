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


def generate(rows=None, cols=None, idxs=None, brows=None, bcols=None,
             colors=None, flip=None, size=13):
  """Returns input and output grids according to the given parameters.

  Args:
    rows: a list of vertical coordinates where pixels should be placed
    cols: a list of horizontal coordinates where pixels should be placed
    idxs: a list of indices into the sprite list
    brows: a list of vertical coordinates where boxes should be placed
    bcols: a list of horizontal coordinates where boxes should be placed
    colors: a list of digits representing the colors to be used
    flip: whether to flip the sprites horizontally
    size: the width and height of the (square) grid
  """
  if rows is None:
    wide, tall = common.randint(2, 3), common.randint(2, 4)
    rows0, cols0 = common.conway_sprite(wide, tall, wide * tall // 2)
    rows1, cols1 = common.conway_sprite(wide, tall, wide * tall // 2)
    rows, cols = rows0 + rows1, cols0 + cols1
    idxs = [0] * len(rows0) + [1] * len(rows1)
    while True:
      width, height = 2 * (wide + 1), tall + 2
      wides, talls = [width, width - 2], [height, height - 2]
      brows = [common.randint(0, size - tall) for tall in talls]
      bcols = [common.randint(0, size - wide) for wide in wides]
      if not common.overlaps(brows, bcols, wides, talls): break
    colors = common.random_colors(2, exclude=[common.yellow()])
    flip = common.randint(0, 1)

  width, height = 2 * (max(cols) + 2), max(rows) + 3
  grid, output = common.grid(size, size), common.grid(width, height)
  for r in [0, height - 1]:
    for c in [0, width - 1]:
      output[r][c] = grid[r + brows[0]][c + bcols[0]] = common.yellow()
  for r in range(1, height - 1):
    output[r][0] = grid[r + brows[0]][bcols[0]] = colors[0]
    output[r][width - 1] = grid[r + brows[0]][width - 1 + bcols[0]] = colors[1]
  for row, col, idx in zip(rows, cols, idxs):
    r, c = row, col + idx * (max(cols) + 1)
    output[r + 1][c + 1] = colors[idx]
    if flip: c = width - c - 3
    grid[r + brows[1]][c + bcols[1]] = colors[idx]
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(rows=[0, 0, 1, 2, 2, 3, 0, 1, 1, 1, 2],
               cols=[0, 1, 1, 1, 2, 2, 0, 0, 1, 2, 0],
               idxs=[0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1],
               brows=[7, 3], bcols=[5, 2], colors=[2, 1], flip=0),
      generate(rows=[0, 0, 1, 1, 1, 2, 2, 3, 3, 3, 4, 4, 0, 1, 1, 1, 2, 3, 3],
               cols=[0, 2, 0, 1, 2, 0, 2, 0, 1, 2, 0, 2, 1, 0, 1, 2, 1, 0, 1],
               idxs=[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1],
               brows=[6, 1], bcols=[1, 4], colors=[8, 3], flip=1),
      generate(rows=[0, 1, 1, 0, 0, 1],
               cols=[1, 0, 1, 0, 1, 0],
               idxs=[0, 0, 0, 1, 1, 1],
               brows=[1, 9], bcols=[2, 3], colors=[2, 1], flip=1),
      generate(rows=[0, 0, 1, 1, 2, 0, 1, 1, 2],
               cols=[0, 1, 0, 1, 1, 1, 0, 1, 1],
               idxs=[0, 0, 0, 0, 0, 1, 1, 1, 1],
               brows=[1, 9], bcols=[5, 5], colors=[7, 3], flip=0),
  ]
  test = [
      generate(rows=[0, 1, 1, 1, 2, 3, 3, 0, 0, 1, 1, 1, 2, 3],
               cols=[2, 0, 1, 2, 1, 0, 1, 0, 2, 0, 1, 2, 2, 2],
               idxs=[0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1],
               brows=[1, 9], bcols=[1, 1], colors=[2, 8], flip=1),
  ]
  return {"train": train, "test": test}
