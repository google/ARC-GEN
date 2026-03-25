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


def generate(size=None, line=None, xpose=None, colors=None):
  """Returns input and output grids according to the given parameters.

  Args:
    size: The size of the grid.
    line: The row of the line to draw.
    xpose: Whether to transpose the grid.
    colors: The colors of the pixels.
  """

  if size is None:
    size, xpose = common.randint(3, 4), common.randint(0, 1)
    rows, cols = common.conway_sprite(size, size)
    colors = [0] * (size * size)
    for row, col in zip(rows, cols):
      colors[row * size + col] = 1
    line = common.randint(0, size - 1)

  grid, output = common.grids(size * (size + 1) - 1, size * (size + 1) - 1)
  for i, i_color in enumerate(colors):
    if not i_color: continue
    for j, j_color in enumerate(colors):
      if not j_color: continue
      color = 2 if i != j else 8
      grid[(i // size) * (size + 1) + j // size][(i % size) * (size + 1) + j % size] = 2
      output[(i // size) * (size + 1) + j // size][(i % size) * (size + 1) + j % size] = color
  for col in range(size * (size + 1) - 1):
    for row in range(line * (size + 1), line * (size + 1) + size):
      grid[row][col] = 3
  if xpose: grid, output = common.transpose(grid), common.transpose(output)
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(size=3, line=2, xpose=True, colors=[1, 1, 0, 1, 0, 1, 0, 1, 0]),
      generate(size=4, line=1, xpose=False,
               colors=[0, 1, 1, 1, 0, 1, 0, 0, 1, 1, 1, 0, 1, 1, 0, 0]),
      generate(size=3, line=2, xpose=True, colors=[1, 0, 1, 0, 1, 1, 1, 0, 0]),
  ]
  test = [
      generate(size=4, line=2, xpose=False,
               colors=[1, 1, 1, 1, 1, 0, 0, 0, 1, 0, 0, 1, 1, 0, 1, 1]),
  ]
  return {"train": train, "test": test}
