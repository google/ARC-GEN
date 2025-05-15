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


def generate(colors=None, size=20, minisize=3):
  """Returns input and output grids according to the given parameters.

  Args:
    colors: a list of digits representing the colors to be used
    size: the width and height of the (square) grid
    minisize: the width and height of the small cutouts
  """

  def draw(grid, output):
    for r in range(size):
      for c in range(size):
        output[r][c] = grid[r][c] = colors[r * size + c]
    legal = True
    for r in range(1, size - 1):
      for c in range(1, size - 1):
        grid_total, output_total = 0, 0
        for dr in [-1, 0, 1]:
          for dc in [-1, 0, 1]:
            grid_total += grid[r + dr][c + dc]
            output_total += output[r + dr][c + dc]
        if (grid_total > 0) != (output_total > 0): legal = False
        if output_total: continue
        for dr in [-1, 0, 1]:
          for dc in [-1, 0, 1]:
            output[r + dr][c + dc] = common.blue()
    return legal

  if colors is None:
    color = common.random_color(exclude=[common.blue()])
    while True:  # Keep repeating until the grid is unambiguous.
      # First, create some dense static.
      bitmap = common.grid(size, size)
      for pixel in common.random_pixels(size, size, 0.8):
        bitmap[pixel[0]][pixel[1]] = color
      # Second, create a few holes.
      for _ in range(common.randint(1, 3)):
        row = common.randint(0, size - minisize)
        col = common.randint(0, size - minisize)
        for dr in range(minisize):
          for dc in range(minisize):
            bitmap[row + dr][col + dc] = common.black()
      # Finally, extract the colors.
      colors = []
      for r in range(size):
        for c in range(size):
          colors.append(bitmap[r][c])
      grid, output = common.grids(size, size)
      if draw(grid, output): break

  grid, output = common.grids(size, size)
  draw(grid, output)
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(colors=[5, 0, 0, 5, 0, 0, 5, 5, 5, 5, 5, 5, 0, 0, 5, 5, 5, 5, 0,
                       0, 5, 0, 5, 5, 5, 5, 5, 5, 0, 0, 5, 5, 5, 5, 0, 5, 5, 0,
                       5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 0,
                       0, 5, 5, 0, 5, 5, 5, 5, 5, 0, 0, 0, 5, 0, 5, 5, 0, 5, 5,
                       0, 0, 0, 5, 5, 5, 5, 5, 5, 5, 0, 5, 0, 0, 5, 5, 5, 0, 0,
                       0, 5, 5, 0, 5, 0, 5, 0, 5, 0, 5, 0, 0, 5, 0, 5, 0, 5, 0,
                       5, 0, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 0, 0, 5, 0,
                       5, 5, 5, 0, 0, 0, 5, 0, 0, 0, 5, 5, 5, 0, 0, 0, 5, 5, 5,
                       0, 5, 0, 5, 0, 0, 0, 5, 5, 5, 0, 0, 5, 0, 0, 5, 5, 5, 5,
                       0, 0, 5, 0, 5, 0, 0, 0, 5, 0, 0, 5, 0, 0, 0, 5, 5, 0, 5,
                       5, 5, 5, 0, 5, 5, 5, 0, 5, 5, 5, 5, 5, 0, 5, 5, 5, 5, 5,
                       0, 0, 5, 0, 0, 5, 5, 5, 5, 5, 5, 5, 0, 5, 5, 5, 5, 5, 0,
                       5, 5, 5, 5, 0, 5, 0, 5, 5, 5, 0, 5, 5, 0, 0, 5, 5, 5, 5,
                       0, 0, 5, 5, 5, 0, 5, 5, 5, 5, 5, 5, 5, 5, 5, 0, 5, 5, 5,
                       5, 5, 5, 5, 5, 0, 5, 5, 5, 0, 5, 5, 0, 5, 0, 0, 5, 5, 5,
                       5, 0, 5, 5, 0, 5, 5, 5, 5, 0, 5, 5, 5, 0, 5, 5, 0, 0, 5,
                       0, 5, 0, 0, 0, 5, 5, 5, 0, 5, 0, 5, 5, 0, 5, 0, 0, 5, 0,
                       5, 0, 5, 5, 0, 0, 5, 0, 0, 5, 0, 5, 0, 0, 0, 5, 0, 5, 5,
                       5, 5, 5, 0, 5, 5, 5, 5, 5, 0, 0, 0, 5, 0, 5, 5, 0, 5, 5,
                       5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 0, 0, 5, 5, 0, 5, 5,
                       5, 5, 5, 0, 0, 5, 5, 5, 5, 0, 5, 5, 0, 5, 0, 5, 0, 0, 0,
                       5]),
      generate(colors=[3, 3, 3, 3, 0, 3, 0, 3, 0, 3, 3, 0, 0, 3, 3, 3, 0, 3, 0,
                       0, 0, 0, 3, 3, 0, 0, 3, 0, 3, 3, 0, 3, 0, 3, 3, 0, 0, 3,
                       3, 0, 3, 3, 3, 3, 3, 0, 0, 3, 0, 0, 0, 3, 0, 3, 3, 0, 3,
                       3, 3, 3, 3, 0, 3, 3, 0, 0, 0, 0, 3, 0, 3, 3, 0, 3, 3, 3,
                       0, 3, 3, 0, 0, 0, 0, 3, 0, 3, 0, 3, 3, 3, 0, 3, 3, 3, 0,
                       3, 3, 3, 0, 0, 3, 3, 0, 0, 3, 3, 0, 3, 3, 3, 3, 0, 0, 3,
                       0, 3, 3, 3, 3, 0, 0, 3, 0, 0, 0, 0, 3, 3, 0, 3, 0, 0, 3,
                       0, 0, 0, 3, 0, 3, 0, 3, 0, 3, 0, 0, 0, 0, 0, 0, 3, 3, 3,
                       0, 3, 3, 3, 3, 3, 3, 3, 0, 3, 3, 0, 0, 0, 0, 3, 0, 3, 3,
                       0, 3, 3, 0, 0, 3, 3, 3, 3, 0, 0, 0, 3, 3, 0, 0, 3, 3, 3,
                       3, 3, 0, 3, 0, 3, 0, 3, 3, 3, 3, 0, 3, 3, 0, 3, 3, 3, 0,
                       0, 3, 0, 3, 0, 0, 0, 3, 3, 0, 3, 3, 0, 0, 3, 0, 0, 0, 3,
                       3, 3, 3, 0, 0, 3, 0, 3, 0, 3, 3, 3, 0, 3, 3, 0, 0, 0, 3,
                       3, 0, 3, 3, 3, 3, 0, 0, 3, 0, 0, 3, 3, 0, 0, 3, 0, 3, 3,
                       3, 3, 0, 0, 0, 3, 3, 3, 0, 0, 3, 0, 3, 0, 3, 0, 3, 3, 3,
                       0, 3, 3, 0, 3, 3, 3, 3, 3, 3, 3, 3, 0, 0, 3, 0, 0, 3, 0,
                       3, 3, 0, 0, 3, 0, 3, 0, 3, 3, 0, 3, 3, 3, 0, 0, 3, 3, 0,
                       3, 3, 0, 0, 0, 0, 0, 0, 0, 3, 0, 3, 0, 0, 0, 3, 3, 0, 3,
                       0, 3, 0, 0, 3, 3, 3, 0, 3, 3, 3, 0, 0, 3, 3, 0, 0, 0, 3,
                       0, 0, 3, 0, 3, 3, 0, 3, 0, 0, 3, 0, 0, 3, 3, 3, 3, 3, 3,
                       3, 0, 3, 3, 0, 3, 3, 3, 0, 0, 0, 3, 0, 3, 0, 3, 3, 3, 0,
                       3]),
      generate(colors=[7, 0, 7, 7, 7, 7, 0, 7, 7, 0, 0, 7, 7, 0, 0, 7, 0, 7, 7,
                       7, 0, 0, 7, 0, 7, 0, 7, 0, 7, 7, 7, 0, 0, 0, 0, 7, 7, 0,
                       0, 7, 0, 0, 0, 0, 0, 7, 0, 0, 7, 7, 7, 7, 0, 7, 0, 0, 0,
                       0, 7, 0, 7, 0, 7, 0, 7, 0, 7, 7, 0, 0, 0, 7, 7, 0, 0, 7,
                       7, 0, 7, 0, 0, 0, 7, 0, 0, 7, 0, 0, 7, 0, 7, 7, 7, 7, 0,
                       0, 7, 0, 0, 7, 7, 7, 7, 7, 7, 7, 7, 7, 0, 7, 7, 0, 7, 7,
                       0, 0, 0, 7, 0, 7, 0, 0, 0, 7, 0, 7, 0, 0, 7, 7, 0, 7, 0,
                       7, 0, 0, 0, 0, 7, 7, 0, 7, 7, 7, 7, 0, 7, 0, 7, 0, 0, 7,
                       7, 7, 0, 0, 0, 0, 0, 7, 0, 0, 0, 7, 0, 0, 0, 0, 7, 7, 7,
                       0, 0, 7, 7, 0, 0, 0, 7, 7, 7, 7, 0, 7, 7, 7, 0, 7, 0, 0,
                       7, 0, 7, 7, 0, 7, 7, 0, 7, 0, 7, 0, 0, 0, 0, 0, 0, 0, 0,
                       7, 0, 0, 7, 0, 0, 0, 0, 7, 7, 0, 7, 7, 0, 0, 7, 7, 7, 0,
                       7, 7, 7, 7, 0, 7, 0, 0, 7, 7, 7, 7, 0, 7, 0, 7, 7, 7, 0,
                       0, 0, 7, 7, 0, 7, 7, 0, 7, 0, 0, 7, 7, 0, 0, 7, 7, 0, 7,
                       7, 7, 7, 7, 0, 7, 7, 0, 7, 7, 7, 0, 7, 7, 0, 0, 7, 7, 7,
                       0, 7, 0, 7, 7, 0, 7, 0, 7, 7, 7, 0, 7, 7, 7, 7, 0, 7, 7,
                       7, 0, 7, 0, 7, 7, 7, 7, 7, 0, 0, 7, 7, 7, 0, 0, 7, 7, 7,
                       0, 0, 0, 7, 7, 7, 0, 7, 7, 0, 7, 0, 7, 0, 0, 0, 0, 7, 7,
                       7, 0, 0, 0, 7, 0, 7, 7, 0, 7, 0, 0, 7, 0, 0, 0, 0, 0, 7,
                       0, 0, 0, 0, 0, 7, 7, 0, 7, 0, 0, 0, 7, 0, 7, 7, 7, 0, 7,
                       0, 7, 7, 0, 7, 7, 0, 7, 0, 0, 7, 7, 7, 7, 0, 0, 7, 0, 7,
                       7]),
  ]
  test = [
      generate(colors=[0, 4, 0, 4, 4, 0, 4, 4, 4, 0, 0, 0, 4, 0, 4, 4, 4, 4, 4,
                       0, 0, 0, 4, 4, 0, 0, 4, 0, 4, 4, 0, 0, 0, 0, 4, 4, 4, 4,
                       4, 0, 4, 4, 4, 0, 0, 4, 0, 4, 0, 4, 0, 4, 4, 4, 4, 4, 4,
                       0, 4, 0, 4, 4, 0, 4, 0, 0, 4, 0, 0, 0, 0, 0, 0, 4, 4, 4,
                       0, 4, 0, 0, 4, 0, 0, 4, 4, 0, 4, 4, 4, 4, 4, 4, 4, 0, 4,
                       4, 0, 4, 0, 4, 4, 4, 0, 0, 4, 0, 0, 4, 4, 4, 4, 4, 4, 0,
                       0, 4, 4, 0, 4, 0, 0, 0, 0, 4, 0, 0, 0, 0, 4, 4, 4, 4, 4,
                       0, 4, 0, 4, 4, 0, 4, 4, 0, 4, 4, 0, 0, 0, 4, 4, 0, 0, 0,
                       0, 4, 4, 0, 0, 0, 0, 0, 0, 4, 4, 4, 0, 0, 0, 4, 4, 4, 0,
                       0, 4, 0, 4, 4, 4, 0, 0, 0, 4, 0, 0, 0, 4, 4, 0, 0, 4, 0,
                       0, 4, 0, 4, 4, 4, 0, 4, 0, 4, 0, 0, 0, 4, 0, 4, 0, 4, 4,
                       4, 0, 0, 4, 0, 4, 4, 4, 0, 4, 4, 0, 4, 4, 0, 0, 4, 4, 4,
                       4, 0, 0, 0, 4, 4, 4, 4, 4, 0, 4, 0, 0, 0, 4, 0, 0, 4, 0,
                       0, 4, 0, 0, 4, 0, 4, 4, 0, 0, 0, 4, 4, 4, 0, 4, 4, 0, 4,
                       0, 0, 4, 4, 4, 0, 0, 0, 0, 4, 4, 4, 0, 0, 0, 4, 4, 4, 4,
                       0, 0, 4, 0, 4, 0, 0, 4, 4, 0, 4, 4, 4, 4, 4, 4, 0, 0, 4,
                       4, 0, 4, 0, 4, 0, 0, 4, 0, 4, 0, 4, 0, 4, 0, 0, 4, 4, 0,
                       4, 0, 4, 0, 4, 4, 0, 0, 4, 4, 4, 0, 0, 0, 0, 4, 4, 4, 0,
                       0, 0, 0, 4, 4, 0, 4, 4, 0, 4, 0, 4, 0, 0, 0, 4, 4, 4, 0,
                       0, 0, 0, 0, 4, 4, 4, 4, 0, 4, 0, 0, 4, 0, 0, 0, 0, 0, 0,
                       4, 4, 0, 0, 0, 0, 0, 4, 4, 0, 0, 0, 4, 0, 4, 0, 4, 0, 4,
                       4]),
  ]
  return {"train": train, "test": test}
