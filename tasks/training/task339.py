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


def generate(rows=None, cols=None, color=None, size=3):
  """Returns input and output grids according to the given parameters.

  Args:
    rows: a list of vertical coordinates where pixels should be placed
    cols: a list of horizontal coordinates where pixels should be placed
    color: the color of the pixels
    size: the width and height of the (square) grid
  """
  if rows is None:
    count = common.randint(1, 9)
    pixels = common.sample(common.all_pixels(size, size), count)
    rows, cols = zip(*pixels)
    color = common.random_color()

  grid, output = common.grid(size, size), common.grid(len(rows), 1, color)
  for r, c in zip(rows, cols):
    grid[r][c] = color
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(rows=[1, 2], cols=[0, 1], color=1),
      generate(rows=[0, 1, 2], cols=[1, 0, 1], color=2),
      generate(rows=[0], cols=[1], color=7),
      generate(rows=[0, 1, 1, 2], cols=[1, 0, 1, 0], color=8),
  ]
  test = [
      generate(rows=[0, 0, 1, 1, 2], cols=[0, 1, 0, 2, 2], color=4),
  ]
  return {"train": train, "test": test}
