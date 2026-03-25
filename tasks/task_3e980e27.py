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


def generate(rows=None, cols=None, idxs=None, colors=None, megarows=None,
             megacols=None, megaidxs=None, size=13):
  """Returns input and output grids according to the given parameters.

  Args:
    rows: a list of vertical coordinates where pixels should be placed
    cols: a list of horizontal coordinates where pixels should be placed
    color: a digit representing a color to be used
    size: the width and height of the (square) grid
  """
  if rows is None:
    # Choose the contents of the sprites.
    rows, cols, idxs, colors = [], [], [], []
    color_list = common.random_colors(2, exclude=[common.red(), common.green()])
    for idx in [0, 1]:
      num_pixels = common.randint(4, 6)
      while True:
        pixels = common.sample(common.all_pixels(3, 3), num_pixels)
        if common.diagonally_connected(pixels): break
      rows.extend([p[0] for p in pixels])
      cols.extend([p[1] for p in pixels])
      idxs.extend([idx] * len(pixels))
      colors.extend([color_list[idx]] * len(pixels))
      colors[-1] = common.green() if idx else common.red()
    # Choose the megarows and megacols.
    idx_set, idx_list, megaidxs = common.randint(0, 2), [], []
    if idx_set in [0, 1]: idx_list += [0]
    if idx_set in [0, 2]: idx_list += [1]
    for idx in idx_list:
      megaidxs.extend([idx] * common.randint(2, 3))
    megalens = [3] * len(megaidxs)
    while True:
      megarows = [common.randint(0, size - 3) for _ in megaidxs]
      megacols = [common.randint(0, size - 3) for _ in megaidxs]
      if not common.overlaps(megarows, megacols, megalens, megalens, 1): break

  grid, output = common.grids(size, size)
  seen = set()
  for mr, mc, mi in zip(megarows, megacols, megaidxs):
    for row, col, idx, color in zip(rows, cols, idxs, colors):
      if mi != idx: continue
      r, c = row, col
      if idx in seen and not idx: c = 2 - c
      if idx not in seen or color in [common.red(), common.green()]:
        grid[mr + r][mc + c] = color
      output[mr + r][mc + c] = color
    seen.add(mi)
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(rows=[0, 0, 1, 1, 2], cols=[0, 1, 0, 1, 2], idxs=[0, 0, 0, 0, 0],
               colors=[2, 1, 1, 1, 1], megarows=[3, 8], megacols=[3, 5],
               megaidxs=[0, 0]),
      generate(rows=[0, 1, 1, 1, 2, 2], cols=[1, 0, 1, 2, 0, 1],
               idxs=[1, 1, 1, 1, 1, 1], colors=[4, 4, 3, 4, 4, 4],
               megarows=[1, 5, 8], megacols=[5, 1, 8], megaidxs=[1, 1, 1]),
      generate(rows=[0, 0, 0, 1, 0, 0, 1, 1], cols=[0, 1, 2, 0, 0, 1, 1, 2],
               idxs=[1, 1, 1, 1, 0, 0, 0, 0], colors=[3, 8, 8, 8, 4, 2, 4, 4],
               megarows=[2, 8, 7, 1], megacols=[2, 1, 6, 9],
               megaidxs=[1, 1, 0, 0]),
      generate(rows=[0, 0, 0, 1, 1, 2, 0, 0, 1, 1, 1],
               cols=[0, 1, 2, 1, 2, 2, 1, 2, 0, 1, 2],
               idxs=[0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1],
               colors=[4, 4, 4, 2, 4, 4, 1, 1, 1, 3, 1],
               megarows=[1, 1, 10, 7, 8], megacols=[7, 2, 7, 9, 3],
               megaidxs=[0, 0, 0, 1, 1]),
  ]
  test = [
      generate(rows=[0, 1, 1, 2, 2, 0, 0, 0, 1, 1, 2],
               cols=[1, 0, 1, 0, 1, 0, 1, 2, 1, 2, 1],
               idxs=[0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1],
               colors=[1, 1, 2, 1, 1, 8, 8, 8, 3, 8, 8],
               megarows=[1, 0, 8, 5, 0, 9], megacols=[1, 8, 2, 8, 4, 6],
               megaidxs=[0, 0, 0, 1, 1, 1]),
  ]
  return {"train": train, "test": test}
