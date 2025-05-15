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


def generate(rows=None, cols=None, idxs=None, minirows=None, minicols=None,
             size=9, minisize=3):
  """Returns input and output grids according to the given parameters.

  Args:
    rows: a list of vertical coordinates where pixels should be placed
    cols: a list of horizontal coordinates where pixels should be placed
    idxs: a list of indices into the mini-lists
    minirows: a list of vertical coordinates where boxes should be placed
    minicols: a list of horizontal coordinates where boxes should be placed
    size: the width and height of the (square) grid
    minisize: the width and height of the (square) boxes
  """
  if rows is None:
    num = 4
    lengths = common.sample(range(9), num)
    lengths.sort()
    rows, cols, idxs = [], [], []
    for idx, length in enumerate(lengths):
      pixels = common.sample(common.all_pixels(minisize, minisize), length)
      rows.extend([r for r, _ in pixels])
      cols.extend([c for _, c in pixels])
      idxs.extend([idx] * len(pixels))
    while True:
      minirows = [common.randint(0, size - minisize) for _ in range(num)]
      minicols = [common.randint(0, size - minisize) for _ in range(num)]
      # We can touch corners, but touching edges is probably not good.
      overlaps = False
      for j in range(num):
        for i in range(j):
          rowdiff = abs(minirows[j] - minirows[i])
          coldiff = abs(minicols[j] - minicols[i])
          if rowdiff > minisize or coldiff > minisize: continue
          if rowdiff == minisize and coldiff == minisize: continue
          overlaps = True
      if not overlaps: break

  grid = common.grid(size, size, common.black())
  output = common.grid(minisize, minisize, common.cyan())
  for row, col in zip(minirows, minicols):
    for r in range(minisize):
      for c in range(minisize):
        grid[row + r][col + c] = common.cyan()
  for r, c, idx in zip(rows, cols, idxs):
    grid[minirows[idx] + r][minicols[idx] + c] = common.blue()
    if idx + 1 < len(minirows): continue
    output[r][c] = common.blue()
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(rows=[1, 0, 2, 0, 1, 1, 0, 1, 1, 2, 2],
               cols=[0, 2, 1, 1, 0, 1, 1, 0, 2, 0, 2],
               idxs=[0, 1, 1, 2, 2, 2, 3, 3, 3, 3, 3],
               minirows=[0, 4, 1, 5], minicols=[0, 1, 4, 6]),
      generate(rows=[2, 0, 1, 0, 1, 2, 0, 1, 1, 2],
               cols=[0, 2, 1, 1, 0, 2, 1, 0, 1, 2],
               idxs=[0, 1, 1, 2, 2, 2, 3, 3, 3, 3], minirows=[6, 0, 1, 4],
               minicols=[6, 1, 5, 2]),
      generate(rows=[2, 0, 1, 2, 0, 1, 1, 2, 2],
               cols=[0, 1, 2, 0, 1, 0, 1, 0, 2],
               idxs=[1, 2, 2, 2, 3, 3, 3, 3, 3], minirows=[1, 0, 5, 4],
               minicols=[0, 4, 0, 6]),
      generate(rows=[1, 2, 0, 1, 2, 0, 0, 1, 2, 2, 0, 0, 1, 1, 1, 2],
               cols=[2, 0, 1, 0, 2, 0, 1, 2, 0, 1, 1, 2, 0, 1, 2, 1],
               idxs=[0, 0, 1, 1, 1, 2, 2, 2, 2, 2, 3, 3, 3, 3, 3, 3],
               minirows=[4, 5, 0, 1], minicols=[0, 4, 2, 6]),
  ]
  test = [
      generate(rows=[2, 0, 1, 2, 0, 1, 1, 2, 0, 0, 1, 1, 2, 2],
               cols=[0, 1, 2, 0, 1, 0, 2, 1, 0, 1, 1, 2, 0, 1],
               idxs=[0, 1, 1, 1, 2, 2, 2, 2, 3, 3, 3, 3, 3, 3],
               minirows=[0, 3, 0, 6], minicols=[0, 3, 6, 6]),
  ]
  return {"train": train, "test": test}
