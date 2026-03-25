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


def generate(rows=None, cols=None, thick=None, color=None, flip=None,
             xpose=None, size=14):
  """Returns input and output grids according to the given parameters.

  Args:
    rows: a list of vertical coordinates where pixels should be placed
    cols: a list of horizontal coordinates where pixels should be placed
    thick: the thickness of the horizon
    color: the color of the pixels
    flip: whether to flip the grid vertically
    xpose: whether to transpose the grid
    size: the size of the grid
  """
  if rows is None:
    thick = common.randint(2, 5)
    while True:
      pixels = common.random_pixels(size, size, 0.05)
      pixels = [p for p in pixels if p[0] < 5 or p[0] >= 5 + thick]
      if pixels: break
    rows, cols = zip(*pixels)
    color = common.random_color(exclude=[common.gray()])
    flip, xpose = common.randint(0, 1), common.randint(0, 1)

  grid, output = common.grids(size, size)
  for r in range(thick):
    for c in range(size):
      output[5 + r][c] = grid[5 + r][c] = common.gray()
  for r, c in zip(rows, cols):
    grid[r][c] = color
    dr = 1 if r < 5 else -1
    r = 0 if r < 5 else size - 1
    while output[r + dr][c] == 0:
      r += dr
    output[r][c] = common.gray()
  if flip: grid, output = grid[::-1], output[::-1]
  if xpose: grid, output = common.transpose(grid), common.transpose(output)
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(rows=[0, 2, 3, 9, 10, 11, 12], cols=[8, 2, 10, 9, 1, 4, 11],
               thick=4, color=2, flip=0, xpose=0),
      generate(rows=[1, 1, 1, 2, 3, 3, 4, 10, 11, 12, 13],
               cols=[0, 6, 9, 2, 6, 12, 1, 2, 9, 7, 4],
               thick=5, color=3, flip=1, xpose=1),
      generate(rows=[2, 2, 3, 4, 8, 10, 10, 10, 12],
               cols=[3, 8, 11, 1, 8, 3, 7, 12, 7],
               thick=2, color=1, flip=1, xpose=0),
  ]
  test = [
      generate(rows=[1, 1, 2, 3, 3, 7, 9, 10, 11, 12],
               cols=[4, 11, 1, 3, 11, 6, 1, 11, 6, 13],
               thick=2, color=4, flip=0, xpose=1),
  ]
  return {"train": train, "test": test}
