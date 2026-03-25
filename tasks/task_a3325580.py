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
             colors=None, size=10):
  """Returns input and output grids according to the given parameters.

  Args:
    rows: a list of vertical coordinates where pixels should be placed
    cols: a list of horizontal coordinates where pixels should be placed
    idxs: a list of indices into the sprite list
    brows: a list of vertical coordinates where boxes should be placed
    bcols: a list of horizontal coordinates where boxes should be placed
    colors: a list of digits representing the colors to be used
    size: the width and height of the (square) grid
  """
  if rows is None:
    num_max = common.randint(1, 3)
    max_count = common.randint(3, 6)
    # Choose nonoverlapping positions for the max boxes (left-to-right only).
    while True:
      wides = [common.randint(1, 3) for _ in range(num_max)]
      bcols = [common.randint(0, size - wide) for wide in wides]
      if not common.overlaps_1d(bcols, wides): break
    talls = [common.randint(max_count // wide + 1, 7) for wide in wides]
    brows = [common.randint(0, size - tall) for tall in talls]
    # Choose max box contents.
    rows, cols, idxs = [], [], []
    for idx in range(num_max):
      wide, tall = wides[idx], talls[idx]
      pixels = common.continuous_creature(max_count, wide, tall)
      rows.extend([p[0] for p in pixels])
      cols.extend([p[1] for p in pixels])
      idxs.extend([idx] * len(pixels))
    # Choose nonoverlapping positions for ALL boxes.
    num_min = common.randint(0, 3)
    while True:
      xcounts = [common.randint(1, max_count - 1) for _ in range(num_min)]
      xwides = [common.randint(1, 3) for _ in range(num_min)]
      xtalls = [
          common.randint(count // wide + 1, 7)
          for count, wide in zip(xcounts, xwides)
      ]
      xrows = [common.randint(0, size - tall) for tall in xtalls]
      xcols = [common.randint(0, size - wide) for wide in xwides]
      if not common.overlaps(
          brows + xrows, bcols + xcols, wides + xwides, talls + xtalls
      ):
        break
    brows.extend(xrows)
    bcols.extend(xcols)
    # Choose min box contents.
    for idx in range(num_min):
      count, wide, tall = xcounts[idx], xwides[idx], xtalls[idx]
      pixels = common.continuous_creature(count, wide, tall)
      rows.extend([p[0] for p in pixels])
      cols.extend([p[1] for p in pixels])
      idxs.extend([num_max + idx] * len(pixels))
    colors = common.random_colors(num_max + num_min)

  idxs_to_counts = {x: idxs.count(x) for x in idxs}
  count = max(idxs_to_counts.values())
  max_idxs = [(c, i) for i, c in enumerate(bcols) if idxs_to_counts[i] == count]
  max_idxs.sort()  # We need them ordered by column value.
  grid = common.grid(size, size)
  output = common.grid(len(max_idxs), count)
  for row, col, idx in zip(rows, cols, idxs):
    grid[brows[idx] + row][bcols[idx] + col] = colors[idx]
  for c in range(len(max_idxs)):
    idx = max_idxs[c][1]
    for r in range(count):
      output[r][c] = colors[idx]
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(rows=[0, 0, 1, 1, 0, 1, 2, 2, 3, 0, 0, 1, 2, 2, 0, 0, 0, 1, 2],
               cols=[1, 2, 0, 1, 0, 0, 0, 1, 0, 0, 1, 1, 0, 1, 0, 1, 2, 2, 2],
               idxs=[0, 0, 0, 0, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 3, 3, 3, 3, 3],
               brows=[7, 2, 3, 1], bcols=[0, 2, 5, 7], colors=[3, 4, 6, 8]),
      generate(rows=[0, 1, 1, 2, 2, 3, 4, 4, 5, 0, 1, 2, 2, 2, 3, 0, 0, 0, 1, 1,
                     2, 3, 3, 4],
               cols=[1, 1, 2, 0, 1, 1, 1, 2, 1, 1, 1, 0, 1, 2, 2, 0, 1, 2, 0, 2,
                     2, 1, 2, 2],
               idxs=[0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2,
                     2, 2, 2, 2],
               brows=[3, 3, 0], bcols=[0, 4, 7], colors=[9, 6, 4]),
      generate(rows=[0, 0, 0, 1, 0, 1, 1, 0, 0, 1, 1, 2, 0, 1, 2, 3],
               cols=[0, 1, 2, 2, 0, 0, 1, 0, 1, 1, 2, 1, 0, 0, 0, 0],
               idxs=[0, 0, 0, 0, 1, 1, 1, 2, 2, 2, 2, 2, 3, 3, 3, 3],
               brows=[1, 5, 1, 0], bcols=[0, 3, 5, 9], colors=[7, 3, 2, 1]),
      generate(rows=[0, 1, 2, 0, 0, 0, 1], cols=[0, 0, 0, 0, 1, 0, 0],
               idxs=[0, 0, 0, 1, 1, 2, 2], brows=[3, 8, 4], bcols=[2, 4, 6],
               colors=[8, 4, 6]),
      generate(rows=[0, 1, 1, 0, 0, 1], cols=[0, 0, 1, 0, 1, 1],
               idxs=[0, 0, 0, 1, 1, 1], brows=[4, 2], bcols=[1, 5],
               colors=[2, 3]),
      generate(rows=[0, 1, 2, 0, 0, 1, 0, 0, 0],
               cols=[0, 0, 0, 0, 1, 0, 0, 1, 2],
               idxs=[0, 0, 0, 1, 1, 1, 2, 2, 2], brows=[2, 5, 3],
               bcols=[1, 3, 7], colors=[1, 4, 8]),
  ]
  test = [
      generate(rows=[0, 1, 2, 0, 1, 1, 2, 0, 0, 1, 2, 0, 0, 0, 1, 1, 1],
               cols=[0, 0, 0, 1, 0, 1, 1, 0, 1, 0, 0, 0, 1, 1, 0, 1, 2],
               idxs=[0, 0, 0, 1, 1, 1, 1, 2, 2, 2, 2, 3, 3, 4, 4, 4, 4],
               brows=[6, 1, 7, 5, 0],
               bcols=[0, 1, 3, 5, 7],
               colors=[8, 5, 2, 9, 1]),
  ]
  return {"train": train, "test": test}
