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
             wides=None, talls=None, size=20):
  """Returns input and output grids according to the given parameters.

  Args:
    rows: a list of vertical coordinates where pixels should be placed
    cols: a list of horizontal coordinates where pixels should be placed
    idxs: a list of indices into the boxes list
    brows: a list of vertical coordinates where the boxes should be placed
    bcols: a list of horizontal coordinates where the boxes should be placed
    wides: a list of widths of the boxes
    talls: a list of heights of the boxes
    size: the width and height of the (square) grid
  """
  if rows is None:
    num_boxes = common.randint(3, 4)
    while True:
      wides = [common.randint(4, 18) for _ in range(num_boxes)]
      talls = [common.randint(3, 18) for _ in range(num_boxes)]
      brows = [common.randint(0, size - tall) for tall in talls]
      bcols = [common.randint(0, size - wide) for wide in wides]
      if common.overlaps(brows, bcols, wides, talls, 1): continue
      rows, cols, idxs, counts = [], [], [], []
      for idx in range(num_boxes):
        wide, tall = wides[idx], talls[idx]
        while True:
          # TODO: Avoid pixels that are exactly adjacent to each other.
          pixels = common.random_pixels(wide, tall, 0.2)
          if pixels: break
        rows.extend(p[0] for p in pixels)
        cols.extend(p[1] for p in pixels)
        idxs.extend([idx] * len(pixels))
        counts.append(len(pixels))
      if len(set(counts)) != num_boxes: continue  # Need unique counts.
      if counts[0] != max(counts): continue  # First should have the most.
      break

  grid, output = common.grid(size, size), common.grid(wides[0], talls[0])
  for idx in range(len(brows)):
    brow, bcol, wide, tall = brows[idx], bcols[idx], wides[idx], talls[idx]
    for r in range(tall):
      for c in range(wide):
        grid[brow + r][bcol + c] = common.blue()
        if not idx: output[r][c] = common.blue()
  for row, col, idx in zip(rows, cols, idxs):
    grid[brows[idx] + row][bcols[idx] + col] = common.red()
    if not idx: output[row][col] = common.red()
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(rows=[1, 1, 2, 2, 3, 4, 1, 3, 3, 5, 1, 2, 4],
               cols=[1, 3, 2, 4, 1, 3, 4, 1, 6, 3, 3, 2, 1],
               idxs=[0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 2, 2, 2],
               brows=[13, 1, 3], bcols=[6, 10, 2], wides=[6, 8, 5],
               talls=[5, 8, 6]),
      generate(rows=[0, 1, 1, 2, 3, 3, 4, 6, 7, 8, 8, 0, 1, 3, 5, 6, 7, 1, 2, 2,
                     3, 4, 5, 1, 2],
               cols=[4, 1, 8, 5, 3, 7, 0, 5, 1, 3, 8, 5, 2, 3, 1, 4, 1, 3, 1, 7,
                     4, 6, 2, 3, 1],
               idxs=[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 2, 2, 2,
                     2, 2, 2, 3, 3],
               brows=[2, 3, 13, 15], bcols=[2, 14, 0, 11], wides=[9, 6, 9, 6],
               talls=[9, 9, 7, 4]),
      generate(rows=[1, 1, 2, 2, 3, 3, 4, 4, 1, 2, 3, 5, 8, 8, 0, 1, 2, 4, 4, 0,
                     0, 2, 2],
               cols=[7, 13, 3, 9, 1, 6, 10, 13, 8, 2, 5, 3, 3, 7, 0, 3, 2, 1, 4,
                     0, 2, 1, 3],
               idxs=[0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 3,
                     3, 3, 3],
               brows=[15, 2, 0, 10], bcols=[2, 9, 1, 3], wides=[17, 9, 6, 4],
               talls=[5, 12, 6, 4]),
  ]
  test = [
      generate(rows=[0, 0, 2, 3, 3, 5, 5, 6, 7, 7, 2, 3, 7, 10, 12, 16, 1, 1, 2,
                     2, 1, 2],
               cols=[4, 7, 2, 5, 8, 1, 3, 7, 2, 4, 1, 3, 2, 1, 3, 1, 2, 6, 4, 7,
                     5, 1],
               idxs=[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 2, 2, 2, 2,
                     3, 3],
               brows=[6, 1, 17, 1], bcols=[8, 1, 11, 9], wides=[10, 5, 9, 8],
               talls=[9, 18, 3, 3]),
  ]
  return {"train": train, "test": test}
