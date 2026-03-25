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


def generate(rows=None, cols=None, idxs=None, colors=None, boxrows=None,
             boxcols=None, wides=None, talls=None, size=20):
  """Returns input and output grids according to the given parameters.

  Args:
    rows: a list of vertical coordinates where sprites should be placed
    cols: a list of horizontal coordinates where sprites should be placed
    idxs: a list of indices into the (hardcoded) sprite type list
    colors: a list of colors to use for the sprites
    boxrows: a list of vertical coordinates where boxes should be placed
    boxcols: a list of horizontal coordinates where boxes should be placed
    wides: a list of widths of boxes
    talls: a list of heights of boxes
    size: the width and height of the (square) grid
  """
  if rows is None:
    num_sprites = common.randint(5, 6)
    while True:
      # TODO: We might need more space around sprite #0 (due to its box).
      rows = [common.randint(1, size - 6) for _ in range(num_sprites)]
      cols = [common.randint(1, size - 6) for _ in range(num_sprites)]
      lengths = [5] * num_sprites
      if not common.overlaps(rows, cols, lengths, lengths, 1): break
    idxs = [common.randint(0, 9) for _ in range(num_sprites)]
    idxs[1] = idxs[0]  # We should have at least one copy.
    colors = [common.randint(2, 3)] + [1] * (num_sprites - 1)
    boxrows, boxcols, wides, talls = [rows[0] - 1], [cols[0] - 1], [7], [7]
    # TODO: Create the "fakeout" boxes.

  grid, output = common.grids(size, size)
  for row, col, idx, color in zip(rows, cols, idxs, colors):
    r_list, c_list = [], []
    if idx == 0:
      r_list, c_list = [1, 2, 2, 2, 3], [2, 1, 2, 3, 2]
    if idx == 1:
      r_list, c_list = [1, 1, 1, 2, 2, 2, 3, 3, 3], [1, 2, 3, 1, 2, 3, 1, 2, 3]
    if idx == 2:
      r_list, c_list = [2, 2, 2, 2], [1, 2, 3, 4]
    if idx == 3:
      r_list, c_list = [1, 2, 3], [2, 2, 2]
    if idx == 4:
      r_list, c_list = [1, 2, 2, 2, 3, 3, 3, 3, 3], [2, 1, 2, 3, 0, 1, 2, 3, 4]
    if idx == 5:
      r_list, c_list = [1, 1, 1, 2, 2, 2], [1, 2, 3, 1, 2, 3]
    if idx == 6:
      r_list, c_list = [1, 1, 2, 2, 3, 3, 3, 3], [2, 3, 2, 3, 1, 2, 3, 4]
    if idx == 7:
      r_list, c_list = [0, 1, 2, 3], [2, 2, 2, 2]
    if idx == 8:
      r_list, c_list = [1, 2, 3, 3, 3, 3, 4], [2, 2, 1, 2, 3, 4, 2]
    if idx == 9:
      r_list = [0, 0, 1, 1, 1, 1, 2, 2, 2, 2, 3, 3]
      c_list = [1, 2, 0, 1, 2, 3, 0, 1, 2, 3, 1, 2]
    for r, c in zip(r_list, c_list):
      output[row + r][col + c] = grid[row + r][col + c] = color
      if idx != idxs[0]: continue
      output[row + r][col + c] = colors[0]
    if wides:
      for boxrow, boxcol, wide, tall in zip(boxrows, boxcols, wides, talls):
        for bitmap in [grid, output]:
          for r in range(boxrow, boxrow + tall):
            common.draw(bitmap, r, boxcol, common.gray())
            common.draw(bitmap, r, boxcol + wide - 1, common.gray())
          for c in range(boxcol, boxcol + wide):
            common.draw(bitmap, boxrow, c, common.gray())
            common.draw(bitmap, boxrow + tall - 1, c, common.gray())
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(rows=[1, 0, 6, 10, 14], cols=[1, 12, 9, 2, 12],
               idxs=[0, 1, 0, 2, 0], colors=[2, 1, 1, 1, 1], boxrows=[0],
               boxcols=[0], wides=[7], talls=[7]),
      generate(rows=[2, 8, 10, 11, 15], cols=[6, 14, 9, 2, 10],
               idxs=[1, 1, 3, 1, 4], colors=[3, 1, 1, 1, 1], boxrows=[1],
               boxcols=[5], wides=[7], talls=[7]),
      generate(rows=[1, 0, 9, 10, 14, 15], cols=[14, 0, 2, 9, 6, 1],
               idxs=[5, 3, 3, 5, 0, 5], colors=[2, 2, 1, 1, 1, 1],
               boxrows=[0, -1], boxcols=[13, -1], wides=[7, 7], talls=[7, 7]),
      generate(rows=[4, 0, 7, 8, 12, 14], cols=[2, 14, 14, 9, 3, 9],
               idxs=[1, 6, 6, 1, 7, 0], colors=[3, 3, 1, 1, 1, 1],
               boxrows=[3, -1], boxcols=[1, 13], wides=[7, 8], talls=[7, 7]),
  ]
  test = [
      generate(rows=[14, 0, 1, 3, 8, 8, 8, 15],
               cols=[13, 14, 6, 1, 0, 6, 13, 1],
               idxs=[0, 5, 5, 8, 0, 9, 0, 9], colors=[2, 2, 1, 1, 1, 1, 1, 2],
               boxrows=[13, -1, 13], boxcols=[12, 12, -1], wides=[7, 9, 8],
               talls=[7, 7, 8]),
  ]
  return {"train": train, "test": test}
