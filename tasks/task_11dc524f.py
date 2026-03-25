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


def generate(wide=None, tall=None, brow=None, bcol=None, angle=None,
             colors=None):
  """Returns input and output grids according to the given parameters.

  Args:
    wide: The width of the box.
    tall: The height of the box.
    brow: The row of the box.
    bcol: The column of the box.
    angle: The angle of the box.
    colors: The colors of the box.
  """

  if wide is None:
    wide, tall = common.randint(2, 3), common.randint(2, 3)
    angle = common.randint(0, 3)
    pixels = common.diagonally_connected_sprite(wide, tall, common.randint(1, 4))
    colors = []
    for r in range(tall):
      for c in range(wide):
        colors.append(1 if (r, c) in pixels else 0)
    brow, bcol = common.randint(8 - tall, 6), common.randint(6 - wide, 4)
    if angle == 0: brow = common.randint(10, 13 - tall)
    if angle == 1: bcol = common.randint(0, 3 - wide)
    if angle == 2: brow = common.randint(0, 4 - tall)
    if angle == 3: bcol = common.randint(8, 13 - wide)

  grid, output = common.grids(13, 13, 7)
  common.rect(grid, 2, 2, 6, 4, 5)
  for r in range(tall):
    for c in range(wide):
      if not colors[r * wide + c]: continue
      grid[brow + r][bcol + c] = 2
  if angle == 0: brow = 8
  if angle == 1: bcol = 4 - wide
  if angle == 2: brow = 6 - tall
  if angle == 3: bcol = 6
  for r in range(tall):
    for c in range(wide):
      if not colors[r * wide + c]: continue
      output[brow + r][bcol + c] = 2
      row, col = brow + r, bcol + c
      if angle == 0: row = 7 - r
      if angle == 1: col = 3 + wide - c
      if angle == 2: row = 5 + tall - r
      if angle == 3: col = 5 - c
      output[row][col] = 5
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(wide=2, tall=3, brow=5, bcol=0, angle=1,
               colors=[1, 0, 0, 1, 1, 1]),
      generate(wide=2, tall=3, brow=1, bcol=4, angle=2,
               colors=[1, 0, 1, 0, 1, 1]),
      generate(wide=3, tall=3, brow=10, bcol=3, angle=0,
               colors=[0, 1, 1, 0, 1, 0, 1, 0, 0]),
  ]
  test = [
      generate(wide=2, tall=3, brow=5, bcol=9, angle=3,
               colors=[0, 1, 1, 1, 1, 0]),
  ]
  return {"train": train, "test": test}
