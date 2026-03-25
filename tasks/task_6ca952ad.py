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


def generate(size=None, wides=None, talls=None, brows=None, bcols=None,
             colors=None, groups=None, fgcolor=None):
  """Returns input and output grids according to the given parameters.

  Args:
    size: The size of the grids.
    wides: The widths of the shapes.
    talls: The heights of the shapes.
    brows: The rows of the shapes.
    bcols: The columns of the shapes.
    colors: The colors of the shapes.
    groups: The groups of the colors.
    fgcolor: The foreground color.
  """

  def draw():
    if common.overlaps_1d(bcols, wides): return None, None
    grid, output = common.grids(size, size, 7)
    igrid, ioutput = common.grids(size, size, -1)
    num_boxes, num_small = len(wides), 0
    for i, (wide, tall, brow, bcol) in enumerate(zip(wides, talls, brows, bcols)):
      hues = [int(c) for c, g in zip(colors, groups) if int(g) == i]
      if sum(hues) <= 3: num_small += 1
      for row in range(tall):
        for col in range(wide):
          orow = brow if sum(hues) <= 3 else (size - tall)
          hue = hues[row * wide + col]
          grid[brow + row][bcol + col] = fgcolor if hue else 7
          output[orow + row][bcol + col] = fgcolor if hue else 7
          igrid[brow + row][bcol + col] = i if hue else -1
          ioutput[orow + row][bcol + col] = i if hue else -1
    # Check that we have the appropriate number of small boxes.
    if num_small < num_boxes // 2 or num_small > num_boxes // 2:
      return None, None
    # Check that no two boxes are diagonally connected.
    for g in [igrid, ioutput]:
      for row in range(1, size - 1):
        for col in range(1, size - 1):
          if g[row][col] == -1: continue
          for dr in range(-1, 2):
            for dc in range(-1, 2):
              if g[row + dr][col + dc] == -1: continue
              if g[row + dr][col + dc] != g[row][col]: return None, None
    return grid, output

  if size is None:
    size, fgcolor = common.randint(7, 16), common.random_color(exclude=[7])
    num_boxes = (size + 1) // 3
    while True:
      wides = [common.randint(1, 4) for _ in range(num_boxes)]
      talls = [common.randint(1, 4) for _ in range(num_boxes)]
      brows = [common.randint(0, size - tall - 1) for tall in talls]
      bcols = [common.randint(0, size - wide) for wide in wides]
      colors, groups = [], []
      for group, (wide, tall) in enumerate(zip(wides, talls)):
        pixels = common.connected_sprite(wide, tall, min(wide, tall) - 1)
        for row in range(tall):
          for col in range(wide):
            colors.append(1 if (row, col) in pixels else 0)
            groups.append(group)
      grid, _ = draw()
      if grid: break

  grid, output = draw()
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(size=7, wides=[2, 2], talls=[2, 4], brows=[1, 1], bcols=[1, 4],
               colors="110111110101", groups="000011111111", fgcolor=6),
      generate(size=15, wides=[2, 1, 2, 3, 1], talls=[2, 1, 3, 3, 3],
               brows=[1, 3, 2, 1, 3], bcols=[1, 4, 6, 9, 13], colors="11111111111111111111111", groups="00001222222333333333444", fgcolor=5),
      generate(size=16, wides=[2, 1, 2, 1, 4], talls=[5, 2, 3, 3, 3],
               brows=[1, 2, 8, 5, 2], bcols=[1, 4, 6, 9, 11],
               colors="111111111111011111111111110011111",
               groups="000000000011222222333444444444444", fgcolor=1),
  ]
  test = [
      generate(size=14, wides=[2, 1, 1, 3, 2], talls=[2, 3, 1, 4, 4],
               brows=[1, 1, 1, 1, 1], bcols=[1, 4, 6, 7, 11],
               colors="1111111101101111111111111111",
               groups="0000111233333333333344444444", fgcolor=4),
  ]
  return {"train": train, "test": test}
