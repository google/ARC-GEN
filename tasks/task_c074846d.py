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


def generate(width=None, height=None, length=None, row=None, col=None, cdir=0):
  """Returns input and output grids according to the given parameters.

  Args:
    width: width of the output grid
    height: height of the output grid
    length: length of the line
    row: row of the pixel
    col: col of the pixel
    cdir: direction of the line
  """

  def draw():
    grid, output = common.grids(width, height)
    dr, dc = [-1, 0, 1, 0], [0, 1, 0, -1]
    for i in range(length + 1):
      r, c = row + i * dr[cdir], col + i * dc[cdir]
      if common.get_pixel(grid, r, c) == -1: return None, None
      grid[r][c], output[r][c] = 2, 3
      r, c = row + i * dr[(cdir + 1) % 4], col + i * dc[(cdir + 1) % 4]
      if common.get_pixel(grid, r, c) == -1: return None, None
      output[r][c] = 2
    output[row][col] = grid[row][col] = 5
    return grid, output

  if width is None:
    length, cdir = common.randint(1, 4), common.randint(0, 3)
    while True:
      width, height = common.randint(3, 12), common.randint(3, 12)
      row, col = common.randint(1, height - 2), common.randint(1, width - 2)
      grid, _ = draw()
      if grid: break

  grid, output = draw()
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(width=7, height=6, length=3, row=3, col=4, cdir=3),
      generate(width=3, height=3, length=1, row=1, col=1, cdir=1),
      generate(width=7, height=7, length=2, row=4, col=4, cdir=2),
      generate(width=7, height=7, length=1, row=3, col=3, cdir=0),
      generate(width=7, height=5, length=2, row=2, col=3, cdir=3),
  ]
  test = [
      generate(width=11, height=9, length=4, row=4, col=5, cdir=0),
      generate(width=9, height=9, length=3, row=5, col=3, cdir=2),
  ]
  return {"train": train, "test": test}
