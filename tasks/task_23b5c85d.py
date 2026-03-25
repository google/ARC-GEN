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


def generate(width=None, height=None, rows=None, cols=None, wides=None,
             talls=None, colors=None):
  """Returns input and output grids according to the given parameters.

  Args:
    width: the width of the (square) grid
    height: the height of the (square) grid
    rows: a list of vertical coordinates where pixels should be placed
    cols: a list of horizontal coordinates where pixels should be placed
    wides: a list of vertical coordinates where pixels should be placed
    talls: a list of horizontal coordinates where pixels should be placed
    colors: a list of digits representing the colors to be used
  """

  def draw(grid, output):
    for row, col, wide, tall, color in zip(rows, cols, wides, talls, colors):
      for r in range(row, row + tall):
        for c in range(col, col + wide):
          grid[r][c] = color
    for r in range(talls[-1]):
      for c in range(wides[-1]):
        output[r][c] = colors[-1]

  if width is None:
    while True:
      width, height = common.randint(10, 20), common.randint(10, 20)
      num_boxes = common.randint(2, 5)
      while True:  # loop until the last box is definitely the smallest
        wides = [common.randint(2, width - 2) for _ in range(num_boxes)]
        talls = [common.randint(2, height - 2) for _ in range(num_boxes)]
        wides.sort(reverse=True)
        talls.sort(reverse=True)
        if talls[-1] != talls[-2] and wides[-1] != wides[-2]: break
      rows = [common.randint(0, height - tall) for tall in talls]
      cols = [common.randint(0, width - wide) for wide in wides]
      colors = common.random_colors(num_boxes)
      # Now, draw the boxes and check that the rarest is indeed the smallest.
      grid = common.grid(width, height)
      output = common.grid(wides[-1], talls[-1])
      draw(grid, output)
      fore = []
      for r in range(height):
        fore.extend(grid[r])
      is_rarest, count = True, len([f for f in fore if f == colors[-1]])
      for color in colors:
        if color == colors[-1]: continue
        if len([f for f in fore if f == color]) <= count: is_rarest = False
      if is_rarest: break

  grid, output = common.grid(width, height), common.grid(wides[-1], talls[-1])
  draw(grid, output)
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(width=10, height=10, rows=[1, 5], cols=[1, 3], wides=[6, 3],
               talls=[6, 3], colors=[2, 8]),
      generate(width=20, height=20, rows=[3, 2, 10, 3, 15],
               cols=[1, 12, 4, 10, 14], wides=[8, 7, 6, 6, 3],
               talls=[9, 7, 5, 4, 2], colors=[3, 8, 2, 4, 1]),
      generate(width=15, height=10, rows=[1, 0, 5], cols=[2, 9, 5],
               wides=[4, 3, 2], talls=[9, 4, 3], colors=[3, 2, 6]),
      generate(width=15, height=13, rows=[2, 9, 4], cols=[1, 6, 3],
               wides=[13, 7, 4], talls=[8, 4, 3], colors=[2, 3, 7]),
      generate(width=15, height=18, rows=[2, 11, 3], cols=[1, 4, 11],
               wides=[8, 7, 2], talls=[7, 4, 2], colors=[1, 6, 4]),
  ]
  test = [
      generate(width=18, height=18, rows=[3, 2, 13, 9], cols=[9, 2, 2, 7],
               wides=[8, 6, 5, 3], talls=[11, 6, 4, 3], colors=[4, 1, 3, 6]),
  ]
  return {"train": train, "test": test}
