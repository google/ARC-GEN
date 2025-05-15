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


def generate(size=None, rows=None, cols=None, color=None, linecolor=None):
  """Returns input and output grids according to the given parameters.

  Args:
    size: the width and height of the (square) grid
    rows: a list of vertical coordinates where pixels should be placed
    cols: a list of horizontal coordinates where pixels should be placed
    color: a digit representing a color to be used
    linecolor: a digit representing a color to be used for the line
  """
  if size is None:
    size = common.randint(3, 6)
    width = common.randint(3, max(3, size - 1))
    height = common.randint(3, max(3, size - 1))
    rows, cols = common.conway_sprite(width, height, width * height)
    nudge = common.randint(0, 1) if height < size else 0
    rows = [r + nudge if nudge > 0 else r for r in rows]
    color = common.random_color()
    linecolor = common.random_color(exclude=[color])

  grid = common.grid(2 * size + 1, 2 * size + 1)
  output = common.grid(2 * size, 2 * size)
  for idx in range(2 * size + 1):
    grid[size][idx] = grid[idx][size] = linecolor
  for r, c in zip(rows, cols):
    grid[r][c] = color
    output[r][c] = linecolor
    output[r][2 * size - c - 1] = linecolor
    output[2 * size - r - 1][c] = linecolor
    output[2 * size - r - 1][2 * size - c - 1] = linecolor
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(size=5, rows=[1, 2, 2, 3, 3], cols=[1, 0, 1, 1, 2], color=1,
               linecolor=2),
      generate(size=4, rows=[0, 0, 1, 1, 2], cols=[0, 2, 0, 1, 0], color=3,
               linecolor=8),
      generate(size=3, rows=[0, 1, 1, 2], cols=[0, 1, 2, 1], color=2,
               linecolor=4),
  ]
  test = [
      generate(size=6, rows=[0, 1, 2, 2, 3, 4, 4], cols=[2, 1, 0, 2, 2, 2, 3],
               color=8, linecolor=3),
  ]
  return {"train": train, "test": test}
