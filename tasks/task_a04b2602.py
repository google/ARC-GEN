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


def generate(width=None, height=None, colors=None):
  """Returns input and output grids according to the given parameters.

  Args:
    width: Width of the grid.
    height: Height of the grid.
    colors: Colors of the grid.
  """

  def draw():
    grid, output = common.grids(width, height)
    for i, color in enumerate(colors):
      output[i // width][i % width] = grid[i // width][i % width] = color
    outlined = []
    for it in range(2):
      for row in range(height):
        for col in range(width):
          if grid[row][col] != 2: continue
          greens = 0
          if common.get_pixel(grid, row - 1, col) == 3: greens += 1
          if common.get_pixel(grid, row + 1, col) == 3: greens += 1
          if common.get_pixel(grid, row, col - 1) == 3: greens += 1
          if common.get_pixel(grid, row, col + 1) == 3: greens += 1
          if greens < 2: continue
          if it == 0:  # In the first iteration, we draw the blue squares.
            for r in [-1, 0, 1]:
              for c in [-1, 0, 1]:
                common.draw(output, row + r, col + c, 1)
          if it == 1:  # In the second iteration, we redraw the red pixels.
            output[row][col] = 2
            outlined.append((row, col))
    return grid, output, outlined

  if width is None:
    width, height = common.randint(10, 30), common.randint(10, 30)
    num_boxes = common.randint(2, 3)
    while True:
      wides = [common.randint(4, width - 6) for _ in range(num_boxes)]
      talls = [common.randint(4, height - 6) for _ in range(num_boxes)]
      brows = [common.randint(0, height - t) for t in talls]
      bcols = [common.randint(0, width - w) for w in wides]
      if common.overlaps(brows, bcols, wides, talls, 2): continue
      grid = common.grid(width, height)
      for wide, tall, brow, bcol in zip(wides, talls, brows, bcols):
        common.rect(grid, wide, tall, brow, bcol, 3)
      expected_outlined = []
      for r in range(height):
        for c in range(width):
          if common.randint(0, 19): continue
          grid[r][c] = 2
          for wide, tall, brow, bcol in zip(wides, talls, brows, bcols):
            if r >= brow and r < brow + tall and c >= bcol and c < bcol + wide:
              expected_outlined.append((r, c))
      colors = common.flatten(grid)
      _, _, outlined = draw()
      if outlined and outlined == expected_outlined: break

  grid, output, _ = draw()
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(width=20, height=20,
               colors=[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0,
                       0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 3, 3, 3, 3, 3,
                       0, 0, 3, 3, 3, 3, 3, 3, 3, 3, 3, 0, 0, 0, 0, 3, 3, 3, 3, 3,
                       0, 0, 3, 3, 3, 3, 3, 2, 3, 3, 3, 0, 0, 0, 0, 3, 3, 3, 3, 3,
                       0, 0, 2, 3, 3, 3, 3, 3, 3, 2, 3, 0, 0, 0, 2, 3, 3, 2, 3, 3,
                       0, 0, 3, 3, 3, 3, 3, 3, 3, 3, 3, 0, 0, 0, 0, 3, 3, 3, 3, 3,
                       0, 0, 3, 3, 3, 3, 3, 2, 3, 3, 3, 0, 2, 0, 0, 3, 3, 3, 3, 3,
                       0, 0, 3, 3, 3, 3, 3, 3, 3, 3, 3, 0, 0, 0, 0, 3, 3, 3, 3, 3,
                       0, 0, 3, 3, 3, 3, 3, 3, 3, 3, 3, 0, 0, 0, 0, 3, 3, 3, 3, 2,
                       0, 0, 3, 2, 3, 3, 3, 3, 3, 3, 3, 0, 0, 0, 0, 3, 3, 3, 3, 3,
                       0, 0, 3, 3, 3, 3, 3, 2, 3, 3, 3, 0, 0, 2, 0, 2, 3, 3, 3, 3,
                       0, 0, 2, 3, 3, 3, 3, 3, 3, 3, 3, 0, 2, 0, 0, 3, 3, 3, 3, 3,
                       0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 3, 3, 3, 3,
                       0, 0, 0, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 0, 0, 3, 3, 3, 3, 3,
                       0, 0, 0, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 0, 0, 3, 3, 3, 3, 3,
                       0, 2, 0, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 0, 0, 0, 0, 0, 0, 0,
                       0, 0, 0, 3, 3, 3, 3, 3, 3, 2, 3, 3, 3, 0, 2, 0, 0, 0, 0, 0,
                       0, 0, 0, 3, 3, 3, 3, 3, 3, 3, 3, 2, 3, 0, 0, 0, 0, 0, 0, 0,
                       0, 0, 0, 3, 3, 3, 3, 2, 3, 3, 3, 3, 3, 0, 0, 0, 0, 0, 0, 0,
                       0, 0, 0, 3, 3, 3, 3, 3, 3, 3, 2, 3, 3, 0, 0, 0, 0, 0, 0, 0]),
      generate(width=20, height=20,
               colors=[0, 0, 0, 0, 0, 0, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                       0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                       0, 0, 0, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 0, 0, 0, 0, 0,
                       0, 0, 0, 3, 3, 2, 3, 3, 3, 3, 3, 3, 3, 3, 3, 0, 0, 0, 0, 0,
                       0, 0, 0, 3, 3, 3, 3, 3, 3, 3, 2, 3, 3, 3, 3, 0, 0, 0, 0, 0,
                       0, 0, 0, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 2, 0, 0, 0, 0, 0,
                       2, 0, 2, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 0, 0, 0, 0, 0,
                       0, 0, 0, 3, 2, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 0, 0, 0, 0, 0,
                       0, 0, 0, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 0, 2, 0, 0, 0,
                       0, 0, 0, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 0, 0, 0, 0, 0,
                       0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                       0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0,
                       0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                       0, 0, 2, 0, 0, 0, 0, 0, 2, 3, 3, 3, 3, 3, 3, 3, 3, 0, 0, 0,
                       0, 0, 0, 0, 0, 2, 0, 0, 3, 3, 3, 3, 3, 3, 3, 3, 3, 0, 0, 0,
                       0, 0, 0, 0, 0, 0, 2, 0, 3, 3, 3, 3, 3, 3, 3, 3, 2, 0, 0, 0,
                       0, 0, 0, 0, 0, 0, 0, 0, 3, 3, 2, 3, 3, 3, 3, 3, 3, 0, 0, 0,
                       0, 0, 0, 0, 0, 0, 0, 0, 3, 3, 3, 2, 3, 3, 3, 3, 3, 0, 0, 0,
                       0, 0, 0, 0, 0, 2, 0, 0, 3, 3, 3, 3, 3, 3, 3, 3, 3, 0, 0, 0,
                       0, 0, 0, 0, 0, 0, 2, 0, 3, 2, 3, 3, 3, 3, 3, 3, 3, 2, 0, 0]),
      generate(width=17, height=10,
               colors=[0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0,
                       0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0,
                       0, 3, 3, 3, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                       0, 3, 3, 3, 2, 0, 0, 0, 0, 3, 3, 3, 3, 3, 2, 0, 0,
                       0, 3, 3, 3, 3, 0, 0, 0, 0, 3, 3, 3, 3, 3, 3, 0, 0,
                       0, 3, 3, 3, 3, 0, 0, 0, 0, 3, 2, 2, 3, 3, 3, 0, 0,
                       0, 2, 0, 0, 0, 0, 0, 0, 0, 3, 3, 3, 3, 3, 3, 0, 0,
                       0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 3, 3, 3, 3, 3, 0, 0,
                       0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                       0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0]),
  ]
  test = [
      generate(width=27, height=16,
               colors=[0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 3, 3, 3, 2, 3, 3, 3, 3, 3, 3, 3, 3, 0, 0,
                       0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 0, 0,
                       0, 0, 0, 3, 3, 3, 3, 3, 3, 3, 3, 0, 0, 3, 3, 3, 3, 3, 2, 3, 3, 3, 3, 3, 3, 0, 0,
                       0, 0, 0, 3, 3, 3, 3, 3, 3, 3, 2, 0, 0, 3, 3, 3, 2, 3, 3, 3, 3, 3, 3, 3, 3, 0, 2,
                       0, 0, 0, 3, 3, 3, 3, 2, 3, 3, 3, 0, 2, 3, 3, 2, 3, 3, 3, 3, 3, 3, 3, 3, 3, 0, 0,
                       0, 0, 0, 2, 3, 3, 3, 3, 3, 3, 3, 0, 0, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 0, 0,
                       0, 0, 0, 3, 3, 3, 3, 3, 3, 3, 3, 0, 0, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 0, 0,
                       0, 0, 0, 3, 3, 3, 2, 3, 3, 3, 3, 0, 0, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 0, 0,
                       0, 0, 0, 3, 3, 3, 3, 3, 3, 3, 3, 0, 0, 3, 3, 2, 3, 3, 3, 3, 3, 3, 3, 3, 2, 0, 0,
                       0, 0, 0, 3, 3, 2, 2, 3, 3, 3, 3, 0, 0, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 0, 0,
                       0, 0, 0, 3, 3, 3, 3, 3, 3, 3, 3, 0, 0, 0, 0, 0, 0, 0, 2, 2, 0, 0, 0, 0, 0, 0, 0,
                       0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0,
                       0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 3, 3, 3, 3, 3, 3, 3, 3, 0, 0, 0, 0, 0,
                       0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 3, 3, 3, 3, 2, 3, 2, 3, 0, 0, 0, 0, 0,
                       0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 3, 3, 3, 3, 3, 3, 3, 3, 3, 0, 0, 0, 0, 0,
                       0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 2, 0, 2, 3, 2, 2, 3, 3, 3, 3, 3, 0, 0, 0, 2, 0]),
  ]
  return {"train": train, "test": test}
