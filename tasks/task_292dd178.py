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


def generate(width=None, height=None, brows=None, bcols=None, notches=None,
             bgcolor=None):
  """Returns input and output grids according to the given parameters.

  Args:
    width: The width of the grid.
    height: The height of the grid.
    brows: The rows of the boxes.
    bcols: The columns of the boxes.
    notches: The notches of the boxes.
    bgcolor: The background color of the grids.
  """

  def draw():
    grid, output = common.grids(width, height, bgcolor)
    row_map, col_map = [0, 0, 1, 2, 3, 3, 2, 1], [1, 2, 3, 3, 2, 1, 0, 0]
    row_dir, col_dir = [-1, -1, 0, 0, 1, 1, 0, 0], [0, 0, 1, 1, 0, 0, -1, -1]
    for brow, bcol, notch in zip(brows, bcols, notches):
      common.hollow_rect(grid, 4, 4, brow, bcol, 1)
      common.hollow_rect(output, 4, 4, brow, bcol, 1)
      common.rect(output, 2, 2, brow + 1, bcol + 1, 2)
      row, col = brow + row_map[notch], bcol + col_map[notch]
      output[row][col] = grid[row][col] = bgcolor
      while row >= 0 and col >= 0 and row < height and col < width:
        if output[row][col] != bgcolor: return None, None
        output[row][col] = 2
        row, col = row + row_dir[notch], col + col_dir[notch]
    return grid, output

  if width is None:
    width, height = common.randint(6, 15), common.randint(6, 15)
    boxes = 1
    if width * height >= 64: boxes = 2
    if width * height >= 128: boxes = 3
    bgcolor = common.random_color(exclude=[1, 2])
    while True:
      brows = [common.randint(0, height - 4) for _ in range(boxes)]
      bcols = [common.randint(0, width - 4) for _ in range(boxes)]
      if common.overlaps(brows, bcols, [5] * boxes, [5] * boxes): continue
      notches = [common.randint(0, 7) for _ in range(boxes)]
      grid, _ = draw()
      if grid: break

  grid, output = draw()
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(width=9, height=7, brows=[2], bcols=[2], notches=[6], bgcolor=5),
      generate(width=10, height=11, brows=[2, 6], bcols=[1, 6], notches=[1, 4], bgcolor=8),
      generate(width=9, height=11, brows=[0, 6], bcols=[1, 2], notches=[0, 3], bgcolor=9),
  ]
  test = [
      generate(width=15, height=11, brows=[1, 2, 6], bcols=[8, 1, 7], notches=[2, 0, 5], bgcolor=4),
  ]
  return {"train": train, "test": test}
