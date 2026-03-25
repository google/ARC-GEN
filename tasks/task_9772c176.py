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


def generate(width=None, height=None, wides=None, talls=None, brows=None,
             bcols=None, trims=None):
  """Returns input and output grids according to the given parameters.

  Args:
    width: The width of the grids.
    height: The height of the grids.
    wides: The widths of the rectangles.
    talls: The heights of the rectangles.
    brows: The row indices of the tops of the rectangles.
    bcols: The column indices of the lefts of the rectangles.
    trims: The rows by which to trim the input rectangles.
  """

  def draw():
    if common.overlaps(brows, bcols, wides, talls, 5): return None, None
    grid, output = common.grids(width, height)
    for wide, tall, brow, bcol, trim in zip(wides, talls, brows, bcols, trims):
      common.rect(grid, wide, tall, brow, bcol, 8)
      common.rect(output, wide, tall, brow, bcol, 8)
    # Draw the tops and bots.
      bot, top, left, rite, i = brow, brow + tall - 1, bcol, bcol + wide, 0
      while True:
        bot, top, left, rite = bot - 1, top + 1, left + 1, rite - 1
        if left >= rite: break
        for col in range(left, rite):
          if i < trim:
            common.draw(grid, bot, col, 8)
            common.draw(grid, top, col, 8)
            if common.get_pixel(output, bot, col) in [4, 8]: return None, None
            if common.get_pixel(output, top, col) in [4, 8]: return None, None
            common.draw(output, bot, col, 8)
            common.draw(output, top, col, 8)
          else:
            if common.get_pixel(output, bot, col) in [4, 8]: return None, None
            if common.get_pixel(output, top, col) in [4, 8]: return None, None
            common.draw(output, bot, col, 4)
            common.draw(output, top, col, 4)
        i += 1
      # Draw the lefts and rights.
      bot, top, left, rite = brow, brow + tall, bcol, bcol + wide - 1
      while True:
        bot, top, left, rite = bot + 1, top - 1, left - 1, rite + 1
        if bot >= top: break
        for row in range(bot, top):
          if common.get_pixel(output, row, left) in [4, 8]: return None, None
          if common.get_pixel(output, row, rite) in [4, 8]: return None, None
          common.draw(output, row, left, 4)
          common.draw(output, row, rite, 4)
    return grid, output

  if width is None:
    width, height = common.randint(20, 30), common.randint(20, 30)
    while True:
      wides = [common.randint(5, 2 * width // 3) for _ in range(2)]
      talls = [common.randint(3, height // 2) for _ in range(2)]
      brows = [common.randint(1, height - tall - 1) for tall in talls]
      bcols = [common.randint(1, width - wide - 1) for wide in wides]
      trims = [common.randint(1, (wide - 3) // 2) for wide in wides]
      grid, _ = draw()
      if grid: break

  grid, output = draw()
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(width=21, height=22, wides=[7, 11], talls=[6, 3], brows=[3, 15],
               bcols=[3, 6], trims=[1, 2]),
      generate(width=29, height=26, wides=[17, 7], talls=[8, 3], brows=[3, 19],
               bcols=[1, 14], trims=[4, 2]),
  ]
  test = [
      generate(width=20, height=20, wides=[9, 5], talls=[7, 4], brows=[2, 14],
               bcols=[3, 13], trims=[2, 1]),
  ]
  return {"train": train, "test": test}
