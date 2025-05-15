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


def generate(width=None, height=None, rows=None, cols=None, colors=None,
             brows=None, bcols=None, bmags=None):
  """Returns input and output grids according to the given parameters.

  Args:
    width: the width of the grid
    height: the height of the grid
    rows: a list of vertical coordinates where pixels should be placed
    cols: a list of horizontal coordinates where pixels should be placed
    colors: a list of digits representing the colors to be used
    brows: a list of vertical coordinates where boxes should be placed
    bcols: a list of horizontal coordinates where boxes should be placed
    bmags: a list of box magnifiers
  """
  if width is None:
    num_sprites = common.randint(2, 4)
    width, height = 12 if num_sprites < 4 else 14, 14 if num_sprites < 4 else 17
    wide, tall = common.randint(3, 4), common.randint(3, 4)
    # First, choose sprite magnifiers & locations.
    while True:
      bmags = [common.randint(1, 3) for _ in range(num_sprites)]
      bmags[0] = 1  # First one should have no magnifier.
      wides = [bmag * wide for bmag in bmags]
      talls = [bmag * tall for bmag in bmags]
      brows = [common.randint(0, height - t) for t in talls]
      bcols = [common.randint(0, width - w) for w in wides]
      if not common.overlaps(brows, bcols, wides, talls, 1): break
    # Second, choose sprite contents.
    num_pixels = wide * tall // 2 + common.randint(-1, 1)
    pixels = common.continuous_creature(num_pixels, wide, tall)
    rows, cols = zip(*pixels)
    colors = [common.blue()] * num_pixels
    for _ in range(2):
      colors[common.randint(0, num_pixels - 1)] = common.red()

  grid, output = common.grids(width, height)
  for idx in range(len(bmags)):
    brow, bcol, bmag = brows[idx], bcols[idx], bmags[idx]
    for row, col, color in zip(rows, cols, colors):
      for dr in range(bmag):
        for dc in range(bmag):
          r, c = brow + row * bmag + dr, bcol + col * bmag + dc
          common.draw(output, r, c, color)
          if idx and color == common.blue(): continue
          common.draw(grid, r, c, color)
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(width=12, height=14, rows=[0, 0, 0, 0, 1, 2, 2, 2],
               cols=[0, 1, 2, 3, 2, 1, 2, 3], colors=[2, 1, 1, 2, 1, 1, 1, 1],
               brows=[2, 8], bcols=[1, 3], bmags=[1, 2]),
      generate(width=12, height=14, rows=[0, 1, 1, 1, 2, 3],
               cols=[1, 0, 1, 2, 1, 1], colors=[2, 1, 1, 1, 1, 2],
               brows=[3, 8, 9], bcols=[5, 1, 8], bmags=[1, 1, 1]),
      generate(width=12, height=14, rows=[0, 0, 0, 0],
               cols=[0, 1, 2, 3], colors=[1, 1, 1, 2],
               brows=[2, 7], bcols=[1, -2], bmags=[1, 3]),
  ]
  test = [
      generate(width=21, height=17, rows=[0, 1, 1, 2, 2, 2],
               cols=[0, 0, 2, 0, 1, 2], colors=[1, 1, 2, 1, 1, 1],
               brows=[2, 1, 5, 9], bcols=[2, 10, 11, 1], bmags=[1, 1, 3, 2]),
  ]
  return {"train": train, "test": test}
