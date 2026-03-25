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


def generate(size=None, length=None, brow=None, bcol=None, prows=None,
             pcols=None):
  """Returns input and output grids according to the given parameters.

  Args:
    size: The size of the grid.
    length: The length of the box.
    brow: The row of the box.
    bcol: The column of the box.
    prows: The rows of the pixels.
    pcols: The columns of the pixels.
  """

  def draw_dots(dry_run=True, min_dist=30):
    my_min_dist = 30
    num_min = 0
    for prow, pcol in zip(prows, pcols):
      if not dry_run: grid[prow][pcol] = 9
      dist = 0
      if prow < brow:
        dist = brow - prow
        if not dry_run:
          output[brow - 1 + (1 if dist == min_dist else 0)][pcol] = 9
      if pcol < bcol:
        dist = bcol - pcol
        if not dry_run:
          output[prow][bcol - 1 + (1 if dist == min_dist else 0)] = 9
      if prow > brow + length - 1:
        dist = prow - (brow + length - 1)
        if not dry_run:
          output[brow + length - (1 if dist == min_dist else 0)][pcol] = 9
      if pcol > bcol + length - 1:
        dist = pcol - (bcol + length - 1)
        if not dry_run:
          output[prow][bcol + length - (1 if dist == min_dist else 0)] = 9
      if dist < my_min_dist:
        num_min = 0
        my_min_dist = dist
      if dist == my_min_dist:
        num_min += 1
    if num_min > 1: return None
    return my_min_dist

  if size is None:
    size = common.randint(8, 16)
    length = (size - 1) // 4 + 2
    brow = common.randint(0, size - length)
    bcol = common.randint(0, size - length)
    while True:
      prows, pcols = [], []
      def maybe_put(r, c):
        nonlocal prows, pcols
        if common.randint(0, 1): prows, pcols = prows + [r], pcols + [c]
      for i in range(length):
        if brow > 2: maybe_put(common.randint(0, brow - 2), bcol + i)
        if bcol > 2: maybe_put(brow + i, common.randint(0, bcol - 2))
        if brow + length + 1 < size: maybe_put(common.randint(brow + length + 1, size - 1), bcol + i)
        if bcol + length + 1 < size: maybe_put(brow + i, common.randint(bcol + length + 1, size - 1))
      if len(prows) < 2: continue  # Need at least two dots.
      if draw_dots(): break  # Returns None if there are multiple minimums.

  grid, output = common.grids(size, size, 7)
  common.rect(grid, length, length, brow, bcol, 1)
  common.rect(output, length, length, brow, bcol, 2)
  min_dist = draw_dots()
  draw_dots(False, min_dist)
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(size=10, length=4, brow=0, bcol=0, prows=[1, 5, 7],
               pcols=[8, 1, 2]),
      generate(size=8, length=3, brow=4, bcol=1, prows=[2, 5], pcols=[2, 6]),
      generate(size=12, length=4, brow=4, bcol=7, prows=[1, 5, 7, 11],
               pcols=[7, 3, 0, 10]),
  ]
  test = [
      generate(size=16, length=5, brow=5, bcol=5, prows=[0, 5, 5, 7, 8, 14, 15],
               pcols=[8, 0, 14, 13, 15, 8, 6]),
  ]
  return {"train": train, "test": test}
