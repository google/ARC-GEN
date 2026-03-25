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


def generate(width=None, height=None, brow=None, bcol=None, wide=None,
             tall=None, hcopies=None, vcopies=None, hoffset=None, voffset=None,
             color=None):
  """Returns input and output grids according to the given parameters.

  Args:
    width: The width of the grid.
    height: The height of the grid.
    brow: The row of the shape.
    bcol: The column of the shape.
    wide: The width of the inner boxes.
    tall: The height of the inner boxes.
    hcopies: The number of horizontal copies.
    vcopies: The number of vertical copies.
    hoffset: The horizontal offset of the copies.
    voffset: The vertical offset of the copies.
    color: The color of the shape.
  """

  if width is None:
    width, height = 14 + common.randint(-1, 1), 14 + common.randint(-1, 1)
    hoffset, voffset = common.randint(0, 1), common.randint(0, 1)
    hcopies, vcopies = common.randint(1, 3), common.randint(1, 3)
    while True:
      wide, tall = common.randint(3, width - 2), common.randint(3, height - 2)
      eff_width = hcopies * (wide + hoffset - 1) + 1
      eff_height = vcopies * (tall + voffset - 1) + 1
      if eff_width <= width - 4 and eff_height <= height - 2: break
    brow = common.randint(1, height - eff_height - 1)
    bcol = common.randint(2, width - eff_width - 2)
    color = common.random_color()

  grid, output = common.grids(width, height)
  for row in range(vcopies):
    for col in range(hcopies):
      r = brow + row * (tall + voffset - 1)
      c = bcol + col * (wide + hoffset - 1)
      common.hollow_rect(grid, wide, tall, r, c, color)
      common.hollow_rect(output, wide, tall, r, c, color)
  scanline = None
  for row in range(height - 1, -1, -1):
    if scanline is None and sum(output[row]) == 0: continue
    if scanline is None: scanline = 0
    if scanline % 4 == 1: output[row] = output[row][1:] + [0]
    if scanline % 4 == 3: output[row] = [0] + output[row][:-1]
    scanline += 1
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(width=15, height=15, brow=2, bcol=4, wide=4, tall=4, hcopies=2,
               vcopies=3, hoffset=1, voffset=0, color=5),
      generate(width=14, height=15, brow=3, bcol=3, wide=6, tall=11, hcopies=1,
               vcopies=1, hoffset=0, voffset=0, color=2),
      generate(width=15, height=15, brow=2, bcol=4, wide=3, tall=12, hcopies=2,
               vcopies=1, hoffset=0, voffset=0, color=8),
      generate(width=14, height=13, brow=4, bcol=3, wide=5, tall=4, hcopies=2,
               vcopies=2, hoffset=0, voffset=0, color=3),
  ]
  test = [
      generate(width=15, height=15, brow=1, bcol=4, wide=4, tall=13, hcopies=2,
               vcopies=1, hoffset=0, voffset=0, color=7),
  ]
  return {"train": train, "test": test}
