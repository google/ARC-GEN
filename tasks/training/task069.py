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


def generate(rows=None, cols=None, colors=None, megarows=None, megacols=None,
             size=10, num_boxes=4):
  """Returns input and output grids according to the given parameters.

  Args:
    rows: a list of vertical coordinates for pixels in a sprite
    cols: a list of horizontal coordinates for pixels in a sprite
    colors: digits representing the colors to be used
    megarows: a list of vertical coordinates for the sprite locations
    megacols: a list of horizontal coordinates for the sprite locations
    size: the width and height of the (square) grid
    num_boxes: the number of boxes to be placed
  """
  if rows is None:
    width, height = common.randint(2, 4), common.randint(2, 3)
    all_pixels = common.all_pixels(width, height)
    num_pixels = len(all_pixels)
    num_sampled = common.randint(num_pixels // 2, num_pixels)
    while True:
      pixels = common.sample(all_pixels, num_sampled)
      if common.connected(pixels): break
    rows, cols = zip(*pixels)
    num_colors = common.randint(2, 4)
    color_list = common.random_colors(num_colors, exclude=[common.cyan()])
    while True:
      colors = common.choices(color_list, k=len(pixels))
      if len(set(colors)) > 1: break
    while True:
      megarows = [common.randint(0, size - height) for _ in range(num_boxes)]
      megacols = [common.randint(0, size - width) for _ in range(num_boxes)]
      wides, talls = [width] * num_boxes, [height] * num_boxes
      if not common.overlaps(megarows, megacols, wides, talls, 1): break

  grid, output = common.grids(size, size)
  for idx in range(len(megarows)):
    mr, mc = megarows[idx], megacols[idx]
    for r, c, color in zip(rows, cols, colors):
      grid[mr + r][mc + c] = color if idx == 0 else common.cyan()
      output[mr + r][mc + c] = common.black() if idx == 0 else color
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(rows=[0, 0, 1, 1], cols=[0, 1, 0, 1], colors=[7, 6, 9, 4],
               megarows=[1, 4, 7, 8], megacols=[1, 5, 2, 8]),
      generate(rows=[0, 0, 1, 1, 1], cols=[0, 1, 0, 1, 2],
               colors=[7, 7, 6, 6, 6], megarows=[5, 1, 2, 7],
               megacols=[5, 1, 6, 3]),
  ]
  test = [
      generate(rows=[0, 0, 1, 1, 1, 1, 2], cols=[1, 2, 0, 1, 2, 3, 2],
               colors=[4, 4, 3, 4, 3, 3, 3], megarows=[5, 1, 1, 6],
               megacols=[0, 0, 5, 5]),
  ]
  return {"train": train, "test": test}
