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


def generate(size=None, spacing=None, linecolor=None, brow=None, bcol=None,
             colors=None):
  """Returns input and output grids according to the given parameters.

  Args:
    size: the width and height of the input grid (in cells)
    spacing: the spacing between the lines (in pixels)
    linecolor: the color of the lines
    brow: the row of the box
    bcol: the column of the box
    colors: the colors of the pixels
  """
  if size is None:
    size, spacing = 10, common.randint(2, 4)
    if spacing == 3: size = 7
    if spacing == 4: size = 6
    brow, bcol = common.randint(0, size - 5), common.randint(0, size - 5)
    linecolor = common.random_color()
    num_colors = 2 if common.randint(0, 4) else 3
    while True:
      color_list = common.random_colors(num_colors, exclude=[linecolor])
      colors = [common.choice(color_list + [0]) for _ in range(9)]
      if len(set(colors)) != num_colors + 1: continue  # Need all (plus black)
      rlist = [i // 3 for i, color in enumerate(colors) if color]
      clist = [i % 3 for i, color in enumerate(colors) if color]
      if 0 not in rlist or 2 not in rlist or 0 not in clist or 2 not in clist:
        continue  # Can't have any empty margins.
      illegal = False
      for row in range(3):
        for col in range(3):
          if not colors[row * 3 + col]: continue
          for dr in [-1, 0, 1]:
            for dc in [-1, 0, 1]:
              if (not dr) and (not dc): continue
              r, c = row + dr, col + dc
              if r < 0 or r >= 3 or c < 0 or c >= 3 or not colors[r * 3 + c]:
                continue
              if colors[r * 3 + c] != colors[row * 3 + col]: illegal = True
      # All pixels of the same color must be connected.
      for hue in color_list:
        rlist = [i // 3 for i, color in enumerate(colors) if color == hue]
        clist = [i % 3 for i, color in enumerate(colors) if color == hue]
        if not common.diagonally_connected(list(zip(rlist, clist))):
          illegal = True
      if not illegal: break

  grid = common.create_linegrid(common.grid(size, size), spacing, linecolor)
  output = common.grid(3, 3)
  for row in range(3):
    for col in range(3):
      if not colors[row * 3 + col]: continue
      output[row][col] = colors[row * 3 + col]
      for dr, dc in [(0, 0), (0, 1), (1, 0), (1, 1)]:
        r = (brow + row + dr + 1) * (spacing + 1) - 1
        c = (bcol + col + dc + 1) * (spacing + 1) - 1
        grid[r][c] = colors[row * 3 + col]
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(size=10, spacing=2, linecolor=4, brow=1, bcol=1,
               colors=[1, 0, 3, 1, 0, 0, 1, 0, 0]),
      generate(size=7, spacing=3, linecolor=3, brow=1, bcol=0,
               colors=[0, 2, 0, 2, 0, 0, 0, 0, 8]),
      generate(size=10, spacing=2, linecolor=1, brow=3, bcol=4,
               colors=[6, 6, 0, 0, 0, 0, 3, 3, 3]),
      generate(size=7, spacing=3, linecolor=8, brow=1, bcol=1,
               colors=[1, 0, 2, 0, 0, 2, 2, 2, 2]),
  ]
  test = [
      generate(size=6, spacing=4, linecolor=2, brow=0, bcol=0,
               colors=[1, 0, 4, 0, 0, 0, 8, 8, 8]),
  ]
  return {"train": train, "test": test}
