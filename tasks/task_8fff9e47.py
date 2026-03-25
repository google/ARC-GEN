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
    width: The width of the input grid.
    height: The height of the input grid.
    colors: A list of colors to use.
  """

  if width is None:
    width, height = 2 * common.randint(2, 3), 2 * common.randint(2, 3)
    colors = common.choices(list(range(10)), width * height)
    colors = "".join(str(c) for c in colors)

  size = width * height // 2
  grid, output = common.grid(width, height), common.grid(size, size)
  # First, set the middle colors.
  for row in range(height):
    for col in range(width):
      color = int(colors[row * width + col])
      grid[row][col] = color
      if row % 2 == 0:
        r = size // 2 - 1 - row * width // 4 - col // 2
      else:
        r = size // 2 - 1 + row * width // 4 + col // 2
      c = size // 2 - 1 + col % 2
      output[r][c] = color
  # Second, set all the remaining colors.
  for row in range(size):
    for col in range(size):
      if row < size // 2 and col < size // 2:
        r, c = min(row, col), size // 2 - 1
      elif row < size // 2 and col >= size // 2:
        r, c = min(row, size - 1 - col), size // 2
      elif row >= size // 2 and col < size // 2:
        r, c = size - 1 - min(size - 1 - row, col), size // 2 - 1
      else:
        r, c = size - 1 - min(size - 1 - row, size - 1 - col), size // 2
      output[row][col] = output[r][c]
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(width=4, height=6, colors="139455289831401423653980"),
      generate(width=6, height=4, colors="911779207703287721539778"),
  ]
  test = [
      generate(width=4, height=4, colors="6975588701268743"),
  ]
  return {"train": train, "test": test}
