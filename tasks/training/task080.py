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


def generate(size=None, rows=None, cols=None, colors=None, spacing=None,
             linecolor=None):
  """Returns input and output grids according to the given parameters.

  Args:
    size: the width and height of the bitmap
    rows: a list of vertical coordinates where pixels should be placed
    cols: a list of horizontal coordinates where pixels should be placed
    colors: a list of colors to be used for the middle / edges / corners
    spacing: how much spacing to leave in between the lines
    linecolor: the color of the lines
  """
  if size is None:
    size = common.randint(5, 10)
    while True:
      pixels = common.sample(common.all_pixels(size, size), (size - 1) // 2)
      rows, cols = zip(*pixels)
      lengths = [3] * len(pixels)
      if rows[0] in [0, size - 1] or cols[0] in [0, size - 1]: continue
      if not common.overlaps(rows, cols, lengths, lengths): break
    linecolor, spacing = common.random_color(), 6 - (size - 1) // 2
    num = common.randint(1, 2)  # Number of extra colors
    center = common.random_color(exclude=[linecolor])
    ext = [common.random_color(exclude=[linecolor, center]) for _ in range(num)]
    colors = [center] + ext

  bitmap = common.grid(size, size)
  def draw(max_idx):
    for idx in range(len(rows)):
      row, col = rows[idx], cols[idx]
      common.draw(bitmap, row, col, colors[0])
      if idx > max_idx: continue  # In the input grid, we only draw one of them.
      for dr, dc in [(-1, 0), (0, 1), (1, 0), (0, -1)]:
        common.draw(bitmap, row + dr, col + dc, colors[1])
      if len(colors) < 3: continue
      for dr, dc in [(-1, 1), (1, 1), (1, -1), (-1, -1)]:
        common.draw(bitmap, row + dr, col + dc, colors[2])
  draw(0)
  grid = common.create_linegrid(bitmap, spacing, linecolor)
  draw(len(rows))
  output = common.create_linegrid(bitmap, spacing, linecolor)
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(size=5, rows=[1, 4], cols=[1, 3], colors=[6, 3], spacing=4,
               linecolor=8),
      generate(size=7, rows=[2, 0, 5], cols=[2, 6, 3], colors=[4, 6], spacing=3,
               linecolor=3),
      generate(size=7, rows=[4, 0, 1], cols=[4, 6, 1], colors=[2, 4, 4],
               spacing=3, linecolor=8),
  ]
  test = [
      generate(size=10, rows=[3, 1, 7, 8], cols=[3, 7, 5, 0], colors=[6, 3, 8],
               spacing=2, linecolor=4),
  ]
  return {"train": train, "test": test}
