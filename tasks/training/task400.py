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


def generate(colors=None, brow=None, bcol=None, size=24, cutout=5):
  """Returns input and output grids according to the given parameters.

  Args:
    colors: a list of digits representing the colors to be used
    brow: a list of vertical coordinates where the cutout should be placed
    bcol: a list of horizontal coordinates where the cutout should be placed
    size: the width and height of the (square) grid
    cutout: the width and height of the cutout
  """

  def draw(grid, output):
    for r in range(cutout):
      for c in range(cutout):
        grid[brow + r][bcol + c] = common.blue()
    idx = 0
    for r in range(size // 2):
      for c in range(r, size // 2):
        cells = [(r, c), (c, r), (r, size - 1 - c), (size - 1 - c, r),
                 (size - 1 - r, c), (c, size - 1 - r),
                 (size - 1 - r, size - 1 - c), (size - 1 - c, size - 1 - r)]
        shown = False
        for row, col in cells:
          if grid[row][col] != common.blue(): shown = True
        if not shown: return False
        for row, col in cells:
          grid[row][col] = colors[idx]
        idx += 1
    for r in range(cutout):
      for c in range(cutout):
        output[r][c] = grid[brow + r][bcol + c]
        grid[brow + r][bcol + c] = common.blue()
    return True

  if colors is None:
    color_list, colors = [], []
    for _ in range(3):
      color_list.append(common.random_color(exclude=[common.blue()]))
    for r in range(size // 2):
      for c in range(r, size // 2):
        if common.randint(0, 5) < 2:
          colors.append(common.black())
        elif r < 6 and c < 6:
          colors.append(color_list[0])
        elif r < 6:
          colors.append(color_list[1])
        else:
          colors.append(color_list[2])
    while True:
      brow = common.randint(0, size - cutout)
      bcol = common.randint(0, size - cutout)
      grid, output = common.grid(size, size), common.grid(cutout, cutout)
      if draw(grid, output): break

  grid, output = common.grid(size, size), common.grid(cutout, cutout)
  draw(grid, output)
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(colors=[0, 3, 3, 3, 3, 0, 0, 2, 2, 2, 0, 0, 3, 3, 3, 3, 0, 2, 2,
                       0, 2, 2, 0, 3, 0, 0, 3, 2, 0, 0, 2, 0, 0, 3, 3, 3, 2, 2,
                       2, 2, 2, 2, 3, 3, 0, 2, 0, 2, 2, 2, 3, 0, 0, 0, 2, 2, 2,
                       2, 0, 0, 2, 2, 2, 2, 2, 0, 2, 2, 2, 0, 0, 2, 2, 2, 2, 0,
                       2, 0],
               brow=0, bcol=18),
      generate(colors=[0, 3, 3, 3, 0, 3, 0, 8, 8, 0, 8, 8, 0, 3, 0, 3, 0, 8, 0,
                       8, 0, 0, 0, 3, 3, 3, 3, 8, 8, 8, 0, 8, 8, 0, 3, 3, 0, 0,
                       0, 8, 0, 8, 0, 0, 8, 0, 8, 0, 0, 8, 3, 8, 0, 8, 8, 8, 0,
                       6, 6, 6, 6, 6, 6, 6, 0, 6, 6, 6, 0, 6, 0, 6, 6, 6, 6, 6,
                       6, 0],
               brow=11, bcol=6),
      generate(colors=[0, 3, 3, 3, 3, 0, 5, 5, 5, 0, 0, 5, 3, 3, 3, 3, 3, 5, 5,
                       0, 0, 0, 0, 3, 0, 0, 0, 5, 0, 0, 5, 5, 0, 0, 3, 3, 0, 0,
                       5, 0, 5, 5, 3, 0, 0, 0, 5, 5, 0, 0, 3, 5, 0, 0, 5, 0, 0,
                       0, 5, 0, 0, 5, 5, 5, 5, 0, 0, 5, 5, 5, 0, 5, 5, 5, 5, 0,
                       5, 0],
               brow=15, bcol=10),
  ]
  test = [
      generate(colors=[4, 4, 4, 0, 4, 0, 0, 3, 3, 3, 0, 0, 4, 4, 4, 0, 4, 3, 3,
                       3, 3, 0, 3, 0, 4, 0, 0, 3, 3, 0, 0, 3, 3, 0, 4, 4, 3, 3,
                       0, 0, 3, 3, 4, 4, 0, 0, 3, 3, 0, 3, 0, 0, 3, 3, 3, 3, 3,
                       8, 8, 8, 8, 8, 8, 8, 8, 0, 0, 8, 8, 0, 8, 0, 8, 8, 8, 0,
                       8, 8],
               brow=6, bcol=9),
  ]
  return {"train": train, "test": test}
