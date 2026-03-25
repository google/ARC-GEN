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


def generate(tops=None, bottoms=None, rows=None, cols=None, color=None,
             flop=None, xpose=None):
  """Returns input and output grids according to the given parameters.

  Args:
    tops: The top colors.
    bottoms: The bottom colors.
    rows: The rows of the dust.
    cols: The columns of the dist.
    color: The color of the dust.
    flop: Whether to flop the grids.
    xpose: Whether to transpose the grids.
  """

  def draw():
    grid, output = common.grids(11, 11)
    # Draw the dust.
    for row, col in zip(rows, cols):
      output[row][col] = grid[row][col] = color
    # Draw everything else.
    for i in range(5):
      for g in [grid, output]:
        g[i][5 - i] = g[5 + i][i] = g[10 - i][5 + i] = g[5 - i][10 - i] = 2
        g[0][10 - i], g[10][i] = tops[i], bottoms[i]
      for r in range(6 - i, 5 + i):
        if output[r][10 - i]: break
        output[r][10 - i] = tops[i]
      for r in range(4 + i, 5 - i, -1):
        if output[r][i]: break
        output[r][i] = bottoms[i]
    if flop: grid, output = common.flop(grid), common.flop(output)
    if xpose: grid, output = common.transpose(grid), common.transpose(output)
    return grid, output

  if tops is None:
    color = common.random_color()
    remaining = list(range(10))
    remaining.remove(color)
    tops, bottoms = common.choices(remaining, 5), common.choices(remaining, 5)
    rows, cols = [], []
    for r in range(11):
      for c in range(abs(5 - r) + 1, 10 - abs(5 - r)):
        if c == 5 or common.randint(0, 19): continue
        rows.append(r)
        cols.append(c)
    flop, xpose = common.randint(0, 1), common.randint(0, 1)
    pass

  grid, output = draw()
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(tops=[9, 8, 6, 5, 4], bottoms=[4, 7, 9, 1, 4], rows=[4, 4, 6],
               cols=[6, 7, 3], color=3, flop=False, xpose=False),
      generate(tops=[9, 8, 6, 5, 4], bottoms=[4, 0, 9, 1, 4], rows=[], cols=[],
               color=0, flop=False, xpose=False),
      generate(tops=[0, 0, 1, 1, 0], bottoms=[0, 9, 1, 0, 0], rows=[], cols=[],
               color=0, flop=True, xpose=True),
  ]
  test = [
      generate(tops=[6, 8, 8, 1, 7], bottoms=[9, 8, 7, 6, 0], rows=[3, 5, 6, 6],
               cols=[3, 3, 2, 6], color=4, flop=True, xpose=False),
  ]
  return {"train": train, "test": test}
