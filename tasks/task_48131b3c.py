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


def generate(size=None, hue=None, colors=None):
  """Returns input and output grids according to the given parameters.

  Args:
    size: The size of the grid.
    hue: The hue of the colors.
    colors: The colors of the grid.
  """

  if size is None:
    size, hue = common.randint(2, 4), common.random_color()
    while True:
      colors = [common.randint(0, 1) for _ in range(size * size)]
      if sum(colors) >= size and sum(colors) <= size * size - size:
        break

  grid, output = common.grid(size, size), common.grid(2 * size, 2 * size)
  for i, color in enumerate(colors):
    grid[i // size][i % size] = color * hue
    for r in range(2):
      for c in range(2):
        output[r * size + i // size][c * size + i % size] = (1 - color) * hue
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(size=2, hue=7, colors=[1, 0, 0, 1]),
      generate(size=3, hue=8, colors=[0, 1, 0, 1, 0, 1, 0, 0, 0]),
      generate(size=4, hue=4,
               colors=[1, 0, 0, 0, 0, 1, 1, 1, 0, 0, 1, 0, 0, 1, 0, 0]),
  ]
  test = [
      generate(size=4, hue=1,
               colors=[0, 1, 0, 1, 1, 0, 0, 1, 0, 0, 1, 0, 1, 0, 0, 0]),
  ]
  return {"train": train, "test": test}
