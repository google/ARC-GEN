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


def generate(size=None, brow=None, bcol=None, values=None, bgcolor=None,
             fgcolor=None):
  """Returns input and output grids according to the given parameters.

  Args:
    size: The size of the grids.
    brow: The row of the shown sprite.
    bcol: The column of the shown
    values: The values of the sprite.
    bgcolor: The background color.
    fgcolor: The foreground color.
  """

  if size is None:
    size = 2 * common.randint(10, 14) + 1
    brow = common.randint(0, (size - 3) // 4)
    bcol = common.randint(0, (size - 3) // 4)
    pixels = common.diagonally_connected_sprite()
    values = []
    for row in range(3):
      for col in range(3):
        values.append(1 if (row, col) in pixels else 0)
    values = "".join(str(v) for v in values)
    colors = common.sample([1, 2, 3, 4, 8], 2)
    bgcolor, fgcolor = colors[0], colors[1]

  grid, output = common.grids(size, size)
  for i in range(size):
    for j in range(3, size, 4):
      output[i][j] = output[j][i] = grid[i][j] = grid[j][i] = bgcolor
  for row in range(size // 4 + 1):
    for col in range(size // 4 + 1):
      for r in range(3):
        for c in range(3):
          color = fgcolor * int(values[r * 3 + c])
          if row % 2 != brow % 2 or col % 2 != bcol % 2: continue
          common.draw(output, row * 4 + r, col * 4 + c, color)
          if row != brow or col != bcol: continue
          grid[row * 4 + r][col * 4 + c] = color
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(size=23, brow=2, bcol=1, values="010101010", bgcolor=2, fgcolor=4),
      generate(size=27, brow=1, bcol=1, values="110111010", bgcolor=1, fgcolor=3),
      generate(size=25, brow=0, bcol=5, values="110010011", bgcolor=8, fgcolor=2),
  ]
  test = [
      generate(size=29, brow=1, bcol=4, values="010110001", bgcolor=3, fgcolor=8),
  ]
  return {"train": train, "test": test}
