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


def generate(tall=None, colors=None, brow=None, bcol=None, wide=3, width=28,
             height=23):
  """Returns input and output grids according to the given parameters.

  Args:
    tall: The height of the box.
    colors: The colors of the box.
    brow: The row of the box.
    bcol: The column of the box.
    wide: The width of the box.
    width: The width of the grid.
    height: The height of the grid.
  """

  if tall is None:
    tall = common.randint(3, 5)
    brow, bcol = common.randint(2, 8), common.randint(2, 8)
    while True:
      rows, cols = common.conway_sprite(wide, tall, common.randint(1, 8))
      if common.diagonally_connected(list(zip(rows, cols))): break
    colors = [0] * (wide * tall)
    for row, col in zip(rows, cols):
      colors[row * wide + col] = 1

  grid, output = common.grids(width, height)
  i = 0
  while True:
    row, col = brow, bcol + (wide + 1) * i
    if col >= width: break
    hue = 6 if i % 3 == 2 else 7
    for j, color in enumerate(colors):
      if not color: continue
      common.draw(output, row + j // 3, col + j % 3, hue)
      if not i: common.draw(grid, row + j // 3, col + j % 3, hue)
    if i % 3 == 2:
      while True:
        if row > height: break
        for j, color in enumerate(colors):
          if color: common.draw(output, row + j // 3, col + j % 3, hue)
        row += tall + 1
    i += 1
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(tall=3, colors=[1, 1, 1, 1, 0, 1, 1, 1, 1], brow=5, bcol=3),
      generate(tall=5, colors=[1, 0, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 0, 1],
               brow=4, bcol=5),
  ]
  test = [
      generate(tall=5, colors=[0, 1, 0, 0, 1, 0, 1, 0, 1, 0, 1, 0, 0, 1, 0],
               brow=7, bcol=2),
  ]
  return {"train": train, "test": test}
