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


def generate(width=None, height=None, length=None, color=None):
  """Returns input and output grids according to the given parameters.

  Args:
    width: The width of the input grid.
    height: The height of the input grid.
    length: The length of the line.
    color: The color of the line.
  """

  def draw():
    grid = common.grid(width, height)
    for c in range(length):
      grid[0][c] = color
    col = 0
    output = [[0] * width]
    def put(color):
      nonlocal output, col
      if col == width: output, col = output + [[0] * width], 0
      output[-1][col] = color
      col += 1
    for i in range(1, length + 1):
      for _ in range(i): put(color)
      put(0)
    for i in range(length - 1, 0, -1):
      for _ in range(i): put(color)
      put(0)
    if col == 1: return None, None  # We finished with a blank line (undefined).
    return grid, output

  if width is None:
    while True:
      length = common.randint(2, 10)
      width = length + common.randint(1, 20)
      height = common.randint(5, 15)
      color = common.random_color()
      grid, _ = draw()
      if grid: break

  grid, output = draw()
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(width=11, height=8, length=6, color=3),
      generate(width=23, height=7, length=4, color=1),
      generate(width=5, height=8, length=3, color=7),
      generate(width=23, height=7, length=3, color=4),
  ]
  test = [
      generate(width=16, height=13, length=8, color=9),
      generate(width=10, height=7, length=7, color=6),
  ]
  return {"train": train, "test": test}
