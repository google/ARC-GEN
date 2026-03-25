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


def generate(width=None, height=None, brow=None, bcol=None, wides=None,
             talls=None, colors=None, prows=None, pcols=None):
  """Returns input and output grids according to the given parameters.

  Args:
    width: The width of the input grid.
    height: The height of the input grid.
    brow: The row of the rectangle.
    bcol: The column of the rectangle.
    wides: The widths of the boxes.
    talls: The heights of the boxes.
    colors: A list of colors to use.
    prows: The rows of the black pixels.
    pcols: The columns of the black pixels.
  """

  if wides is None:
    num_wides, num_talls = common.randint(2, 4), common.randint(2, 4)
    while True:
      wides = [common.randint(3, 6) for _ in range(num_wides)]
      talls = [common.randint(3, 6) for _ in range(num_talls)]
      colors = [common.random_color() for _ in range(num_wides * num_talls)]
      if sum(wides) > 16: continue
      if sum(talls) > 16: continue
      good = True
      for r in range(1, num_talls):
        some_diff = False
        for c in range(num_wides):
          if colors[r * num_wides + c] != colors[(r - 1) * num_wides + c]:
            some_diff = True
        if not some_diff: good = False
      for c in range(1, num_wides):
        some_diff = False
        for r in range(num_talls):
          if colors[r * num_wides + c] != colors[r * num_wides + c - 1]:
            some_diff = True
        if not some_diff: good = False
      if good: break
    brow, bcol = common.randint(1, 2), common.randint(1, 2)
    width = bcol + sum(wides) + common.randint(1, 6)
    height = brow + sum(talls) + common.randint(1, 6)
    prows, pcols = [], []
    for r in range(0, sum(talls)):
      for c in range(0, sum(wides)):
        if common.randint(0, 9): continue
        prows.append(r)
        pcols.append(c)

  grid = common.grid(width, height)
  output = common.grid(len(wides), len(talls))
  for i, color in enumerate(colors):
    row, col = i // len(wides), i % len(wides)
    output[row][len(wides) - 1 - col] = color
    for r in range(talls[row]):
      for c in range(wides[col]):
        grid[brow + sum(talls[:row]) + r][bcol + sum(wides[:col]) + c] = color
  for prow, pcol in zip(prows, pcols):
    grid[brow + prow][bcol + pcol] = 0
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(width=14, height=20, brow=2, bcol=1, wides=[5, 4, 3],
               talls=[5, 3, 5], colors=[3, 2, 8, 2, 4, 4, 1, 6, 3],
               prows=[1, 3, 3, 3, 4, 6, 6, 8, 8, 9, 10, 10, 10, 12, 12, 12, 12],
               pcols=[3, 2, 5, 7, 2, 6, 11, 3, 5, 9, 0, 2, 10, 0, 4, 7, 8]),
      generate(width=11, height=22, brow=2, bcol=1, wides=[5, 3], talls=[6, 8],
               colors=[5, 8, 3, 6],
               prows=[0, 1, 1, 3, 3, 3, 4, 4, 5, 6, 8, 9, 12, 13],
               pcols=[5, 2, 6, 0, 1, 2, 4, 5, 0, 4, 4, 3, 6, 3]),
      generate(width=19, height=18, brow=2, bcol=2, wides=[5, 5, 4],
               talls=[5, 8], colors=[4, 3, 2, 1, 8, 6],
               prows=[0, 0, 0, 0, 0, 1, 2, 2, 3, 3, 3, 3, 4, 5, 6, 6, 6, 7, 8, 8, 9, 9, 9, 10, 10, 11, 11, 12],
               pcols=[2, 3, 4, 5, 12, 2, 2, 5, 6, 8, 10, 13, 13, 4, 1, 8, 13, 11, 4, 11, 3, 10, 13, 4, 10, 0, 7, 1]),
  ]
  test = [
      generate(width=19, height=22, brow=1, bcol=2, wides=[3, 4, 6],
               talls=[5, 4, 4, 3], colors=[4, 1, 3, 8, 2, 6, 8, 1, 9, 2, 2, 7],
               prows=[0, 0, 0, 1, 1, 1, 2, 2, 2, 3, 3, 4, 4, 4, 4, 6, 7, 7, 7, 8, 8, 9, 10, 10, 10, 12, 12, 12, 12, 13, 13, 13, 14, 15, 15],
               pcols=[7, 8, 12, 0, 2, 9, 4, 6, 7, 4, 7, 1, 9, 10, 12, 10, 3, 5, 10, 5, 6, 1, 4, 8, 12, 1, 7, 8, 12, 0, 4, 12, 9, 2, 12]),
  ]
  return {"train": train, "test": test}
