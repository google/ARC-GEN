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


def generate(width=None, height=None, wides=None, talls=None, brows=None,
             bcols=None, colors=None):
  """Returns input and output grids according to the given parameters.

  Args:
    width: the width of the grid.
    height: the height of the grid.
    wides: the widths of the boxes.
    talls: the heights of the boxes.
    brows: the rows of the boxes.
    bcols: the columns of the boxes.
    colors: the colors of the pixels.
  """

  def draw():
    grid, output = common.grids(width, height)
    # First, fill the grids with colors.
    for i, color in enumerate(colors):
      r, c = i // width, i % width
      output[r][c] = grid[r][c] = color
    # Second, orange out the appropriate sections of the output.
    for wide, tall, brow, bcol in zip(wides, talls, brows, bcols):
      if brow in [0, height - tall]: common.rect(output, wide, height, 0, bcol, 7)
      if bcol in [0, width - wide]: common.rect(output, width, tall, brow, 0, 7)
    # Finally, draw the boxes.
    for wide, tall, brow, bcol in zip(wides, talls, brows, bcols):
      row, col = brow, bcol
      if row == 0: row = height - tall
      elif row == height - tall: row = 0
      elif col == 0: col = width - wide
      elif col == width - wide: col = 0
      for r in range(tall):
        for c in range(wide):
          # We want to avoid cases where the boxes overlap (ill-defined).
          if grid[brow + r][bcol + c] == 0: return None, None
          if output[row + r][col + c] == 0: return None, None
          grid[brow + r][bcol + c] = 0
          output[row + r][col + c] = 0
    return grid, output

  if width is None:
    width, height = 2 * common.randint(3, 10), 2 * common.randint(3, 10)
    boxes = (width + height - 6) // 6
    colors = [2 * common.randint(0, 1) + 5 for _ in range(width * height)]
    while True:
      wides = [common.randint(1, width // 3) for _ in range(boxes)]
      talls = [common.randint(1, height // 3) for _ in range(boxes)]
      brows, bcols = [], []
      for wide, tall in zip(wides, talls):
        if common.randint(0, 1):
          brows.append(0 if common.randint(0, 1) else height - tall)
          bcols.append(common.randint(1, width - wide - 1))
        else:
          brows.append(common.randint(1, height - tall - 1))
          bcols.append(0 if common.randint(0, 1) else width - wide)
      if common.overlaps(brows, bcols, wides, talls, 1): continue
      grid, _ = draw()
      if not grid: continue
      # Now, check that no boxes occur across from each other (ill-defined).
      good = True
      for r in range(height):
        if grid[r][0] == 0 and grid[r][width - 1] == 0: good = False
      for c in range(width):
        if grid[0][c] == 0 and grid[height - 1][c] == 0: good = False
      if good: break

  grid, output = draw()
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(width=10, height=10, wides=[3, 2, 2], talls=[3, 3, 2],
               brows=[1, 7, 8], bcols=[0, 1, 5],
               colors=[7, 5, 7, 7, 5, 5, 7, 7, 5, 7,
                       1, 1, 1, 7, 7, 5, 5, 7, 7, 5,
                       1, 1, 1, 7, 5, 5, 7, 5, 7, 7,
                       1, 1, 1, 5, 7, 5, 7, 5, 7, 7,
                       7, 7, 5, 5, 5, 5, 7, 5, 5, 5,
                       7, 5, 7, 5, 7, 7, 5, 5, 7, 5,
                       7, 5, 7, 7, 5, 5, 5, 7, 7, 7,
                       7, 1, 1, 5, 5, 5, 7, 5, 7, 5,
                       5, 1, 1, 7, 5, 1, 1, 7, 5, 7,
                       7, 1, 1, 5, 5, 1, 1, 5, 7, 7]),
      generate(width=8, height=6, wides=[3], talls=[3], brows=[2], bcols=[5],
               colors=[7, 7, 5, 7, 5, 7, 5, 7,
                       7, 5, 7, 7, 5, 7, 7, 7,
                       7, 7, 5, 7, 7, 1, 1, 1,
                       5, 7, 7, 5, 7, 1, 1, 1,
                       7, 7, 7, 7, 7, 1, 1, 1,
                       5, 7, 5, 7, 5, 5, 7, 7]),
      generate(width=12, height=12, wides=[4, 4, 1], talls=[3, 2, 2],
               brows=[0, 6, 10], bcols=[4, 8, 2],
               colors=[5, 5, 5, 7, 1, 1, 1, 1, 5, 5, 5, 7,
                       5, 7, 5, 5, 1, 1, 1, 1, 7, 5, 5, 5,
                       5, 7, 7, 7, 1, 1, 1, 1, 7, 5, 7, 7,
                       5, 7, 7, 5, 5, 7, 5, 5, 5, 7, 7, 5,
                       7, 7, 5, 7, 5, 5, 7, 5, 5, 7, 7, 5,
                       7, 5, 7, 5, 5, 5, 5, 5, 5, 7, 7, 5,
                       7, 5, 7, 7, 5, 5, 5, 5, 1, 1, 1, 1,
                       7, 7, 7, 5, 7, 7, 5, 5, 1, 1, 1, 1,
                       5, 7, 7, 7, 7, 7, 5, 7, 5, 7, 5, 5,
                       7, 5, 5, 5, 7, 5, 5, 7, 5, 5, 7, 5,
                       7, 5, 1, 5, 7, 5, 7, 7, 5, 7, 5, 5,
                       7, 5, 1, 7, 5, 5, 5, 5, 5, 7, 5, 5]),
  ]
  test = [
      generate(width=14, height=18, wides=[1, 3, 6, 3, 3, 2, 1, 4],
               talls=[2, 2, 3, 1, 2, 2, 4, 3],
               brows=[0, 2, 6, 9, 10, 13, 14, 15],
               bcols=[8, 11, 0, 11, 0, 12, 9, 3],
               colors=[7, 7, 7, 7, 7, 7, 7, 7, 1, 7, 7, 5, 7, 7,
                       5, 5, 7, 7, 7, 5, 5, 7, 1, 7, 7, 7, 7, 7,
                       7, 7, 5, 7, 7, 5, 7, 7, 7, 7, 7, 1, 1, 1,
                       7, 7, 5, 7, 7, 5, 5, 5, 5, 7, 7, 1, 1, 1,
                       7, 7, 7, 5, 7, 5, 7, 7, 7, 5, 7, 7, 7, 5,
                       7, 5, 7, 7, 5, 7, 7, 7, 7, 5, 5, 7, 7, 5,
                       1, 1, 1, 1, 1, 1, 7, 7, 7, 7, 7, 5, 7, 7,
                       1, 1, 1, 1, 1, 1, 7, 5, 5, 7, 7, 7, 7, 7,
                       1, 1, 1, 1, 1, 1, 7, 7, 5, 7, 7, 7, 7, 7,
                       5, 7, 5, 7, 7, 5, 7, 7, 7, 5, 5, 1, 1, 1,
                       1, 1, 1, 7, 7, 7, 7, 7, 5, 5, 5, 5, 7, 5,
                       1, 1, 1, 7, 5, 7, 5, 7, 7, 7, 7, 5, 7, 7,
                       5, 7, 5, 7, 7, 7, 7, 7, 5, 7, 7, 7, 7, 7,
                       7, 7, 7, 7, 7, 5, 5, 7, 5, 7, 7, 7, 1, 1,
                       7, 5, 7, 5, 7, 7, 7, 5, 5, 1, 7, 5, 1, 1,
                       5, 7, 7, 1, 1, 1, 1, 7, 7, 1, 7, 7, 7, 7,
                       7, 7, 7, 1, 1, 1, 1, 7, 7, 1, 7, 7, 7, 5,
                       7, 7, 7, 1, 1, 1, 1, 5, 5, 1, 7, 5, 7, 7]),
  ]
  return {"train": train, "test": test}
