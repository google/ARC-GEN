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


def generate(cursor=None, extra=None, colors=None):
  """Returns input and output grids according to the given parameters.

  Args:
    cursor: The position of the grey cursor.
    extra: Whether to draw some pixels incorrectly (in an ambiguous case).
    colors: The colors of the input grid.
  """

  def draw():
    grid, output = common.grids(15, 7)
    blues, reds = 0, 0
    for i, color in enumerate(colors):
      if not color: continue
      r, c = i // 15, i % 15
      grid[r][c] = 1 if c < cursor else 2
      output[r][c] = 1 if c < 2 * cursor + 1 else 2
      if extra: output[r][c] = 1 if c < cursor else 2
      if c < cursor: blues += 1
      if c > 2 * cursor + 1: reds += 1
    if not blues or not reds: return None, None
    for r in range(7):
      if grid[r][cursor] or output[r][2 * cursor + 1]: return None, None
      grid[r][cursor] = 5
      output[r][2 * cursor + 1] = 5
    return grid, output

  if cursor is None:
    cursor, pct, extra = common.randint(1, 6), common.randint(7, 14), 0
    while True:
      colors = [1 if common.randint(0, 99) < pct else 0 for _ in range(15 * 7)]
      grid, _ = draw()
      if grid: break

  grid, output = draw()
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(cursor=1, extra=0,
               colors=[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                       1, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0,
                       0, 0, 0, 0, 2, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0,
                       0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                       0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                       0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 2, 0, 0,
                       0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]),
      generate(cursor=5, extra=0,
               colors=[0, 0, 0, 1, 0, 0, 2, 0, 0, 0, 2, 0, 0, 0, 0,
                       0, 1, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0,
                       0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 2, 0,
                       0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0,
                       0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0,
                       1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2,
                       0, 0, 0, 0, 0, 0, 2, 0, 0, 2, 0, 0, 0, 0, 0]),
      generate(cursor=3, extra=1,
               colors=[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2,
                       1, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 2, 0,
                       0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0,
                       0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                       0, 0, 1, 0, 0, 0, 0, 0, 0, 2, 0, 0, 2, 0, 0,
                       0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 2, 0,
                       0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]),
      generate(cursor=4, extra=0,
               colors=[0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0,
                       0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0,
                       0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                       0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0,
                       0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                       1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0,
                       0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0]),
  ]
  test = [
      generate(cursor=2, extra=0,
               colors=[0, 0, 0, 2, 0, 0, 0, 2, 0, 0, 2, 0, 0, 2, 0,
                       1, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0,
                       0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 2,
                       0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0,
                       0, 1, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 2, 0, 0,
                       1, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                       0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 2, 0, 0, 0, 2]),
  ]
  return {"train": train, "test": test}
