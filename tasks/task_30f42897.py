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


def generate(width=None, height=None, length=None, offset=None, color=None):
  """Returns input and output grids according to the given parameters.

  Args:
    width: The width of the grid.
    height: The height of the grid.
    length: The length of the line.
    offset: The offset of the line.
    color: The color of the line.
  """

  if width is None:
    length, color = common.randint(2, 5), common.random_color(exclude=[8])
    while True:
      width, height = common.randint(8, 16), common.randint(3, 8)
      perim = (2 * width + 2 * height - 4)
      if perim % (2 * length) == 0: break
    offset = common.randint(0, perim - 1)

  grid, output = common.grids(width, height, 8)
  row, col, rdir, cdir = 0, 0, 0, 1
  for _ in range(offset):
    row, col = row + rdir, col + cdir
    if cdir == 1 and col + 1 == width: cdir, rdir = 0, 1
    if rdir == 1 and row + 1 == height: cdir, rdir = -1, 0
    if cdir == -1 and col == 0: cdir, rdir = 0, -1
    if rdir == -1 and row == 0: cdir, rdir = 1, 0
  copies = (2 * width + 2 * height - 4) // length // 2
  for i in range(copies):
    for j in [1, 0]:
      for _ in range(length):
        if j and not i: grid[row][col] = color
        if j: output[row][col] = color
        row, col = row + rdir, col + cdir
        if cdir == 1 and col + 1 == width: cdir, rdir = 0, 1
        if rdir == 1 and row + 1 == height: cdir, rdir = -1, 0
        if cdir == -1 and col == 0: cdir, rdir = 0, -1
        if rdir == -1 and row == 0: cdir, rdir = 1, 0
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(width=10, height=7, length=5, offset=10, color=2),
      generate(width=10, height=4, length=4, offset=23, color=9),
      generate(width=9, height=7, length=2, offset=25, color=4),
  ]
  test = [
      generate(width=14, height=3, length=3, offset=18, color=5),
  ]
  return {"train": train, "test": test}
