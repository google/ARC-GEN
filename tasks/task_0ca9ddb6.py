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


def generate(rows=None, cols=None, colors=None, size=9, twinklers=(1, 2)):
  """Returns input and output grids according to the given parameters.

  Args:
    rows: a list of vertical coordinates where pixels should be placed
    cols: a list of horizontal coordinates where pixels should be placed
    colors: a list of digits representing colors to be used
    size: the width and height of the (square) grid
    twinklers: a list of integers representing stars that twinkle
  """
  if rows is None:
    pixels = common.all_pixels(size, size)
    pixels = common.sample(pixels, common.randint(1, 6))
    rows, cols = [p[0] for p in pixels], [p[1] for p in pixels]
    colors = [common.choice([1, 2, 6, 8]) for _ in pixels]
    # Scooch any twinkling stars away from the edges.
    for idx in range(len(pixels)):
      if colors[idx] not in twinklers: continue
      rows[idx] = rows[idx] if rows[idx] > 0 else 1
      rows[idx] = rows[idx] if rows[idx] < size - 1 else size - 2
      cols[idx] = cols[idx] if cols[idx] > 0 else 1
      cols[idx] = cols[idx] if cols[idx] < size - 1 else size - 2
    # Only keep stars that don't clobber each other.
    keep = []
    for idx in range(len(pixels)):
      good = True
      my_radius = 1 if colors[idx] in twinklers else 0
      for prev in range(idx):
        prev_radius = 1 if colors[prev] in twinklers else 0
        radius = my_radius + prev_radius
        if abs(rows[idx] - rows[prev]) > radius: continue
        if abs(cols[idx] - cols[prev]) > radius: continue
        good = False
      if good:
        keep.append(idx)
    rows = [rows[idx] for idx in keep]
    cols = [cols[idx] for idx in keep]
    colors = [colors[idx] for idx in keep]

  grid, output = common.grids(size, size)
  for r, c, color in zip(rows, cols, colors):
    output[r][c] = grid[r][c] = color
    if color == twinklers[0]:  # blue stars twinkle like a rook
      for dr, dc in [(1, 0), (0, 1), (-1, 0), (0, -1)]:
        output[r + dr][c + dc] = 7
    if color == twinklers[1]:  # red stars twinkle like a bishop
      for dr, dc in [(1, 1), (-1, 1), (1, -1), (-1, -1)]:
        output[r + dr][c + dc] = 4
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(rows=[3, 6], cols=[2, 6], colors=[2, 1]),
      generate(rows=[0, 2, 3, 6, 7], cols=[3, 6, 2, 6, 1],
               colors=[8, 2, 1, 1, 2]),
      generate(rows=[2, 5, 7], cols=[2, 6, 3], colors=[2, 6, 1]),
  ]
  test = [
      generate(rows=[2, 3, 5, 7, 7], cols=[6, 2, 5, 7, 1],
               colors=[1, 2, 8, 2, 6]),
  ]
  return {"train": train, "test": test}
