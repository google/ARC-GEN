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


def generate(rows=None, cols=None, color=None, width=7, height=5, size=3):
  """Returns input and output grids according to the given parameters.

  Args:
    rows: a list of vertical coordinates where pixels should be placed
    cols: a list of horizontal coordinates where pixels should be placed
    color: a digit representing a color to be used
    width: the width of the grid
    height: the width of the grid
    size: the size of the (square) output grid
  """
  if rows is None:
    pixels = common.random_pixels(width, height)
    pixels = [p for p in pixels if not (p[0] == 2 or p[1] in [2, 3, 4])]
    rows, cols = zip(*pixels)
    color = common.random_color()

  grid, output = common.grid(width, height), common.grid(size, size)
  for r, c in zip(rows, cols):
    grid[r][c] = color
    r = r if r < 2 else r - 2
    c = c if c < 2 else c - 4
    output[r][c] = color
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(rows=[0, 0, 1, 1, 1, 1, 3, 3, 3, 3, 4, 4],
               cols=[1, 5, 0, 1, 5, 6, 0, 1, 5, 6, 1, 5], color=8),
      generate(rows=[0, 0, 0, 0, 1, 3, 3, 4, 4],
               cols=[0, 1, 5, 6, 6, 1, 5, 0, 6], color=2),
      generate(rows=[0, 0, 0, 1, 1, 4, 4],
               cols=[0, 1, 5, 5, 6, 0, 6], color=4),
      generate(rows=[0, 0, 4, 4, 4], cols=[0, 6, 0, 5, 6], color=4),
      generate(rows=[0, 0, 1, 1, 4], cols=[1, 5, 0, 6, 6], color=3),
  ]
  test = [
      generate(rows=[0, 0, 1, 4, 4], cols=[5, 6, 0, 1, 6], color=1),
  ]
  return {"train": train, "test": test}
