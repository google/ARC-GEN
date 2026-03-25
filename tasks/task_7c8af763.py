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


def generate(wides=None, talls=None, rows=None, cols=None, colors=None):
  """Returns input and output grids according to the given parameters.

  Args:
    wides: widths of the boxes.
    talls: heights of the boxes.
    rows: rows of the pixels.
    cols: cols of the pixels.
    colors: colors of the pixels.
  """

  def draw(just_lines=False):
    nonlocal wides, talls, rows, cols, colors
    grid, output = common.grids(10, 10)
    # Draw the horizontal gray lines.
    r = 0
    for tall in [0] + talls:
      r += tall
      for c in range(10):
        output[r][c] = grid[r][c] = 5
      r += 1
    # Draw the vertical gray lines.
    c = 0
    for wide in wides:
      c += wide
      if c >= 10: break
      for r in range(10):
        output[r][c] = grid[r][c] = 5
      c += 1
    if just_lines: return grid, output
    # Draw the pixels.
    for row, col, color in zip(rows, cols, colors):
      output[row][col] = grid[row][col] = color
    # Figure out the max values.
    row = 0
    for tall in talls:
      col = -1
      for wide in wides:
        num_red, num_blue = 0, 0
        for r in range(tall + 2):
          for c in range(wide + 2):
            color = common.get_pixel(output, row + r, col + c)
            if color == 1: num_blue += 1
            if color == 2: num_red += 1
        if num_red == num_blue:
          return None, None
        if num_red > num_blue:
          common.rect(output, wide, tall, row + 1, col + 1, 2)
        elif num_blue > num_red:
          common.rect(output, wide, tall, row + 1, col + 1, 1)
        col += wide + 1
      row += tall + 1
    return grid, output

  if wides is None:
    while True:
      wides = common.choices([2, 3, 4], k=common.randint(2, 3))
      if sum(wides) + len(wides) - 1 == 10: break
    while True:
      talls = common.choices([2, 3, 4], k=common.randint(2, 3))
      if sum(talls) + len(talls) + 1 == 10: break
    while True:
      grid, _ = draw(True)
      rows, cols, colors = [], [], []
      for r in range(10):
        for c in range(10):
          if grid[r][c] != 5: continue
          neighbors = []
          neighbors.append(common.get_pixel(grid, r - 1, c))
          neighbors.append(common.get_pixel(grid, r + 1, c))
          neighbors.append(common.get_pixel(grid, r, c - 1))
          neighbors.append(common.get_pixel(grid, r, c + 1))
          if neighbors.count(5) >= 3: continue
          if common.randint(0, 3) != 0: continue
          rows.append(r)
          cols.append(c)
          colors.append(common.randint(1, 2))
      grid, _ = draw()
      if grid: break

  grid, output = draw()
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(wides=[2, 4, 2], talls=[4, 3],
               rows=[0, 0, 0, 2, 2, 5, 5, 5, 7, 9, 9, 9],
               cols=[0, 4, 9, 2, 7, 1, 5, 9, 7, 0, 4, 9],
               colors=[2, 1, 2, 1, 1, 1, 2, 1, 2, 1, 2, 1]),
      generate(wides=[3, 3, 2], talls=[3, 4],
               rows=[0, 0, 0, 0, 2, 4, 4, 6, 9, 9, 9],
               cols=[0, 2, 5, 9, 7, 1, 8, 3, 1, 6, 9],
               colors=[1, 1, 2, 1, 2, 2, 2, 1, 2, 1, 2]),
      generate(wides=[3, 2, 3], talls=[2, 2, 2],
               rows=[0, 0, 0, 0, 1, 3, 3, 3, 4, 5, 6, 6, 6, 6, 7, 9, 9, 9],
               cols=[0, 2, 4, 9, 6, 1, 5, 8, 6, 3, 0, 1, 4, 8, 6, 2, 5, 8],
               colors=[1, 2, 2, 1, 2, 2, 1, 2, 2, 1, 2, 2, 1, 1, 1, 1, 1, 2]),
  ]
  test = [
      generate(wides=[2, 2, 4], talls=[2, 2, 2],
               rows=[0, 0, 2, 3, 3, 3, 4, 4, 6, 6, 6, 6, 7, 7, 9, 9, 9],
               cols=[1, 8, 5, 4, 7, 8, 2, 5, 0, 4, 7, 8, 2, 5, 1, 6, 9],
               colors=[1, 1, 1, 1, 2, 1, 2, 2, 2, 2, 1, 2, 1, 2, 2, 1, 1]),
  ]
  return {"train": train, "test": test}
