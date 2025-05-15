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


def generate(width=None, height=None, rows=None, cols=None, srow=None,
             scol=None, smag=None, brow=None, bcol=None, colors=None,
             scolor=None, size=None):
  """Returns input and output grids according to the given parameters.

  Args:
    width: the width of the input grid
    height: the height of the input grid
    rows: a list of vertical coordinates where pixels should be placed
    cols: a list of horizontal coordinates where pixels should be placed
    srow: the row of the sprite
    scol: the column of the sprite
    smag: the magnification of the sprite
    brow: the row of the color box
    bcol: the column of the color box
    colors: a list of digits representing the colors to be used
    scolor: the color of the sprite
    size: the size of the sprite
  """

  def draw(grid, output):
    # Draw the megasprite and the output sprite.
    for r, c in zip(rows, cols):
      output[r][c] = colors[r * size + c]
      for dr in range(smag):
        for dc in range(smag):
          grid[srow + smag * r + dr][scol + smag * c + dc] = scolor
    # Check that we're not touching the sprite.
    for r in range(size):
      for c in range(size):
        for dr in [-1, 0, 1]:
          for dc in [-1, 0, 1]:
            if common.get_pixel(grid, brow + r + dr, bcol + c + dc) > 0:
              return False
    # Draw the little color box.
    for r in range(size):
      for c in range(size):
        grid[brow + r][bcol + c] = colors[r * size + c]
    return True

  if width is None:
    while True:
      width, height = common.randint(21, 28), common.randint(21, 28)
      size = common.randint(3, 4)
      smag = common.randint(3, 5 if size < 4 else 4)
      srow, scol = 1, common.randint(1, width - size * smag - 1)
      brow = height - size - 1
      bcol = common.randint(width // 2, width - size - 1)
      rows, cols = common.conway_sprite(size, size)
      if not common.diagonally_connected(list(zip(rows, cols))): continue
      colors = [common.random_color() for _ in range(size * size)]
      scolor = common.random_color()
      grid, output = common.grid(width, height), common.grid(size, size)
      if draw(grid, output): break

  grid, output = common.grid(width, height), common.grid(size, size)
  draw(grid, output)
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(width=21, height=27, rows=[0, 0, 1, 2, 2], cols=[0, 2, 1, 0, 2],
               srow=1, scol=1, smag=5, brow=19, bcol=7,
               colors=[3, 1, 7, 2, 8, 9, 3, 4, 6], scolor=1, size=3),
      generate(width=25, height=27, rows=[0, 0, 1, 1, 2, 2],
               cols=[0, 2, 0, 1, 1, 2], srow=3, scol=9, smag=3, brow=19, bcol=8,
               colors=[2, 1, 7, 4, 8, 9, 8, 6, 1], scolor=3, size=3),
      generate(width=22, height=22, rows=[0, 0, 0, 1, 1, 2, 2, 3, 3, 3],
               cols=[0, 2, 3, 0, 2, 0, 3, 0, 1, 2], srow=1, scol=2, smag=4,
               brow=16, bcol=17,
               colors=[4, 1, 9, 4, 6, 3, 6, 1, 3, 5, 7, 5, 2, 4, 2, 7],
               scolor=8, size=4),
  ]
  test = [
      generate(width=24, height=21, rows=[0, 0, 0, 1, 1, 2, 2, 2, 2, 3, 3],
               cols=[0, 2, 3, 1, 2, 0, 1, 2, 3, 0, 3], srow=1, scol=2, smag=3,
               brow=15, bcol=15,
               colors=[4, 8, 6, 3, 9, 3, 3, 5, 6, 7, 7, 4, 1, 5, 8, 1],
               scolor=2, size=4),
  ]
  return {"train": train, "test": test}
