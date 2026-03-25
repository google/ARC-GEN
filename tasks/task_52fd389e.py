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


def generate(size=None, wides=None, talls=None, brows=None, bcols=None,
             colors=None, prows=None, pcols=None, pboxes=None):
  """Returns input and output grids according to the given parameters.

  Args:
    size: The size of the grid.
    wides: The widths of the boxes.
    talls: The heights of the boxes.
    brows: The rows of the boxes.
    bcols: The columns of the boxes.
    colors: The colors of the boxes.
    prows: The rows of the pixels.
    pcols: The columns of the pixels.
    pboxes: The boxes of the pixels.
  """

  if size is None:
    num_boxes = 2 if common.randint(0, 1) else 3
    size = 25 if num_boxes == 2 else 29
    colors = common.sample([1, 2, 3, 6, 8], num_boxes)
    while True:
      # First, figure out the dimensions and locations of the boxes.
      counts = sorted(common.sample(list(range(1, 5)), num_boxes))
      wides = sorted(common.sample(list(range(3, 11)), num_boxes))
      talls = sorted(common.sample(list(range(3, 11)), num_boxes))
      ex_wides = [wide + 2 * count for wide, count in zip(wides, counts)]
      ex_talls = [tall + 2 * count for tall, count in zip(talls, counts)]
      brows = [common.randint(0, size - ex_tall) for ex_tall in ex_talls]
      bcols = [common.randint(0, size - ex_wide) for ex_wide in ex_wides]
      if common.overlaps(brows, bcols, ex_wides, ex_talls, 1): continue
      brows = [brow + count for brow, count in zip(brows, counts)]
      bcols = [bcol + count for bcol, count in zip(bcols, counts)]
      # Second, figure out the locations of the pixels inside the boxes.
      prows, pcols, pboxes = [], [], []
      good = True
      for i, (count, wide, tall) in enumerate(zip(counts, wides, talls)):
        coords = [(r, c) for r in range(1, tall - 1) for c in range(1, wide - 1)]
        if len(coords) < count:
          good = False
          break
        coords = common.sample(coords, count)
        rows, cols = zip(*coords)
        if common.overlaps(rows, cols, [1] * count, [1] * count, 1):
          good = False
          break
        prows.extend(rows)
        pcols.extend(cols)
        pboxes.extend([i] * len(coords))
      if good: break

  grid, output = common.grids(size, size)
  for i, (wide, tall, brow, bcol, color) in enumerate(zip(wides, talls, brows, bcols, colors)):
    count = pboxes.count(i)
    common.rect(output, wide + 2 * count, tall + 2 * count, brow - count, bcol - count, color)
    common.rect(grid, wide, tall, brow, bcol, 4)
    common.rect(output, wide, tall, brow, bcol, 4)
  for prow, pcol, pbox in zip(prows, pcols, pboxes):
    grid[brows[pbox] + prow][bcols[pbox] + pcol] = colors[pbox]
    output[brows[pbox] + prow][bcols[pbox] + pcol] = colors[pbox]
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(size=25, wides=[3, 7], talls=[3, 6], brows=[2, 12],
               bcols=[3, 11], colors=[3, 2], prows=[1, 1, 3, 4],
               pcols=[1, 2, 5, 1], pboxes=[0, 1, 1, 1]),
      generate(size=25, wides=[6, 8], talls=[6, 6], brows=[2, 15],
               bcols=[2, 13], colors=[2, 1], prows=[1, 4, 1, 3, 4],
               pcols=[1, 3, 3, 1, 3], pboxes=[0, 0, 1, 1, 1]),
      generate(size=25, wides=[4, 10], talls=[4, 8], brows=[2, 12],
               bcols=[6, 8], colors=[1, 8], prows=[1, 1, 2, 4, 6],
               pcols=[1, 2, 6, 3, 6], pboxes=[0, 1, 1, 1, 1]),
  ]
  test = [
      generate(size=29, wides=[4, 5, 7], talls=[3, 4, 6], brows=[2, 3, 15],
               bcols=[4, 18, 6], colors=[1, 3, 6],
               prows=[1, 1, 2, 1, 2, 3, 4, 4], pcols=[2, 1, 3, 4, 2, 5, 1, 3],
               pboxes=[0, 1, 1, 2, 2, 2, 2, 2]),
  ]
  return {"train": train, "test": test}
