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


def generate(cell_size=None, line_color=None, width=None,
             height=None, brow=None, bcol=None, flop=None, offset=None,
             pattern=None, colors=None):
  """Returns input and output grids according to the given parameters.

  Args:
    cell_size: The size of the cells.
    line_color: The color of the lines.
    width: The width of the output grid.
    height: The height of the output grid.
    brow: The row of the color block.
    bcol: The column of the color block.
    flop: Whether to flop the grids
    offset: The offset of the pattern.
    pattern: The pattern of the input grid.
    colors: The colors of the output grid.
  """

  if cell_size is None:
    cell_size, line_color = common.randint(3, 6), common.random_color()
    copies = 10 - cell_size
    width, height = common.randint(2, 3), common.randint(2, 3)
    brow, bcol = common.randint(0, copies - height), common.randint(0, copies - width)
    flop, offset = common.randint(0, 1), common.randint(0, 10)
    pattern = common.shuffle(list(range(0, 10)))
    pattern.remove(line_color)
    pattern = pattern[:6]
    colors = []
    for _ in range(width * height):
      color = common.random_color()
      colors.append(color if color != line_color else 0)

  copies = 10 - cell_size
  size = (cell_size + 1) * copies - 1
  grid, output = common.grid(size, size), common.grid(width, height)
  # Make a loop of the pattern so that it goes back and forth.
  patternloop = [p for p in pattern]
  patternloop.pop()
  patternloop += [p for p in pattern[::-1]]
  patternloop.pop()
  for r in range(size):
    for c in range(size):
      grid[r][c] = patternloop[abs(r - c + offset) % len(patternloop)]
  for r in range(size):
    for c in range(cell_size, size, cell_size + 1):
      grid[r][c] = line_color
  for r in range(cell_size, size, cell_size + 1):
    for c in range(size):
      grid[r][c] = line_color
  for r in range(height):
    for c in range(width):
      output[r][c] = colors[r * width + c]
      row, col = (brow + r) * (cell_size + 1), (bcol + c) * (cell_size + 1)
      common.rect(grid, cell_size, cell_size, row, col, colors[r * width + c])
  if flop: grid, output = common.flop(grid), common.flop(output)
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(cell_size=5, line_color=4, width=2, height=2, brow=2,
               bcol=1, flop=False, offset=0, pattern=[1, 2, 5, 0, 7, 6],
               colors=[1, 8, 0, 3]),
      generate(cell_size=4, line_color=8, width=3, height=3, brow=1,
               bcol=2, flop=True, offset=8, pattern=[0, 1, 4, 9, 6, 5],
               colors=[2, 2, 2, 2, 9, 3, 2, 1, 2]),
  ]
  test = [
      generate(cell_size=6, line_color=9, width=2, height=3, brow=1,
               bcol=0, flop=False, offset=0, pattern=[2, 3, 6, 1, 8, 7],
               colors=[8, 2, 2, 6, 1, 1]),
  ]
  return {"train": train, "test": test}
