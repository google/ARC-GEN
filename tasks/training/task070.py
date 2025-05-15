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


def generate(colors=None, width=None, height=None, row=None, col=None,
             wide=None, tall=None, size=17):
  """Returns input and output grids according to the given parameters.

  Args:
    colors: a list of colors to be used for pixels
    width: the width of the input grid
    height: the height of the input grid
    row: the row of the sky blue rectangle
    col: the column of the sky blue rectangle
    wide: the width of the sky blue rectangle
    tall: the height of the sky blue rectangle
    size: the width and height of the (square) grid
  """

  def draw(grid, output):
    for r in range(size):
      for c in range(size):
        output[r][c] = grid[r][c] = colors[(r % height) * width + c % width]
    for r in range(tall):
      for c in range(wide):
        if grid[row + r][col + c] != common.blue():
          grid[row + r][col + c] = common.cyan()
        if output[row + r][col + c] == common.blue():
          output[row + r][col + c] = common.green()
        else:
          output[row + r][col + c] = common.cyan()
    # Check that each row / column of the rectangle is visible.
    for r in range(tall):
      visible = False
      for c in range(wide):
        if grid[row + r][col + c] == common.cyan(): visible = True
      if not visible: return False
    for c in range(wide):
      visible = False
      for r in range(tall):
        if grid[row + r][col + c] == common.cyan(): visible = True
      if not visible: return False
    return True

  if colors is None:
    if common.randint(0, 3) == 0:  # totally randomize the whole grid
      width, height = size, size
    else:
      width, height = common.randint(2, 4), common.randint(2, 4)
    while True:
      pixels, area = common.all_pixels(width, height), width * height
      pixels = common.sample(pixels, common.randint(area // 4, area // 2))
      grid, colors = common.grid(width, height), []
      for (r, c) in pixels:
        grid[r][c] = common.blue()
      for r in range(height):
        for c in range(width):
          colors.append(grid[r][c])
      wide, tall = common.randint(2, 10), common.randint(2, 10)
      row, col = common.randint(0, size - tall), common.randint(0, size - wide)
      grid, output = common.grids(size, size)
      if draw(grid, output): break

  grid, output = common.grids(size, size)
  draw(grid, output)
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(colors=[0, 0, 0, 0, 1, 1, 0, 1, 0, 0, 0, 0, 1, 1, 1, 0],
               width=4, height=4, row=2, col=5, wide=5, tall=5),
      generate(colors=[1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 1, 1, 1,
                       0, 1, 0, 1, 0, 1, 1, 1, 1, 1, 0, 0, 1, 1, 0, 0, 0, 0, 1,
                       0, 0, 0, 1, 0, 0, 1, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0,
                       1, 0, 1, 0, 1, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1, 1, 0,
                       0, 0, 0, 0, 1, 1, 0, 1, 1, 0, 0, 0, 0, 0, 1, 1, 1, 0, 1,
                       1, 0, 1, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 1, 0, 0, 0, 0,
                       0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0,
                       1, 1, 0, 0, 0, 1, 0, 1, 1, 1, 0, 0, 0, 1, 1, 0, 0, 0, 0,
                       0, 0, 1, 1, 0, 1, 1, 0, 1, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0,
                       1, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0,
                       0, 0, 0, 1, 0, 1, 0, 1, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 1,
                       0, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 1, 0, 1, 0, 1,
                       0, 1, 0, 1, 0, 1, 0, 1, 0, 0, 0, 0, 1, 1, 0, 1, 1, 1, 1,
                       1, 1, 0, 0, 0, 0, 0, 1, 0, 1, 1, 0, 1, 1, 0, 0, 0, 0, 0,
                       1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0,
                       0, 0, 1, 1],
               width=17, height=17, row=7, col=1, wide=8, tall=3),
      generate(colors=[0, 1, 0, 1, 0, 1], width=3, height=2, row=3, col=4,
               wide=5, tall=5),
  ]
  test = [
      generate(colors=[1, 0, 0, 0, 1, 0, 0, 0, 1], width=3, height=3, row=11,
               col=7, wide=6, tall=4),
  ]
  return {"train": train, "test": test}
