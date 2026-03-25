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


def generate(length=None, size=None, brow=None, bcol=None, subset=None,
             colors=None, patterns=None):
  """Returns input and output grids according to the given parameters.

  Args:
    length: The length of the grey sprites.
    size: The size of the color grid.
    brow: The row of the color grid.
    bcol: The column of the color grid.
    subset: The subset of colors to use.
    colors: The colors of the grid.
    patterns: The patterns of the sprites.
  """

  def draw():
    inwidth, outwidth = (3 + length + 1) * len(subset) - 1, length * size
    if inwidth > 30 or outwidth > 30: return None, None
    grid, output = common.grid(inwidth, 15), common.grid(outwidth, outwidth)
    color_to_idx = {}
    for i, color in enumerate(subset):
      color_to_idx[color] = i
      common.rect(grid, 2, 2, 0, 3 * i, color)
      for row in range(length):
        for col in range(length):
          color = int(patterns[i * length * length + row * length + col])
          grid[row][3 * len(subset) + (length + 1) * i + col] = color
    for row in range(size):
      for col in range(size):
        color = int(colors[row * size + col])
        grid[brow + row][bcol + col] = color
        idx = color_to_idx[color]
        for r in range(length):
          for c in range(length):
            hue = int(patterns[idx * length * length + r * length + c])
            if hue: output[row * length + r][col * length + c] = color
    return grid, output

  if length is None:
    while True:
      length, size = common.randint(3, 6), common.randint(4, 7)
      brow, bcol = common.randint(length + 1, 15 - size), common.randint(1, 5)
      subset = common.sample([1, 2, 3, 4, 8], common.randint(2, 4))
      while True:
        colors = common.choices(subset, size * size)
        if len(set(colors)) == len(subset): break
      colors = "".join(map(str, colors))
      patterns = []
      for _ in subset:
        rows, cols = common.conway_sprite(length, length, length)
        pixels = list(zip(rows, cols))
        for row in range(length):
          for col in range(length):
            patterns.append(5 if (row, col) in pixels else 0)
      patterns = "".join(map(str, patterns))
      grid, _ = draw()
      if grid: break

  grid, output = draw()
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(length=3, size=5, brow=6, bcol=3, subset=[1, 3, 2],
               colors="1231221321333331231221321",
               patterns="555505555555050555555500555"),
      generate(length=5, size=4, brow=7, bcol=4, subset=[2, 4],
               colors="4242224244422222",
               patterns="55555500005055550000555555555550005505555055055500"),
      generate(length=5, size=6, brow=6, bcol=2, subset=[8, 1],
               colors="818181181818818181181818818181181818",
               patterns="55555500055050550555500005555550005505055550500005"),
  ]
  test = [
      generate(length=3, size=7, brow=6, bcol=5, subset=[1, 2, 3, 8],
               colors="2218883211821311882138882218822211881111823338822",
               patterns="555500555555005555555505555555050555"),
      generate(length=6, size=5, brow=9, bcol=4, subset=[1, 4, 8],
               colors="4141488888141418888841414",
               patterns="555555500005505505505505505005505555555555500005505505505555500000555555555555500005505505505505500005555555"),
  ]
  return {"train": train, "test": test}
