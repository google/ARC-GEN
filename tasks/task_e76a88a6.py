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


def generate(width=None, height=None, colors=None, rows=None, cols=None,
             size=10):
  """Returns input and output grids according to the given parameters.

  Args:
    width: the width of the *sprite*
    height: the height of the *sprite*
    colors: a list of digits representing colors to be used
    rows: a list of vertical coordinates where the sprites should live
    cols: a list of horizontal coordinates where the sprites should live
    size: the size of the grid
  """
  if width is None:
    while True:
      width, height = common.randint(3, 4), common.randint(3, 4)
      if width < 4 or height < 4: break
    num_pixels, num_sprites = width * height, common.randint(3, 4)
    color_list = common.random_colors(2, exclude=[common.gray()])
    colors = [color_list[common.randint(0, 1)] for _ in range(num_pixels)]
    while True:
      rows = [common.randint(0, size - height) for _ in range(num_sprites)]
      cols = [common.randint(0, size - width) for _ in range(num_sprites)]
      overlaps = False
      for j in range(num_sprites):
        for i in range(j):
          if abs(rows[j] - rows[i]) > height: continue
          if abs(cols[j] - cols[i]) > width: continue
          overlaps = True
      if not overlaps: break

  grid, output = common.grids(size, size)
  for idx in range(len(rows)):
    for r in range(height):
      for c in range(width):
        color = colors[r * width + c]
        grid[rows[idx] + r][cols[idx] + c] = common.gray() if idx > 0 else color
        output[rows[idx] + r][cols[idx] + c] = color
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(width=3, height=3, colors=[2, 2, 2, 2, 4, 4, 4, 4, 4],
               rows=[1, 4, 7], cols=[1, 6, 2]),
      generate(width=4, height=3, colors=[6, 6, 6, 6, 8, 8, 6, 8, 6, 8, 8, 8],
               rows=[1, 0, 5], cols=[1, 6, 4]),
  ]
  test = [
      generate(width=3, height=4, colors=[4, 4, 4, 1, 4, 4, 1, 4, 1, 1, 1, 1],
               rows=[0, 1, 5, 6], cols=[1, 6, 2, 7]),
  ]
  return {"train": train, "test": test}
