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
    size: The size of the grid.
    rows: The rows of the boxes.
    cols: The columns of the boxes.
    thicks: The thicknesses of the boxes.
  """

  if width is None:
    width, height = common.randint(1, 3), common.randint(1, 3)
    colors = []
    for _ in range(width * height):
      while True:
        subset = [common.randint(0, 1) for _ in range(9)]
        if sum(subset) > 1 and sum(subset) < 8: break
      colors.extend(subset)
    colors = "".join(str(color) for color in colors)

  grid, output = common.grids(4 * width + 1, 4 * height + 1)
  for row in range(height):
    for col in range(width):
      for r in range(3):
        for c in range(3):
          color = int(colors[row * 9 * width + col * 9 + r * 3 + c])
          grid[row * 4 + r + 1][col * 4 + c + 1] = 8 if color else 0
          output[row * 4 + r + 1][col * 4 + c + 1] = 0 if color else 2
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(width=3, height=2, colors="101010101101111101100110011111101010111000111110001110"),
      generate(width=3, height=1, colors="101101111100010111110010011"),
      generate(width=2, height=2, colors="111000010101011101110011100100111010"),
  ]
  test = [
      generate(width=3, height=3, colors="100101111101111100010011101101111011100010101111101010111110010101110011001111100"),
  ]
  return {"train": train, "test": test}
