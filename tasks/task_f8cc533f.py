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


def generate(width=None, height=None, length=None, brows=None, bcols=None,
             bcolors=None, colors=None):
  """Returns input and output grids according to the given parameters.

  Args:
    width: The width of the grid.
    height: The height of the grid.
    length: The length of the pattern.
    brows: The rows of the boxes.
    bcols: The columns of the boxes.
    bcolors: The colors of the boxes.
    colors: The colors of the input grid.
  """

  def draw():
    grid, output = common.grids(width, height)
    for i, color in enumerate(colors):
      output[i // width][i % width] = grid[i // width][i % width] = color
    pattern = common.grid(length, length)
    for brow, bcol, bcolor in zip(brows, bcols, bcolors):
      for row in range(length):
        for col in range(length):
          if grid[brow + row][bcol + col] == bcolor:
            pattern[row][col] = 1
    for brow, bcol, bcolor in zip(brows, bcols, bcolors):
      some_missing = False
      for row in range(length):
        for col in range(length):
          if not pattern[row][col]: continue
          if output[brow + row][bcol + col] != bcolor: some_missing = True
          output[brow + row][bcol + col] = bcolor
      if not some_missing: return None, None
    return grid, output

  if width is None:
    length = common.randint(5, 7)
    bgcolor = common.random_color()
    num_boxes = common.randint(2, 4)
    bcolors = common.random_colors(num_boxes, exclude=[bgcolor])
    while True:
      width, height = common.randint(10, 22), common.randint(10, 22)
      if width * height < 11 * 19: continue
      # Choose the locations of the boxes.
      brows = [common.randint(0, height - length) for _ in range(num_boxes)]
      bcols = [common.randint(0, width - length) for _ in range(num_boxes)]
      lengths = [length] * num_boxes
      if common.overlaps(brows, bcols, lengths, lengths, 1): continue
      # Create a fully symmetric pattern.
      pattern = common.grid(length, length)
      for row in range(length):
        for col in range(length):
          if common.randint(0, 9): continue
          for r, c in [(row, col), (col, row)]:
            pattern[r][c] = 1
            pattern[r][length - 1 - c] = 1
            pattern[length - 1 - r][c] = 1
            pattern[length - 1 - r][length - 1 - c] = 1
      if len(set(common.flatten(pattern))) != 2: continue
      # Create the input.
      grid, expected = common.grids(width, height, bgcolor)
      for brow, bcol, bcolor in zip(brows, bcols, bcolors):
        for row in range(length):
          for col in range(length):
            if not pattern[row][col]: continue
            expected[brow + row][bcol + col] = bcolor
            if common.randint(0, 9): grid[brow + row][bcol + col] = bcolor
      colors = common.flatten(grid)
      # Finally, check that we can faithfully construct the pattern.
      grid, output = draw()
      if grid and expected == output: break

  grid, output = draw()
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(width=19, height=19, length=5, brows=[2, 2, 10, 11],
               bcols=[3, 11, 1, 11], bcolors=[8, 4, 2, 1],
               colors=[3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3,
                       3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3,
                       3, 3, 3, 3, 8, 8, 3, 3, 3, 3, 3, 3, 3, 4, 4, 3, 3, 3, 3,
                       3, 3, 3, 3, 8, 3, 8, 3, 3, 3, 3, 4, 4, 3, 3, 3, 3, 3, 3,
                       3, 3, 3, 8, 3, 3, 3, 8, 3, 3, 3, 4, 3, 3, 3, 4, 3, 3, 3,
                       3, 3, 3, 8, 8, 3, 8, 8, 3, 3, 3, 4, 4, 3, 4, 4, 3, 3, 3,
                       3, 3, 3, 3, 8, 3, 8, 3, 3, 3, 3, 3, 4, 4, 4, 3, 3, 3, 3,
                       3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3,
                       3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3,
                       3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3,
                       3, 3, 2, 2, 2, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3,
                       3, 2, 2, 3, 3, 2, 3, 3, 3, 3, 3, 3, 1, 3, 1, 3, 3, 3, 3,
                       3, 2, 3, 3, 3, 2, 3, 3, 3, 3, 3, 1, 1, 3, 1, 1, 3, 3, 3,
                       3, 2, 3, 3, 2, 2, 3, 3, 3, 3, 3, 1, 3, 3, 3, 1, 3, 3, 3,
                       3, 3, 2, 2, 2, 3, 3, 3, 3, 3, 3, 1, 1, 3, 1, 1, 3, 3, 3,
                       3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 1, 1, 3, 3, 3, 3, 3,
                       3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3,
                       3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3,
                       3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3]),
      generate(width=19, height=11, length=6, brows=[1, 5], bcols=[9, 1],
               bcolors=[4, 1],
               colors=[2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2,
                       2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 4, 2, 2, 4, 2, 2, 2, 2, 2,
                       2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 4, 4, 4, 4, 2, 2, 2, 2,
                       2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 4, 2, 2, 4, 2, 2, 2, 2, 2,
                       2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 4, 2, 2, 2, 2, 2,
                       2, 2, 1, 2, 2, 2, 2, 2, 2, 4, 4, 4, 4, 4, 2, 2, 2, 2, 2,
                       2, 1, 1, 1, 1, 2, 1, 2, 2, 2, 4, 2, 2, 4, 2, 2, 2, 2, 2,
                       2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2,
                       2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2,
                       2, 2, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2,
                       2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2]),
      generate(width=19, height=11, length=5, brows=[1, 1, 4], bcols=[2, 14, 8],
               bcolors=[3, 8, 2],
               colors=[4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4,
                       4, 4, 4, 4, 4, 3, 4, 4, 4, 4, 4, 4, 4, 4, 4, 8, 4, 8, 4,
                       4, 4, 3, 3, 4, 3, 3, 4, 4, 4, 4, 4, 4, 4, 8, 8, 4, 8, 4,
                       4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4,
                       4, 4, 3, 3, 4, 3, 3, 4, 4, 2, 4, 2, 4, 4, 8, 8, 4, 4, 4,
                       4, 4, 4, 3, 4, 3, 4, 4, 2, 2, 4, 2, 4, 4, 4, 8, 4, 4, 4,
                       4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4,
                       4, 4, 4, 4, 4, 4, 4, 4, 2, 2, 4, 4, 2, 4, 4, 4, 4, 4, 4,
                       4, 4, 4, 4, 4, 4, 4, 4, 4, 2, 4, 2, 4, 4, 4, 4, 4, 4, 4,
                       4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4,
                       4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4]),
  ]
  test = [
      generate(width=18, height=20, length=5, brows=[2, 7, 11],
               bcols=[3, 10, 1], bcolors=[2, 3, 1],
               colors=[4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4,
                       4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4,
                       4, 4, 4, 2, 2, 2, 2, 2, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4,
                       4, 4, 4, 2, 4, 2, 4, 2, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4,
                       4, 4, 4, 2, 2, 2, 2, 2, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4,
                       4, 4, 4, 4, 4, 2, 4, 2, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4,
                       4, 4, 4, 2, 2, 2, 2, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4,
                       4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 3, 3, 3, 4, 3, 4, 4, 4,
                       4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 3, 4, 3, 4, 3, 4, 4, 4,
                       4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 3, 4, 4, 4, 4, 4, 4, 4,
                       4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 3, 4, 3, 4, 4, 4,
                       4, 1, 4, 4, 1, 1, 4, 4, 4, 4, 3, 3, 3, 3, 3, 4, 4, 4,
                       4, 1, 4, 1, 4, 1, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4,
                       4, 1, 1, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4,
                       4, 1, 4, 1, 4, 1, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4,
                       4, 1, 1, 1, 1, 1, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4,
                       4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4,
                       4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4,
                       4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4,
                       4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4]),
      generate(width=22, height=22, length=7, brows=[1, 2, 10, 13],
               bcols=[1, 11, 3, 13], bcolors=[1, 6, 4, 3],
               colors=[8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8,
                       8, 8, 8, 1, 1, 1, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8,
                       8, 8, 8, 1, 8, 8, 1, 8, 8, 8, 8, 8, 8, 6, 6, 6, 8, 8, 8, 8, 8, 8,
                       8, 1, 1, 1, 8, 1, 1, 1, 8, 8, 8, 8, 6, 6, 8, 8, 6, 8, 8, 8, 8, 8,
                       8, 1, 8, 8, 1, 8, 8, 1, 8, 8, 8, 6, 6, 6, 8, 6, 6, 6, 8, 8, 8, 8,
                       8, 1, 1, 1, 8, 1, 1, 1, 8, 8, 8, 6, 8, 8, 8, 8, 8, 6, 8, 8, 8, 8,
                       8, 8, 1, 1, 8, 1, 1, 8, 8, 8, 8, 8, 8, 6, 8, 6, 6, 6, 8, 8, 8, 8,
                       8, 8, 8, 8, 1, 1, 8, 8, 8, 8, 8, 8, 6, 6, 8, 6, 6, 8, 8, 8, 8, 8,
                       8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 6, 8, 8, 8, 8, 8, 8, 8, 8,
                       8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8,
                       8, 8, 8, 8, 8, 4, 4, 4, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8,
                       8, 8, 8, 8, 4, 4, 8, 4, 4, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8,
                       8, 8, 8, 4, 4, 4, 8, 4, 4, 4, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8,
                       8, 8, 8, 8, 8, 8, 4, 8, 8, 4, 8, 8, 8, 8, 8, 3, 3, 3, 8, 8, 8, 8,
                       8, 8, 8, 4, 4, 4, 8, 4, 4, 4, 8, 8, 8, 8, 3, 3, 8, 8, 8, 8, 8, 8,
                       8, 8, 8, 8, 4, 4, 8, 4, 8, 8, 8, 8, 8, 3, 3, 3, 8, 8, 3, 3, 8, 8,
                       8, 8, 8, 8, 8, 4, 4, 4, 8, 8, 8, 8, 8, 3, 8, 8, 3, 8, 8, 3, 8, 8,
                       8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 3, 3, 3, 8, 3, 3, 3, 8, 8,
                       8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 3, 8, 8, 3, 8, 8, 8,
                       8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 3, 3, 8, 8, 8, 8, 8,
                       8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8,
                       8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8]),
  ]
  return {"train": train, "test": test}
