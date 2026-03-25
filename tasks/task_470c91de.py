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


def generate(size=None, wides=None, talls=None, brows=None, bcols=None,
             colors=None, angles=None):
  """Returns input and output grids according to the given parameters.

  Args:
    size: The size of the grid.
    wides: The widths of the boxes.
    talls: The heights of the boxes.
    brows: The rows of the boxes.
    bcols: The columns of the boxes.
    colors: The colors of the boxes.
    angles: The angles of the boxes.
  """

  def draw():
    grid, output = common.grids(size, size, 7)
    for wide, tall, brow, bcol, color, angle in zip(wides, talls, brows, bcols,
                                                     colors, angles):
      for r in range(tall):
        for c in range(wide):
          row, col = brow + r, bcol + c
          if grid[row][col] != 7: return None, None
          grid[row][col] = color
          if angle == 0: row, col = row - 1, col - 1
          if angle == 1: row, col = row - 1, col + 1
          if angle == 2: row, col = row + 1, col - 1
          if angle == 3: row, col = row + 1, col + 1
          if row < 0 or row >= size or col < 0 or col >= size: return None, None
          if output[row][col] != 7: return None, None
          output[row][col] = color
      row, col = brow, bcol
      if angle == 1: col = bcol + wide - 1
      if angle == 2: row = brow + tall - 1
      if angle == 3: row, col = brow + tall - 1, bcol + wide - 1
      grid[row][col] = 8
    return grid, output

  if size is None:
    size = common.randint(10, 11)
    num_boxes = common.randint(2, 4)
    while True:
      wides = [common.randint(2, 5) for _ in range(num_boxes)]
      talls = [common.randint(2, 5) for _ in range(num_boxes)]
      brows = [common.randint(0, size - t) for t in talls]
      bcols = [common.randint(0, size - w) for w in wides]
      colors = common.random_colors(num_boxes, exclude=[7, 8])
      angles = [common.randint(0, 3) for _ in range(num_boxes)]
      grid, _ = draw()
      if grid: break

  grid, output = draw()
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(size=10, wides=[2, 3, 5], talls=[2, 4, 4], brows=[0, 1, 6],
               bcols=[0, 5, 1], colors=[9, 1, 5], angles=[3, 0, 1]),
      generate(size=10, wides=[5, 4], talls=[5, 2], brows=[1, 7], bcols=[1, 5],
               colors=[2, 6], angles=[1, 0]),
      generate(size=11, wides=[3, 4, 3], talls=[4, 4, 3], brows=[2, 3, 6],
               bcols=[7, 0, 8], colors=[9, 2, 3], angles=[3, 3, 2]),
  ]
  test = [
      generate(size=11, wides=[3, 3, 2, 2], talls=[5, 3, 4, 2],
               brows=[0, 0, 3, 6], bcols=[0, 8, 4, 6], colors=[9, 3, 4, 2],
               angles=[3, 2, 1, 3]),
  ]
  return {"train": train, "test": test}
