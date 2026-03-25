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


def generate(size=None, colors=None):
  """Returns input and output grids according to the given parameters.

  Args:
    size: The size of the input grid.
    colors: A list of colors to use.
  """

  if size is None:
    size = common.randint(3, 5)
    hues = common.sample([1, 2, 3], 2)
    colors = [0] * (size * size)
    angle = common.randint(0, 3)
    while 5 not in colors or hues[0] not in colors or hues[1] not in colors:
      r, c = common.randint(0, size - 1), common.randint(0, size - 1)
      color = common.choice(hues + [0, 5])
      colors[r * size + c] = color
      if angle == 0: colors[(size - 1 - r) * size + c] = color
      if angle == 1: colors[r * size + (size - 1 - c)] = color
      if angle == 2: colors[c * size + r] = color
      if angle == 3: colors[(size - 1 - c) * size + (size - 1 - r)] = color

  grid, output = common.grid(size, size), common.grid(size * size, size * size)
  for i, color in enumerate(colors):
    row, col = i // size, i % size
    grid[row][col] = color
    if color != 5: continue
    for j, color_j in enumerate(colors):
      output[row * size + j // size][col * size + j % size] = color_j
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(size=4, colors=[0, 5, 0, 3, 5, 5, 2, 0, 0, 2, 5, 5, 3, 0, 5, 0]),
      generate(size=3, colors=[2, 5, 1, 0, 5, 0, 2, 5, 1]),
      generate(size=4, colors=[5, 5, 5, 5, 5, 2, 3, 5, 5, 3, 3, 5, 5, 5, 5, 5]),
      generate(size=3, colors=[5, 0, 1, 5, 2, 0, 5, 5, 5]),
  ]
  test = [
      generate(size=5,
               colors=[1, 0, 5, 0, 1, 0, 2, 2, 2, 0, 5, 0, 5, 0, 5, 0, 2, 2, 2, 0, 1, 0, 5, 0, 1]),
  ]
  return {"train": train, "test": test}
