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


def generate(width=None, height=None, wide=None, tall=None, brow=None,
             bcol=None, colors=None):
  """Returns input and output grids according to the given parameters.

  Args:
    width: The width of the input grid.
    height: The height of the input grid.
    wide: The width of the sprite.
    tall: The height of the sprite.
    brow: The row of the sprite.
    bcol: The column of the sprite.
    colors: A string representing the sprite.
  """

  if width is None:
    width, height = common.randint(7, 10), common.randint(7, 10)
    tall = 3 if common.randint(0, 1) else 5
    wide = tall + common.randint(0, 1)
    brow = common.randint(0, height - tall)
    bcol = common.randint(0, width - wide)
    while True:
      colors = common.grid(wide, tall)
      for r in range(tall):
        for c in range(wide):
          if common.randint(0, 4): continue
          colors[r][c] = colors[tall - 1 - r][c] = 4
      pixels = []
      for r in range(tall):
        for c in range(wide):
          if colors[r][c] == 4: pixels.append((r, c))
      if not pixels or not common.diagonally_connected(pixels): continue
      rows, cols = zip(*pixels)
      if 0 not in rows or tall - 1 not in rows: continue
      if 0 not in cols or wide - 1 not in cols: continue
      colors = common.flatten(colors)
      colors = "".join(map(str, colors))
      break

  size = 2 * wide + tall
  grid, output = common.grid(width, height), common.grid(size, size)
  for row in range(tall):
    for col in range(wide):
      color = int(colors[row * wide + col])
      grid[brow + row][bcol + col] = color
      output[wide + row][col] = color
      output[wide + row][size - 1 - col] = color
      output[col][wide + row] = color
      output[size - 1 - col][wide + row] = color
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(width=8, height=7, wide=4, tall=3, brow=3, bcol=2,
               colors="040444440404"),
      generate(width=7, height=7, wide=4, tall=3, brow=2, bcol=1,
               colors="044040440440"),
      generate(width=8, height=8, wide=5, tall=5, brow=3, bcol=0,
               colors="4000440444044004044440004"),
      generate(width=7, height=9, wide=5, tall=5, brow=1, bcol=1,
               colors="4440400444000400044444404"),
  ]
  test = [
      generate(width=10, height=8, wide=6, tall=5, brow=1, bcol=1,
               colors="040444044004400040044004040444"),
  ]
  return {"train": train, "test": test}
