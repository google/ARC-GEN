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


def generate(width=None, height=None, colors=None):
  """Returns input and output grids according to the given parameters.

  Args:
    width: The width of the grid.
    height: The height of the grid.
    colors: The colors of the pixels.
  """

  if width is None:
    while True:
      width, height = common.randint(3, 4), common.randint(3, 4)
      if width * height <= 12: break
    while True:
      colors = common.choices([0, 1, 4, 8], k=width * height)
      if len(set(colors)) >= 3: break

  grid, output = common.grids(width * 5 + 1, height * 5 + 1)
  def put(coords, color):
    for coord in coords:
      r, c = coord
      output[r][c] = grid[r][c] = color
  for i, color in enumerate(colors):
    row, col = i // width, i % width
    grid[row * 5][col * 5] = color
    common.rect(output, 4, 4, 5 * row + 1, 5 * col + 1, color)
  for i in range(height):
    for j in range(width):
      put([(i * 5 + 1, j * 5 + 1),
           (i * 5 + 1, j * 5 + 4),
           (i * 5 + 4, j * 5 + 1),
           (i * 5 + 4, j * 5 + 4)], 8)
      for k in range(4):
        put([(i * 5, j * 5 + 1 + k),
             (i * 5 + 1 + k, j * 5),
             (i * 5 + 5, j * 5 + 1 + k),
             (i * 5 + 1 + k, j * 5 + 5)], 8)
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(width=4, height=3, colors=[0, 0, 0, 0, 0, 0, 8, 0, 4, 0, 0, 0]),
      generate(width=3, height=3, colors=[7, 0, 0, 0, 0, 1, 0, 4, 0]),
  ]
  test = [
      generate(width=3, height=4, colors=[8, 8, 8, 8, 1, 8, 8, 8, 8, 0, 0, 0]),
      generate(width=3, height=3, colors=[1, 1, 1, 1, 0, 4, 4, 4, 4]),
  ]
  return {"train": train, "test": test}
