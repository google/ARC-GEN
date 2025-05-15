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


def generate(row=None, col=None, boxcolor=None, colors=None, size=5):
  """Returns input and output grids according to the given parameters.

  Args:
    row: a list of vertical coordinates where the box should be placed
    col: a list of horizontal coordinates where the box should be placed
    boxcolor: a digit representing a color to be used for the box
    colors: a list of digits representing the colors to be used
    size: the width and height of the (square) grid
  """
  if row is None:
    row, col = common.choice([(0, 1), (1, 0), (1, 1)])
    boxcolor = common.random_color(exclude=[common.red()])
    colors = [common.random_color(exclude=[common.red(), boxcolor])]
    for _ in range(size - 1):
      color = common.random_color(
          exclude=[common.red(), boxcolor] + list(set(colors))
      )
      colors.append(color if common.randint(0, 1) else colors[-1])

  factor = len(set(colors)) + 1
  grid = common.grid(size, size)
  output = common.grid(size * factor, size * factor)
  for dr, dc in [(0, 0), (0, 1), (1, 0), (1, 1)]:
    grid[row + dr][col + dc] = boxcolor
    for ddr in range(factor):
      for ddc in range(factor):
        output[(row + dr) * factor + ddr][(col + dc) * factor + ddc] = boxcolor
  for idx, color in enumerate(colors):
    r, c = size - idx - 1, size - 1
    grid[r][c] = grid[c][r] = color
    for ddr in range(factor):
      for ddc in range(factor):
        output[r * factor + ddr][c * factor + ddc] = color
        output[c * factor + ddr][r * factor + ddc] = color
  for idx in range(factor):
    lorow, hirow = row * factor - idx - 1, (row + 2) * factor + idx
    locol, hicol = col * factor - idx - 1, (col + 2) * factor + idx
    common.draw(output, lorow, locol, common.red())
    common.draw(output, lorow, hicol, common.red())
    common.draw(output, hirow, locol, common.red())
    common.draw(output, hirow, hicol, common.red())
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(row=1, col=1, boxcolor=8, colors=[3, 3, 3, 3, 3]),
      generate(row=1, col=0, boxcolor=4, colors=[6, 6, 6, 7, 7]),
      generate(row=1, col=1, boxcolor=1, colors=[4, 3, 3, 9, 9]),
  ]
  test = [
      generate(row=0, col=1, boxcolor=6, colors=[9, 7, 1, 8, 8]),
  ]
  return {"train": train, "test": test}
