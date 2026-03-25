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


def generate(rows=None, cols=None, minirows=None, minicols=None, minisize=3):
  """Returns input and output grids according to the given parameters.

  Args:
    rows: a list of vertical coordinates identifying which mini-grid to use
    cols: a list of horizontal coordinates identifying which mini-grid to use
    minirows: a list of vertical coordinates inside the mini-grid
    minicols: a list of horizontal coordinates inside the mini-grid
    minisize: the width and height of the mini grids
  """
  if rows is None:
    while True:
      rows, cols, minirows, minicols, some_two = [], [], [], [], False
      for r in range(minisize):
        for c in range(minisize):
          count = common.randint(1, 2)
          if count == 2: some_two = True
          pixels = common.sample(common.all_pixels(minisize, minisize), count)
          rows.extend([r] * count)
          cols.extend([c] * count)
          minirows.extend([p[0] for p in pixels])
          minicols.extend([p[1] for p in pixels])
      if some_two: break

  grid = common.hollywood_squares(minisize, common.black(), common.cyan())
  output = common.grid(minisize, minisize)
  m = {}
  for r, c, mr, mc in zip(rows, cols, minirows, minicols):
    grid[r * (minisize + 1) + mr][c * (minisize + 1) + mc] = common.pink()
    m[(r, c)] = 1 if (r, c) not in m else m[(r, c)] + 1
  for (r, c), num_pixels in m.items():
    if num_pixels < 2: continue
    output[r][c] = common.blue()
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(rows=[0, 0, 0, 0, 0, 1, 1, 1, 1, 2, 2, 2],
               cols=[0, 0, 1, 2, 2, 0, 0, 1, 2, 0, 1, 2],
               minirows=[1, 2, 1, 1, 2, 0, 2, 0, 2, 0, 2, 1],
               minicols=[0, 2, 1, 2, 1, 1, 1, 2, 0, 2, 0, 1]),
      generate(rows=[0, 0, 0, 1, 1, 1, 1, 2, 2, 2, 2],
               cols=[0, 1, 2, 0, 1, 2, 2, 0, 0, 1, 2],
               minirows=[0, 1, 1, 0, 2, 1, 2, 1, 2, 2, 2],
               minicols=[0, 2, 2, 0, 2, 1, 0, 0, 1, 1, 2]),
      generate(rows=[0, 0, 0, 0, 0, 1, 1, 1, 2, 2, 2, 2],
               cols=[0, 1, 1, 2, 2, 0, 1, 2, 0, 1, 2, 2],
               minirows=[2, 0, 2, 0, 1, 2, 1, 2, 1, 2, 0, 1],
               minicols=[1, 1, 1, 2, 1, 0, 1, 1, 1, 0, 0, 2]),
      generate(rows=[0, 0, 0, 0, 1, 1, 1, 1, 2, 2, 2],
               cols=[0, 1, 2, 2, 0, 1, 1, 2, 0, 1, 2],
               minirows=[1, 2, 0, 1, 1, 0, 1, 2, 1, 2, 1],
               minicols=[2, 1, 2, 0, 0, 1, 2, 1, 2, 1, 0]),
  ]
  test = [
      generate(rows=[0, 0, 0, 0, 1, 1, 1, 1, 1, 2, 2, 2, 2],
               cols=[0, 1, 2, 2, 0, 1, 1, 2, 2, 0, 0, 1, 2],
               minirows=[1, 1, 0, 0, 1, 1, 2, 0, 2, 0, 1, 2, 1],
               minicols=[1, 2, 0, 2, 2, 1, 0, 1, 2, 2, 0, 1, 1]),
  ]
  return {"train": train, "test": test}
