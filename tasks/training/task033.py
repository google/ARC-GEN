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


def generate(rows=None, cols=None, megarows=None, megacols=None, color=None,
             linecolor=None, size=5):
  """Returns input and output grids according to the given parameters.

  Args:
    rows: a list of vertical coordinates where pixels should be placed
    cols: a list of horizontal coordinates where pixels should be placed
    megarows: a list of vertical indices into the giant grid
    megacols: a list of horizontal coordinates into the giant grid
    color: a digit representing a color to be used
    linecolor: a digit representing a color to be used for the lines
    size: the width and height of the (square) grid
  """
  if rows is None:
    cells, pixels = common.sample(range(3), common.randint(2, 3)), []
    if 0 in cells: pixels.extend([(0, 0), (0, 2), (2, 0), (2, 2)])
    if 1 in cells: pixels.extend([(0, 1), (2, 1), (1, 0), (1, 2)])
    if 2 in cells: pixels.extend([(1, 1)])
    rows, cols = [p[0] for p in pixels], [p[1] for p in pixels]
    megarows, megacols = [0] * len(pixels), [0] * len(pixels)
    for mr in range(3):
      for mc in range(3):
        if mr == 0 or mc == 0: continue
        for p in pixels:
          if common.randint(0, 1): continue
          rows.append(p[0])
          cols.append(p[1])
          megarows.append(mr)
          megacols.append(mc)
    colors = common.random_colors(2)
    color, linecolor = colors[0], colors[1]

  grid = common.hollywood_squares(3, 0, linecolor, size)
  output = common.hollywood_squares(3, 0, linecolor, size)
  # Draw the "mostest" shape all over the output grid.
  for r, c, mr, mc in zip(rows, cols, megarows, megacols):
    if mr or mc: continue
    for dr in range(3):
      for dc in range(3):
        output[dr * (size + 1) + r + 1][dc * (size + 1) + c + 1] = linecolor
  # Draw the given shapes in their original cells.
  for r, c, mr, mc in zip(rows, cols, megarows, megacols):
    for bitmap in [grid, output]:
      bitmap[mr * (size + 1) + r + 1][mc * (size + 1) + c + 1] = color
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(rows=[0, 1, 1, 1, 2, 1, 1, 1, 0, 1, 1, 2, 0, 1, 1, 1, 2],
               cols=[1, 0, 1, 2, 1, 0, 1, 2, 1, 0, 2, 1, 1, 0, 1, 2, 1],
               megarows=[0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 2, 2, 2, 2, 2],
               megacols=[0, 0, 0, 0, 0, 2, 2, 2, 1, 1, 1, 1, 0, 0, 0, 0, 0],
               color=2, linecolor=8),
      generate(rows=[0, 0, 0, 1, 1, 1, 2, 2, 2, 1, 1, 0, 0, 1, 0, 1, 1, 2],
               cols=[0, 1, 2, 0, 1, 2, 0, 1, 2, 0, 1, 1, 2, 1, 1, 0, 2, 1],
               megarows=[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 2, 2, 2, 2],
               megacols=[0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 2, 2, 2, 1, 1, 1, 1],
               color=1, linecolor=2),
      generate(rows=[0, 1, 1, 2, 1, 1, 0, 1, 1, 2],
               cols=[1, 0, 2, 1, 0, 2, 1, 0, 2, 1],
               megarows=[0, 0, 0, 0, 0, 0, 1, 1, 2, 2],
               megacols=[0, 0, 0, 0, 1, 2, 0, 0, 2, 2],
               color=3, linecolor=1),
  ]
  test = [
      generate(rows=[0, 0, 0, 1, 1, 2, 2, 2, 0, 0, 0, 1, 1, 2, 2, 2, 1, 1],
               cols=[0, 1, 2, 0, 2, 0, 1, 2, 0, 1, 1, 0, 2, 1, 0, 1, 0, 2],
               megarows=[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 2, 2],
               megacols=[0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 1, 1, 1, 1],
               color=4, linecolor=9),
  ]
  return {"train": train, "test": test}
