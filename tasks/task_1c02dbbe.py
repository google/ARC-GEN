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


def generate(width=None, height=None, brow=None, bcol=None, widths=None,
             heights=None, colors=None):
  """Returns input and output grids according to the given parameters.

  Args:
    width: The width of the input grid.
    height: The height of the input grid.
    brow: The row of the grey box.
    bcol: The column of the grey box.
    widths: The widths of the boxes in the output grid.
    heights: The heights of the boxes in the output grid.
    colors: The colors of the boxes in the output grid.
  """

  def draw():
    grid, output = common.grids(15, 15)
    common.rect(grid, width, height, brow, bcol, 5)
    common.rect(output, width, height, brow, bcol, 5)
    for i in range(len(widths)):
      # Draw the input dots.
      w, h, r, c, color = widths[i], heights[i], brow, bcol, colors[i]
      if not color: continue
      if i in [1, 3]: c += width - 1
      if i in [2, 3]: r += height - 1
      grid[r][c] = color
      cc = c + (1 if i in [1, 3] else -1)
      rr = r + (1 if i in [0, 1] else -1) * (h - 1)
      grid[rr][cc] = color
      cc = c + (1 if i in [0, 2] else -1) * (w - 1)
      rr = r + (1 if i in [2, 3] else -1)
      grid[rr][cc] = color
      # Draw the output rectangles.
      w, h, r, c, color = widths[i], heights[i], brow, bcol, colors[i]
      if i in [1, 3]: c += width - w
      if i in [2, 3]: r += height - h
      for row in range(h):
        for col in range(w):
          if output[row + r][col + c] != 5: return None, None
          output[row + r][col + c] = color
    return grid, output

  if width is None:
    width, height = common.randint(11, 13), common.randint(11, 13)
    brow = common.randint(1, 15 - height - 1)
    bcol = common.randint(1, 15 - width - 1)
    while True:
      colors = common.random_colors(4, exclude=[5])
      for i in range(4):
        if common.randint(0, 1): colors[i] = 0
      if sum(colors) > 0: break
    while True:
      widths = [common.randint(1, 8) for _ in range(4)]
      heights = [common.randint(1, 8) for _ in range(4)]
      grid, _ = draw()
      if grid: break

  grid, output = draw()
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(width=11, height=11, brow=2, bcol=2, widths=[7, 0, 0, 5],
               heights=[5, 0, 0, 6], colors=[3, 0, 0, 4]),
      generate(width=10, height=10, brow=3, bcol=3, widths=[6], heights=[7],
               colors=[2]),
      generate(width=12, height=13, brow=1, bcol=2, widths=[5, 4, 4],
               heights=[4, 7, 6], colors=[1, 4, 6]),
  ]
  test = [
      generate(width=13, height=13, brow=1, bcol=1, widths=[4, 7, 8, 3],
               heights=[7, 5, 4, 6], colors=[6, 1, 7, 3]),
  ]
  return {"train": train, "test": test}
