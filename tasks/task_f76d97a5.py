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


def generate(size=None, rows=None, cols=None, color=None):
  """Returns input and output grids according to the given parameters.

  Args:
    size: the width and height of the (square) grid
    rows: a list of vertical coordinates where pixels should be placed
    cols: a list of horizontal coordinates where pixels should be placed
    color: a digit representing a color to be used
  """
  if size is None:
    size = common.randint(3, 5)
    num_pixels = common.randint(size, (size * size + 1) // 2)
    pixels = common.sample(common.all_pixels(size, size), num_pixels)
    rows, cols = zip(*pixels)
    color = common.random_color(exclude=[common.gray()])

  grid, output = common.grid(size, size, color), common.grid(size, size)
  for r, c in zip(rows, cols):
    grid[r][c] = common.gray()
    output[r][c] = color
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(size=3, rows=[0, 1, 1, 1, 2], cols=[1, 0, 1, 2, 1], color=4),
      generate(size=5, rows=[0, 0, 1, 1, 2, 2, 3, 3, 4, 4, 4],
               cols=[0, 1, 1, 2, 2, 3, 3, 4, 0, 4], color=6),
      generate(size=5, rows=[0, 1, 1, 2, 3, 4, 4], cols=[1, 2, 3, 1, 2, 3, 4],
               color=9),
  ]
  test = [
      generate(size=5, rows=[0, 1, 2, 2, 2, 3, 4, 4, 4],
               cols=[3, 1, 1, 2, 4, 3, 0, 1, 2], color=3),
  ]
  return {"train": train, "test": test}
