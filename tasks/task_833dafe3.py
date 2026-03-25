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
    size: size of the input grid
    colors: digits representing the colors to be used
  """

  if colors is None:
    size = common.randint(3, 8)
    values = common.random_colors(3)
    while True:
      colors = [0] * (size * size)
      for _ in range(size):
        width = common.randint(1, size)
        row = common.randint(0, size - 1)
        col = common.randint(0, size - width)
        color = common.choice(values)
        if common.randint(0, 1):
          for c in range(width):
            colors[row * size + col + c] = color
        else:
          for c in range(width):
            colors[(col + c) * size + row] = color
      if len(set(colors)) == 4: break

  grid, output = common.grid(size, size), common.grid(2 * size, 2 * size)
  for i in range(len(colors)):
    grid[i // size][i % size] = colors[i]
    output[size - 1 - i // size][size - 1 - i % size] = colors[i]
    output[size - 1 - i // size][size + i % size] = colors[i]
    output[size + i // size][size - 1 - i % size] = colors[i]
    output[size + i // size][size + i % size] = colors[i]
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(size=4, colors=[0, 6, 0, 0, 4, 6, 0, 3, 4, 6, 3, 0, 4, 3, 3, 0]),
      generate(size=3, colors=[3, 0, 0, 3, 4, 0, 3, 4, 2]),
  ]
  test = [
      generate(size=8, colors=[0, 0, 1, 0, 0, 0, 0, 0,
                               0, 2, 1, 0, 9, 0, 0, 0,
                               0, 2, 1, 0, 9, 0, 0, 0,
                               0, 2, 1, 0, 9, 1, 1, 1,
                               9, 2, 0, 0, 9, 0, 0, 0,
                               9, 2, 0, 0, 9, 0, 0, 9,
                               1, 2, 0, 0, 9, 0, 0, 9,
                               9, 9, 0, 0, 9, 0, 0, 9]),
  ]
  return {"train": train, "test": test}
