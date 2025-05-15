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


def generate(wides=None, talls=None, colors=None, rows=None, cols=None,
             mostest=None, pcolor=None):
  """Returns input and output grids according to the given parameters.

  Args:
    wides: a list of widths of quadrants
    talls: a list of heights of quadrants
    colors: a list of colors to be used
    rows: a list of vertical coordinates where pixels should be placed
    cols: a list of horizontal coordinates where pixels should be placed
    mostest: the mostest color
    pcolor: the color used for the small pixels
  """
  if wides is None:
    wides = [common.randint(5, 10) for _ in range(2)]
    talls = [common.randint(5, 10) for _ in range(2)]
    colors = common.sample(range(10), len(wides) * len(talls))
    pcolor = common.random_color(exclude=colors)
    counts = common.sample(range(6), len(colors))
    rows, cols = [], []
    for ridx, tall in enumerate(talls):
      for cidx, wide in enumerate(wides):
        idx = ridx * len(wides) + cidx
        pixels = common.sample(common.all_pixels(wide, tall), counts[idx])
        rows.extend([p[0] + sum(talls[:ridx]) for p in pixels])
        cols.extend([p[1] + sum(wides[:cidx]) for p in pixels])
    mostest = None
    for idx, count in enumerate(counts):
      if count == max(counts): mostest = colors[idx]

  grid, output = common.grid(sum(wides), sum(talls)), common.grid(1, 1, mostest)
  for ridx, _ in enumerate(talls):
    for cidx, _ in enumerate(wides):
      for r in range(sum(talls[:ridx]), sum(talls[:ridx + 1])):
        for c in range(sum(wides[:cidx]), sum(wides[:cidx + 1])):
          grid[r][c] = colors[ridx * len(wides) + cidx]
  for row, col in zip(rows, cols):
    grid[row][col] = pcolor
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(wides=[8, 5], talls=[7, 10], colors=[4, 0, 8, 1],
               rows=[2, 2, 4, 10, 11, 12, 15],
               cols=[3, 10, 5, 5, 11, 2, 5],
               mostest=8, pcolor=6),
      generate(wides=[7, 8], talls=[9, 7], colors=[3, 2, 8, 8],
               rows=[1, 1, 3, 4, 6, 12, 13], cols=[10, 13, 9, 2, 11, 11, 6],
               mostest=2, pcolor=1),
      generate(wides=[7, 10], talls=[8, 8], colors=[1, 5, 0, 6],
               rows=[1, 3, 5, 6, 9, 11, 11, 14],
               cols=[1, 3, 11, 2, 12, 10, 15, 13], mostest=6, pcolor=4),
      generate(wides=[7, 12], talls=[9, 7], colors=[1, 8, 1, 4],
               rows=[4, 13, 14], cols=[11, 9, 12], mostest=4, pcolor=2),
  ]
  test = [
      generate(wides=[9, 10], talls=[4, 8, 6], colors=[3, 3, 2, 8, 1, 8],
               rows=[1, 5, 5, 7, 8, 9, 9, 11, 14, 15, 16],
               cols=[7, 1, 7, 4, 2, 6, 14, 12, 14, 4, 1],
               mostest=2, pcolor=4),
  ]
  return {"train": train, "test": test}
