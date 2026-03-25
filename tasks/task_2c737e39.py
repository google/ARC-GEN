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


def generate(width=None, height=None, wide=None, tall=None, brows=None,
             bcols=None, colors=None):
  """Returns input and output grids according to the given parameters.

  Args:
    width: The width of the grids.
    height: The height of the grids.
    wide: The width of the shapes.
    tall: The height of the shapes.
    brows: The row coordinates of the top of the shapes.
    bcols: The column coordinates of the left of the shapes.
    colors: The colors of the shapes.
  """

  def draw():
    grid, output = common.grids(width, height)
    ids = common.grid(width, height, -1)
    for i, (brow, bcol) in enumerate(zip(brows, bcols)):
      for row in range(tall):
        for col in range(wide):
          color = int(colors[row * wide + col])
          if color == 0: continue
          ids[brow + row][bcol + col] = i
          if i == 0:
            grid[brow + row][bcol + col] = color
            output[brow + row][bcol + col] = color
          else:
            grid[brow + row][bcol + col] = color if color == 5 else 0
            output[brow + row][bcol + col] = color if color != 5 else 0
    # Check that the shapes are not touching.
    for row in range(height):
      for col in range(width):
        if ids[row][col] == -1: continue
        for dr in [-1, 0, 1]:
          for dc in [-1, 0, 1]:
            pixel = common.get_pixel(ids, row + dr, col + dc)
            if pixel not in [-1, ids[row][col]]: return None, None
    return grid, output

  if width is None:
    width, height = common.randint(9, 12), common.randint(9, 12)
    while True:
      wide, tall = common.randint(2, 6), common.randint(3, 5)
      brows = [common.randint(0, height - tall) for _ in range(2)]
      bcols = [common.randint(0, width - wide) for _ in range(2)]
      if common.overlaps(brows, bcols, [wide] * 2, [tall] * 2): continue
      pixels = []
      for row in range(tall):
        for col in range(wide):
          if common.randint(0, 1):
            pixels.append((row, col))
      if len(pixels) < 6 or not common.connected(pixels): continue
      hues = [common.random_color(exclude=[5]) for _ in pixels]
      hues[common.randint(0, len(hues) - 1)] = 5
      colors = [0] * (wide * tall)
      for (row, col), hue in zip(pixels, hues):
        colors[row * wide + col] = hue
      grid, _ = draw()
      if grid: break

  grid, output = draw()
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(width=12, height=12, wide=2, tall=3, brows=[2, 6], bcols=[2, 6],
               colors="332225"),
      generate(width=10, height=12, wide=4, tall=5, brows=[0, 5], bcols=[1, 4],
               colors="00300131445000100072"),
      generate(width=10, height=9, wide=3, tall=4, brows=[0, 4], bcols=[3, 2],
               colors="100110520023"),
  ]
  test = [
      generate(width=10, height=11, wide=6, tall=3, brows=[8, 2], bcols=[1, 4],
               colors="005000223300103388"),
  ]
  return {"train": train, "test": test}
