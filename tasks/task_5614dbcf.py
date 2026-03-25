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


def generate(rows=None, cols=None, colors=None, pixelrows=None, pixelcols=None,
             size=3):
  """Returns input and output grids according to the given parameters.

  Args:
    rows: a list of vertical coordinates where boxes should be placed
    cols: a list of horizontal coordinates where boxes should be placed
    colors: a list of digits representing the colors to be used
    pixelrows: a list of vertical coordinates where pixels should be placed
    pixelcols: a list of horizontal coordinates where pixels should be placed
    size: the size of the grid
  """
  if rows is None:
    boxes = common.sample(common.all_pixels(size, size), common.randint(1, 8))
    rows, cols = zip(*boxes)
    colors = common.random_colors(len(boxes), exclude=[common.gray()])
    pixelrows, pixelcols = [], []
    for r in range(size):
      for c in range(size):
        rand = common.randint(0, 9)
        if rand > 5: continue  # sometimes we leave it empty
        num_pixels = 2 if rand == 0 else 1
        pixels = common.sample(common.all_pixels(size, size), num_pixels)
        for p in pixels:
          pixelrows.append(r * size + p[0])
          pixelcols.append(c * size + p[1])

  grid = common.grid(size * size, size * size)
  output = common.grid(size, size)
  for r, c, color in zip(rows, cols, colors):
    for dr in range(size):
      for dc in range(size):
        grid[r * size + dr][c * size + dc] = color
    output[r][c] = color
  for r, c in zip(pixelrows, pixelcols):
    grid[r][c] = common.gray()
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(rows=[0, 0, 1, 2, 2], cols=[0, 2, 1, 0, 2],
               colors=[3, 8, 7, 6, 9], pixelrows=[1, 3, 6, 8, 8, 8],
               pixelcols=[7, 4, 5, 1, 4, 8]),
      generate(rows=[0, 2], cols=[1, 1], colors=[2, 7],
               pixelrows=[1, 3, 4, 4, 6, 7], pixelcols=[1, 0, 3, 7, 1, 5]),
  ]
  test = [
      generate(rows=[0, 1, 2], cols=[0, 1, 1], colors=[4, 3, 9],
               pixelrows=[0, 1, 2, 3, 6, 7], pixelcols=[7, 0, 4, 7, 2, 4]),
  ]
  return {"train": train, "test": test}
