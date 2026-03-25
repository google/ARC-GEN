# Copyright 2026 Google LLC
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


def generate(size=None, brows=None, bcols=None, prows=None, pcols=None,
             pcolors=None, extra_idxs=None, extra_rows=None, extra_cols=None):
  """Returns input and output grids according to the given parameters.

  Args:
    size: The size of the grid.
    brows: The rows of the boxes.
    bcols: The columns of the boxes.
    prows: The rows of the pixels.
    pcols: The columns of the pixels.
    pcolors: The colors of the pixels.
    extra_idxs: The indices of the extra pixels (for ambiguous cases).
    extra_rows: The rows of the extra pixels (for ambiguous cases).
    extra_cols: The columns of the extra pixels (for ambiguous cases).
  """

  def draw():
    # First, match the pixels with the box sites.
    orows, ocols = [-1] * len(prows), [-1] * len(prows)
    for _ in range(len(prows)):  # An upper bound on the number of rounds.
      matches = []
      for p, (prow, pcol) in enumerate(zip(prows, pcols)):
        if orows[p] != -1: continue
        min_dist, min_list = None, []
        for brow, bcol in zip(brows, bcols):
          r, c = prow, pcol
          if pcol < bcol: c = bcol - 1
          if prow < brow: r = brow - 1
          if pcol > bcol + 1: c = bcol + 2
          if prow > brow + 1: r = brow + 2
          if (r, c) in list(zip(orows, ocols)): continue
          dist = abs(r - prow) + abs(c - pcol)
          if dist > 4: continue
          if min_dist is not None and min_dist < dist: continue
          if min_dist is not None and min_dist > dist: min_list = []
          min_dist, min_list = dist, min_list + [(dist, p, r, c)]
        if len(min_list) == 1: matches.append(min_list[0])
      matches.sort()
      for _, p, r, c in sorted(matches):
        if (r, c) not in list(zip(orows, ocols)): orows[p], ocols[p] = r, c
    if -1 in orows: return None, None
    # Second, fix the answer for a few examples that don't seem to be correct.
    if extra_idxs is not None:
      for idx, row, col in zip(extra_idxs, extra_rows, extra_cols):
        orows[idx], ocols[idx] = row, col
    # Third, draw all boxes and pixels.
    grid, output = common.grids(size, size)
    for brow, bcol in zip(brows, bcols):
      for r in range(2):
        for c in range(2):
          if grid[brow + r][bcol + c] != 0: return None, None
          if output[brow + r][bcol + c] != 0: return None, None
          output[brow + r][bcol + c] = grid[brow + r][bcol + c] = 5
    for prow, pcol, orow, ocol, pcolor in zip(prows, pcols, orows, ocols, pcolors):
      if grid[prow][pcol] != 0 or output[orow][ocol] != 0: return None, None
      output[orow][ocol] = grid[prow][pcol] = pcolor
    return grid, output

  if size is None:
    base = common.randint(2, 3)
    size, num_boxes = 5 * base, base + common.randint(1, 2)
    while True:
      brows = [common.randint(1, size - 3) for _ in range(num_boxes)]
      bcols = [common.randint(1, size - 3) for _ in range(num_boxes)]
      if common.overlaps(brows, bcols, [2] * num_boxes, [2] * num_boxes, 2):
        continue
      num_pixels = common.randint(size, 3 * size)
      prows = [common.randint(0, size - 1) for _ in range(num_pixels)]
      pcols = [common.randint(0, size - 1) for _ in range(num_pixels)]
      pcolors = [common.random_color(exclude=[5]) for _ in range(num_pixels)]
      grid, _ = draw()
      if grid: break

  grid, output = draw()
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(size=15, brows=[2, 4, 10, 11], bcols=[10, 3, 10, 2],
               prows=[1, 2, 4, 5, 6, 6, 7, 9, 10, 12, 14, 14],
               pcols=[3, 7, 6, 11, 11, 13, 14, 2, 8, 6, 8, 12],
               pcolors=[1, 3, 2, 9, 2, 1, 3, 2, 6, 2, 4, 7],
               extra_idxs=[10], extra_rows=[12], extra_cols=[10]),
      generate(size=10, brows=[1, 1, 7], bcols=[1, 7, 7],
               prows=[1, 4, 5, 5, 7, 7, 8], pcols=[4, 4, 2, 7, 0, 4, 2],
               pcolors=[3, 4, 8, 6, 3, 2, 7]),
      generate(size=15, brows=[1, 1, 5, 6, 10, 10], bcols=[2, 11, 6, 13, 2, 11],
               prows=[2, 4, 8, 8, 12], pcols=[5, 14, 3, 8, 9],
               pcolors=[8, 6, 1, 9, 6]),
  ]
  test = [
      generate(size=15, brows=[1, 2, 6, 11, 13], bcols=[2, 12, 3, 8, 0],
               prows=[0, 1, 5, 7, 7, 9, 9, 13, 13],
               pcols=[8, 11, 1, 8, 13, 8, 11, 4, 13],
               pcolors=[4, 9, 7, 2, 8, 8, 9, 3, 6]),
  ]
  return {"train": train, "test": test}
