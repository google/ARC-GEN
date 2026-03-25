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


def generate(width=None, height=None, brows=None, bcols=None, cdirs=None,
             colors=None, flip=None, xpose=None):
  """Returns input and output grids according to the given parameters.

  Args:
    width: The width of the grid.
    height: The height of the grid.
    brows: The rows of the boxes.
    bcols: The columns of the boxes.
    cdirs: The directions of the boxes.
    colors: The colors of the boxes.
    flip: Whether to flip the grid.
    xpose: Whether to transpose the grid.
  """

  def draw():
    grid, output = common.grids(width, height)
    for c in range(width):
      output[0][c] = grid[0][c] = 2
    for brow, bcol, cdir, color in zip(brows, bcols, cdirs, colors):
      row, col = brow, bcol
      grid[row][col] = color
      grid[(row + 1) if cdir else row][col if cdir else (col + 1)] = color
      while True:
        if cdir == 1 and output[row - 1][col]: break
        if cdir == 0 and output[row - 1][col] + output[row - 1][col + 1]: break
        row -= 1
      output[row][col] = color
      output[(row + 1) if cdir else row][col if cdir else (col + 1)] = color
    return grid, output

  if width is None:
    width, height = common.randint(5, 10), common.randint(10, 11)
    num_boxes = (width * height - 1) // 10 + 1
    cdirs = [common.randint(0, 1) for _ in range(num_boxes)]
    colors = [common.random_color(exclude=[2]) for _ in range(num_boxes)]
    flip, xpose = common.randint(0, 1), common.randint(0, 1)
    while True:
      wides = [2 - cdir for cdir in cdirs]
      talls = [1 + cdir for cdir in cdirs]
      brows = [common.randint(1, height - tall) for tall in talls]
      bcols = [common.randint(0, width - wide) for wide in wides]
      if common.overlaps(brows, bcols, wides, talls): continue
      if common.some_abutted(brows, bcols, wides, talls): continue
      # Corners can touch, but only if colors are distinct.
      grid, _ = draw()
      good = True
      for row in range(1, height - 1):
        for col in range(1, width - 1):
          if grid[row][col] == 0: continue
          for dr, dc in [(-1, -1), (-1, 1), (1, -1), (1, 1)]:
            if grid[row + dr][col + dc] == grid[row][col]: good = False
      if good: break

  grid, output = draw()
  if flip: grid, output = common.flip(grid), common.flip(output)
  if xpose: grid, output = common.transpose(grid), common.transpose(output)
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(width=5, height=11, brows=[2, 3, 5, 7, 7, 8], bcols=[4, 0, 1, 0, 3, 2], cdirs=[1, 1, 0, 1, 0, 1], colors=[7, 3, 5, 4, 8, 6], flip=False, xpose=True),
      generate(width=6, height=10, brows=[3, 5, 5, 7, 7, 9], bcols=[2, 0, 5, 0, 3, 4], cdirs=[0, 0, 1, 1, 1, 0], colors=[5, 1, 6, 3, 4, 8], flip=True, xpose=False),
      generate(width=5, height=10, brows=[2, 4, 5, 7, 8], bcols=[1, 3, 1, 0, 3], cdirs=[0, 1, 1, 1, 0], colors=[6, 8, 5, 4, 9], flip=True, xpose=True),
  ]
  test = [
      generate(width=10, height=10, brows=[1, 1, 2, 3, 4, 5, 6, 6, 8, 8, 9], bcols=[2, 7, 5, 1, 8, 4, 2, 8, 0, 5, 7], cdirs=[0, 1, 1, 0, 0, 0, 1, 1, 1, 0, 0], colors=[3, 6, 7, 8, 6, 3, 9, 4, 3, 1, 5], flip=False, xpose=False),
  ]
  return {"train": train, "test": test}
