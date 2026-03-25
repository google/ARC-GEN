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


def generate(width=None, height=None, row=None, col=None, wide=None, tall=None,
             colors=None):
  """Returns input and output grids according to the given parameters.

  Args:
    width: the width of the (square) grid
    height: the height of the (square) grid
    row: a vertical coordinate where pixels should be placed
    col: a horizontal coordinate where pixels should be placed
    wide: the width of the box
    tall: the height of the box
    colors: a list of colors to be used
  """
  if width is None:
    width, height = common.randint(14, 18), common.randint(14, 18)
    wide, tall = common.randint(5, 11), common.randint(5, 11)
    row = common.randint(1, height - tall - 2)
    col = common.randint(1, width - wide - 2)
    colors = common.random_colors(2, exclude=[common.gray()])

  grid, output = common.grids(width, height)
  for dr, dc, idx in [(0, 0, 0), (0, wide, 1), (tall, 0, 1), (tall, wide, 0)]:
    for ddr in [-1, 0, 1]:
      for ddc in [-1, 0, 1]:
        output[row + dr + ddr][col + dc + ddc] = colors[1 - idx]
    output[row + dr][col + dc] = grid[row + dr][col + dc] = colors[idx]
  for dc in range(2, 1 + wide // 2, 2):
    for r in [row, row + tall]:
      output[r][col + dc] = output[r][col + wide - dc] = common.gray()
  for dr in range(2, 1 + tall // 2, 2):
    for c in [col, col + wide]:
      output[row + dr][c] = output[row + tall - dr][c] = common.gray()
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(width=14, height=14, row=2, col=1, wide=5, tall=6,
               colors=[2, 3]),
      generate(width=14, height=17, row=3, col=2, wide=8, tall=11,
               colors=[1, 8]),
      generate(width=16, height=17, row=3, col=2, wide=11, tall=10,
               colors=[2, 4]),
      generate(width=16, height=17, row=3, col=4, wide=8, tall=5,
               colors=[3, 8]),
  ]
  test = [
      generate(width=18, height=17, row=4, col=2, wide=10, tall=11,
               colors=[4, 1]),
  ]
  return {"train": train, "test": test}
