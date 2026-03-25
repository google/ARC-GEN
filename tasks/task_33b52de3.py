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


def generate(width=None, height=None, brow=None, bcol=None, srow=None,
             scol=None, shape=None, colors=None):
  """Returns input and output grids according to the given parameters.

  Args:
    width: The width of the color grid.
    height: The height of the color grid.
    brow: The row where the boxes start.
    bcol: The column where the boxes start.
    srow: The row where the colorful sprite starts.
    scol: The column where the colorful sprite starts.
    shape: The shape of the sprite.
    colors: The colors of the boxes.
  """

  if width is None:
    shape = [1] * 9
    shape[common.randint(0, 8)] = shape[common.randint(0, 8)] = 0
    while True:
      width, height = common.randint(3, 5), common.randint(3, 5)
      if width + height < 10: break
    subset = common.sample([1, 2, 3, 4, 8], common.randint(3, 5))
    colors = common.choices(subset, width * height)
    while True:
      brow = common.randint(1, 23 - 4 * height)
      bcol = common.randint(1, 23 - 4 * width)
      srow = common.randint(1, 23 - height - 1)
      scol = common.randint(1, 23 - width - 1)
      if srow + height < brow or scol + width < bcol: break
      if brow + 4 * height < srow or bcol + 4 * width < scol: break

  grid, output = common.grids(23, 23)
  for row in range(height):
    for col in range(width):
      grid[srow + row][scol + col] = colors[row * width + col]
      output[srow + row][scol + col] = colors[row * width + col]
      for r in range(3):
        for c in range(3):
          if not shape[r * 3 + c]: continue
          grid[brow + row * 4 + r][bcol + col * 4 + c] = 5
          output[brow + row * 4 + r][bcol + col * 4 + c] = colors[row * width + col]
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(width=4, height=4, brow=1, bcol=6, srow=3, scol=1,
               shape=[1, 1, 1, 0, 1, 0, 1, 1, 1],
               colors=[1, 8, 1, 8, 8, 8, 1, 1, 1, 1, 4, 1, 1, 1, 4, 4]),
      generate(width=5, height=3, brow=1, bcol=2, srow=19, scol=1,
               shape=[1, 1, 1, 1, 0, 1, 1, 1, 1],
               colors=[2, 1, 1, 3, 1, 1, 2, 2, 1, 1, 2, 1, 2, 3, 2]),
  ]
  test = [
      generate(width=4, height=5, brow=1, bcol=7, srow=2, scol=1,
               shape=[1, 1, 1, 1, 0, 1, 1, 0, 1],
               colors=[2, 1, 2, 2, 8, 1, 4, 4, 3, 1, 4, 4, 8, 1, 3, 1, 8, 1, 1, 1]),
  ]
  return {"train": train, "test": test}
