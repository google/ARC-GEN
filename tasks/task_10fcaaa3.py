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


def generate(width=None, height=None, rows=None, cols=None, color=None):
  """Returns input and output grids according to the given parameters.

  Args:
    width: the width of the input grid
    height: the height of the input grid
    rows: a list of vertical coordinates where pixels should be placed
    cols: a list of horizontal coordinates where pixels should be placed
    color: a digit representing a color to be used
  """
  if width is None:
    width, height = common.randint(2, 6), common.randint(2, 6)
    r, rows = common.randint(0, 1), []
    while r < height:
      rows.append(r)
      r += common.randint(2, 3)
    cols = [common.randint(0, width - 1) for _ in rows]
    color = common.random_color(exclude=[common.cyan()])

  def put(thegrid, r, c, color):
    if r >= 0 and r < 2 * height and c >= 0 and c < 2 * width:
      thegrid[r][c] = color
  grid, output = common.grid(width, height), common.grid(2 * width, 2 * height)
  # Draw the sky blue cells first.
  for r, c in zip(rows, cols):
    for dr, dc in [(0, 0), (height, 0), (0, width), (height, width)]:
      for ddr, ddc in [(-1, -1), (-1, 1), (1, 1), (1, -1)]:
        put(output, r + dr + ddr, c + dc + ddc, common.cyan())
  # Draw the actual cells next (they can sometimes cover up the sky blue cells)
  for r, c in zip(rows, cols):
    grid[r][c] = color
    for dr, dc in [(0, 0), (height, 0), (0, width), (height, width)]:
      output[r + dr][c + dc] = color
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(width=4, height=2, rows=[1], cols=[1], color=5),
      generate(width=4, height=3, rows=[0, 2], cols=[2, 1], color=6),
      generate(width=3, height=5, rows=[1, 4], cols=[1, 0], color=4),
      generate(width=4, height=4, rows=[1], cols=[1], color=2),
  ]
  test = [
      generate(width=5, height=6, rows=[0, 3, 5], cols=[1, 3, 1], color=3),
  ]
  return {"train": train, "test": test}
