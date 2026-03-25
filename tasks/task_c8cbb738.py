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


def generate(width=None, height=None, halfsize=None, bgcolor=None, rows=None,
             cols=None, colors=None, brows=None, bcols=None):
  """Returns input and output grids according to the given parameters.

  Args:
    width: the width of the input grid
    height: the height of the input grid
    halfsize: half the size of the target square
    bgcolor: the color of the background
    rows: a list of vertical coordinates of the target square perimeter
    cols: a list of horizontal coordinates of the target square perimeter
    colors: a list of digits representing the colors to be used
    brows: a list of vertical coordinates of the broken border centers
    bcols: a list of horizontal coordinates of the broken border centers
  """

  def draw(grid, output, b):
    illegal = False
    for row, col, color, brow, bcol in zip(rows, cols, colors, brows, bcols):
      pairs = [(row, col), (row, -col), (-row, col), (-row, -col)]
      if not row:  # For row zero, we also replicate elsewhere.
        pairs += [(col, row), (col, -row), (-col, row), (-col, -row)]
      # First, check that we won't clobber over anything already drawn.
      for dr, dc in pairs:
        if grid[brow + dr][bcol + dc] != b: illegal = True
      # Second, draw the pixels.
      for dr, dc in pairs:
        grid[brow + dr][bcol + dc] = color
        output[halfsize + dr][halfsize + dc] = color
    return not illegal

  if width is None:
    halfsize, bgcolor = common.randint(1, 3), common.random_color()
    num_elements = 2 * common.randint(1, 2)
    if halfsize == 1: num_elements = 2
    if halfsize == 3: num_elements = 4
    while True:
      width = 5 * halfsize + 3 + common.randint(-2, 2)
      height = 5 * halfsize + 3 + common.randint(-2, 2)
      elts = []
      for i in range(halfsize):
        elts.append((i, halfsize))
        elts.append((halfsize, i + 1))
      elts = common.sample(elts, num_elements)
      rows, cols = zip(*elts)
      colors = common.random_colors(num_elements, exclude=[bgcolor])
      brows = [common.randint(halfsize, height - halfsize - 1) for _ in elts]
      bcols = [common.randint(halfsize, width - halfsize - 1) for _ in elts]
      grid = common.grid(width, height, bgcolor)
      output = common.grid(2 * halfsize + 1, 2 * halfsize + 1, bgcolor)
      if draw(grid, output, bgcolor): break

  grid = common.grid(width, height, bgcolor)
  output = common.grid(2 * halfsize + 1, 2 * halfsize + 1, bgcolor)
  draw(grid, output, bgcolor)
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(width=11, height=12, halfsize=2, bgcolor=3, rows=[0, 1, 2, 2],
               cols=[2, 2, 2, 1], colors=[1, 8, 2, 4], brows=[4, 9, 8, 2],
               bcols=[4, 2, 8, 8]),
      generate(width=8, height=10, halfsize=1, bgcolor=1, rows=[0, 1],
               cols=[1, 1], colors=[3, 8], brows=[6, 2], bcols=[4, 2]),
      generate(width=14, height=12, halfsize=2, bgcolor=4, rows=[0, 2], 
               cols=[2, 2], colors=[7, 1], brows=[7, 3], bcols=[9, 4]),
  ]
  test = [
      generate(width=19, height=18, halfsize=3, bgcolor=8, rows=[0, 1, 3, 3],
               cols=[3, 3, 3, 1], colors=[1, 2, 3, 6], brows=[5, 7, 12, 13],
               bcols=[6, 14, 6, 15]),
  ]
  return {"train": train, "test": test}
