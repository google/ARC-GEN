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


def generate(wides=None, talls=None, brows=None, bcols=None, colors=None):
  """Returns input and output grids according to the given parameters.

  Args:
    wides: The widths of the rectangles.
    talls: The heights of the rectangles.
    brows: The row coordinates of the top of each rectangle.
    bcols: The column coordinates of the left of each rectangle.
    colors: The colors of the rectangles.
  """

  def draw():
    grid, output = common.grid(19, 18, 8), common.grid(1, len(colors))
    last_color = None
    # Draw the squares, and make sure each covers up part of the previous one.
    specials = []
    for i, (wide, tall, brow, bcol, color) in enumerate(zip(wides, talls, brows, bcols, colors)):
      seen = False
      for r in range(tall):
        for c in range(wide):
          if r in [0, tall - 1] or c in [0, wide - 1]:
            if grid[brow + r][bcol + c] == last_color:
              if (brow + r, bcol + c) in specials: return None, None
              specials.append((brow + r, bcol + c))
              seen = True
            grid[brow + r][bcol + c] = color
      if last_color is not None and not seen: return None, None
      last_color = output[i][0] = color
    # Check that at least three corners are visible.
    for wide, tall, brow, bcol, color in zip(wides, talls, brows, bcols, colors):
      corners = 0
      for r in [0, tall - 1]:
        for c in [0, wide - 1]:
          if grid[brow + r][bcol + c] == color: corners += 1
      if corners < 3: return None, None
    return grid, output

  if wides is None:
    colors = common.random_colors(common.randint(4, 5), exclude=[8])
    while True:
      wides = [common.randint(3, 17) for _ in range(len(colors))]
      talls = [common.randint(3, 17) for _ in range(len(colors))]
      brows = [common.randint(0, 18 - t) for t in talls]
      bcols = [common.randint(0, 19 - w) for w in wides]
      grid, _ = draw()
      if grid: break

  grid, output = draw()
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(wides=[5, 16, 4, 8, 3], talls=[16, 12, 12, 9, 5],
               brows=[1, 3, 5, 7, 5], bcols=[1, 3, 7, 9, 12],
               colors=[3, 6, 4, 2, 5]),
      generate(wides=[15, 12, 9, 5, 3], talls=[9, 11, 6, 6, 2],
               brows=[8, 3, 1, 5, 10], bcols=[2, 4, 1, 7, 10],
               colors=[2, 3, 7, 6, 9]),
      generate(wides=[16, 13, 9, 5], talls=[6, 16, 12, 5], brows=[4, 1, 6, 3],
               bcols=[1, 3, 5, 7], colors=[2, 3, 6, 4]),
      generate(wides=[6, 12, 5, 4], talls=[6, 7, 7, 5], brows=[1, 3, 7, 11],
               bcols=[2, 5, 9, 11], colors=[1, 2, 4, 6]),
  ]
  test = [
      generate(wides=[17, 14, 13, 5, 3], talls=[8, 16, 6, 7, 2],
               brows=[7, 1, 0, 3, 9], bcols=[1, 3, 1, 6, 5],
               colors=[2, 4, 1, 6, 5]),
  ]
  return {"train": train, "test": test}
