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


def generate(rows=None, cols=None, colors=None, size=3):
  """Returns input and output grids according to the given parameters.

  Args:
    rows: a list of vertical coordinates where pixels should be placed
    cols: a list of horizontal coordinates where pixels should be placed
    colors: a list of digits representing colors to be used
    size: the width and height of the (square) grid
  """
  if rows is None:
    pixels = common.all_pixels(size, size)
    pixels = common.sample(pixels, common.randint(2, 8))
    rows, cols = zip(*pixels)
    colors = [common.randint(1, 2) for _ in pixels]

  grid = common.grid(size, size)
  output = common.grid(size * size, size * size)
  for r, c, color in zip(rows, cols, colors):
    grid[r][c] = color
    if color != common.red(): continue
    for rr, cc, colorcolor in zip(rows, cols, colors):
      output[r * size + rr][c * size + cc] = colorcolor
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(rows=[0, 1, 1, 2], cols=[0, 0, 1, 2], colors=[1, 2, 1, 1]),
      generate(rows=[0, 0, 1, 1, 2], cols=[1, 2, 0, 1, 0],
               colors=[1, 2, 1, 1, 2]),
      generate(rows=[0, 0, 0, 1, 1, 2, 2], cols=[0, 1, 2, 1, 2, 0, 1],
               colors=[2, 1, 2, 2, 1, 2, 1]),
  ]
  test = [
      generate(rows=[0, 0, 0, 1, 1, 2, 2], cols=[0, 1, 2, 0, 2, 0, 1],
               colors=[1, 2, 2, 2, 1, 1, 2]),
  ]
  return {"train": train, "test": test}
