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
             colors=None, size=13):
  """Returns input and output grids according to the given parameters.

  Args:
    rows: a list of vertical coordinates where pixels should be placed
    cols: a list of horizontal coordinates where pixels should be placed
    idxs: a list of indices into the sprites list
    brows: a list of vertical coordinates where the sprites should be placed
    bcols: a list of horizontal coordinates where the sprites should be placed
    colors: a list of colors to use for the sprites
    size: the size of the input and output grids
  """
  if rows is None:
    num_sprites = common.randint(3, 4)
    lengths = [3] * num_sprites
    while True:
      brows = [common.randint(0, size - 3) for _ in range(num_sprites)]
      bcols = [common.randint(0, size - 3) for _ in range(num_sprites)]
      if not common.overlaps(brows, bcols, lengths, lengths, 1): break
    rows, cols, idxs = [], [], []
    for idx in range(num_sprites):
      xrows, xcols = common.conway_sprite(3, 3, 4)
      rows.extend(xrows)
      cols.extend(xcols)
      idxs.extend([idx] * len(xrows))
    colors = common.random_colors(num_sprites, exclude=[common.cyan()])

  grid, output = common.grid(size, size), common.grid(3, 3)
  for row, col, idx in zip(rows, cols, idxs):
    grid[row + brows[idx]][col + bcols[idx]] = colors[idx]
    if idx: continue
    output[row][col] = colors[idx]
  grid[brows[0] + 1][bcols[0] + 1] = common.cyan()
  output[1][1] = colors[0]
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(rows=[0, 1, 1, 1, 2, 0, 1, 1, 1, 2, 2, 0, 1, 1, 1, 2, 0, 0, 1, 1,
                     2, 2, 2],
               cols=[1, 0, 1, 2, 1, 1, 0, 1, 2, 0, 1, 0, 0, 1, 2, 1, 1, 2, 0, 2,
                     0, 1, 2],
               idxs=[0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 3, 3, 3, 3,
                     3, 3, 3],
               brows=[0, 0, 4, 9], bcols=[9, 1, 4, 8], colors=[4, 3, 2, 6]),
      generate(rows=[0, 0, 1, 1, 2, 2, 0, 1, 1, 1, 2, 0, 0, 1, 1, 1, 2, 2, 2],
               cols=[1, 2, 0, 1, 1, 2, 1, 0, 1, 2, 1, 0, 2, 0, 1, 2, 0, 1, 2],
               idxs=[0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 2, 2, 2],
               brows=[4, 0, 8], bcols=[2, 7, 7], colors=[3, 2, 1]),
      generate(rows=[0, 0, 0, 1, 2, 2, 0, 0, 1, 1, 1, 2, 0, 0, 1, 1, 1, 2],
               cols=[0, 1, 2, 1, 0, 1, 0, 2, 0, 1, 2, 2, 0, 2, 0, 1, 2, 1],
               idxs=[0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 2],
               brows=[2, 3, 8], bcols=[1, 8, 3], colors=[2, 3, 1]),
  ]
  test = [
      generate(rows=[0, 0, 1, 1, 2, 0, 0, 0, 1, 1, 2, 0, 1, 1, 2, 2, 0, 0, 0, 1,
                     2, 2, 2],
               cols=[1, 2, 0, 2, 1, 0, 1, 2, 1, 2, 2, 0, 0, 1, 1, 2, 0, 1, 2, 1,
                     0, 1, 2],
               idxs=[0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 3, 3, 3, 3,
                     3, 3, 3],
               brows=[4, 1, 6, 9], bcols=[9, 5, 1, 7], colors=[7, 1, 2, 3]),
  ]
  return {"train": train, "test": test}
