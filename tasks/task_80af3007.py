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


def generate(width=None, height=None, rows=None, cols=None, rowoffset=None,
             coloffset=None, size=3):
  """Returns input and output grids according to the given parameters.

  Args:
    width: the width of the input grid
    height: the height of the input grid
    rows: a list of vertical coordinates where pixels should be placed
    cols: a list of horizontal coordinates where pixels should be placed
    rowoffset: the offset of the sprite in the output grid
    coloffset: the offset of the sprite in the output grid
    size: the width and height of the (square) output grid
  """
  if width is None:
    offset = common.randint(-1, 1)
    width, height = 18 + offset, 16 + offset
    rows, cols = common.conway_sprite()
    rowoffset = common.randint(1, height - size * size - 1)
    coloffset = common.randint(1, width - size * size - 1)

  grid = common.grid(width, height)
  output = common.grid(size * size, size * size)
  for row, col in zip(rows, cols):
    for dr in range(size):
      for dc in range(size):
        r, c = rowoffset + row * size + dr, coloffset + col * size + dc
        grid[r][c] = common.gray()
    for r, c in zip(rows, cols):
      output[row * size + r][col * size + c] = common.gray()
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(width=18, height=16, rows=[0, 0, 1, 2, 2], cols=[0, 2, 1, 0, 2],
               rowoffset=1, coloffset=1),
      generate(width=18, height=16, rows=[0, 0, 1, 2, 2], cols=[0, 1, 2, 0, 1],
               rowoffset=1, coloffset=7),
      generate(width=18, height=16, rows=[0, 0, 0, 1, 1, 2, 2],
               cols=[0, 1, 2, 1, 2, 0, 2], rowoffset=4, coloffset=3),
  ]
  test = [
      generate(width=19, height=17, rows=[0, 0, 0, 1, 2, 2],
               cols=[0, 1, 2, 1, 0, 2], rowoffset=3, coloffset=7),
  ]
  return {"train": train, "test": test}
