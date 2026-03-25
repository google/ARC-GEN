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
    size: The size of the grid.
    colors: The colors of the pixels.
  """

  if size is None:
    size = common.randint(3, 5)
    hues = common.random_colors(common.randint(2, 3))
    colors = [0 for _ in range(size * size)]
    # Just draw random lines until there's no 0's and all colors are shown.
    while 0 in colors or len(set(colors)) != len(hues):
      hue = common.choice(hues)
      length = common.randint(1, size)
      start = common.randint(0, size - length)
      offset = common.randint(0, size - 1)
      if common.randint(0, 1):
        for r in range(start, start + length):
          colors[r * size + offset] = hue
      else:
        for c in range(start, start + length):
          colors[offset * size + c] = hue

  grid, output = common.grid(size, size), common.grid(size * size, size * size)
  for i, color in enumerate(colors):
    grid[i // size][i % size] = color
  for i, color in enumerate(colors):
    for r in range(size):
      for c in range(size):
        if grid[r][c] != color: continue
        output[r * size + i // size][c * size + i % size] = color
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(size=3, colors=[6, 6, 6, 6, 8, 8, 8, 8, 6]),
      generate(size=3, colors=[2, 4, 4, 3, 2, 4, 3, 3, 2]),
      generate(size=5, colors=[1, 1, 1, 1, 1, 1, 8, 8, 8, 1, 1, 1, 1, 8, 1, 1, 8, 1, 8, 1, 1, 8, 1, 1, 1]),
  ]
  test = [
      generate(size=5, colors=[1, 1, 1, 1, 4, 1, 4, 4, 4, 4, 1, 4, 1, 1, 1, 2, 2, 2, 2, 1, 4, 1, 1, 2, 1]),
      generate(size=4, colors=[3, 3, 3, 3, 4, 3, 3, 6, 4, 4, 6, 6, 4, 3, 3, 6]),
  ]
  return {"train": train, "test": test}
