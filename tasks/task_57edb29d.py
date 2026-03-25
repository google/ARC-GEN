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
             bcols=None, colors=None, pattern=None):
  """Returns input and output grids according to the given parameters.

  Args:
    width: The width of the input grid.
    height: The height of the input grid.
    wides: The widths of the boxes.
    talls: The heights of the boxes.
    brows: The rows of the boxes.
    bcols: The columns of the boxes.
    colors: The colors of the boxes.
    pattern: The colors in the pattern.
  """

  if width is None:
    num_boxes = common.randint(3, 6)
    pcolor = common.random_color(exclude=[4])
    while True:
      width, height = 2 * common.randint(9, 14), 2 * common.randint(9, 14)
      wides = [common.randint(5, width // 3) for _ in range(num_boxes)]
      talls = [common.randint(5, height // 3) for _ in range(num_boxes)]
      if common.randint(0, 1): talls[-1] = common.randint(5, height - 2)
      if common.randint(0, 1): wides[-2] = common.randint(5, width - 2)
      brows = [common.randint(1, height - tall - 1) for tall in talls]
      bcols = [common.randint(1, width - wide - 1) for wide in wides]
      if common.overlaps(brows, bcols, wides, talls, 1): continue
      if max(wides[1:]) >= 7 and max(talls[1:]) >= 7: break
    colors = common.random_colors(num_boxes, exclude=[4, pcolor])
    pattern = [0, 0, pcolor, 0, 0]
    if common.randint(0, 1):
      pattern[1] = pcolor
      if common.randint(0, 1): pattern[0] = pcolor
    if common.randint(0, 1):
      pattern[3] = pcolor
      if common.randint(0, 1): pattern[4] = pcolor

  grid = common.grid(width, height, 4)
  output = common.grid(wides[0], talls[0], colors[0])
  for i, (wide, tall, brow, bcol, color) in enumerate(zip(wides, talls, brows, bcols, colors)):
    common.rect(grid, wide, tall, brow, bcol, color)
    if pattern[0]:
      for r in range(1, tall - 1):
        if i: grid[brow + r][bcol + 1] = grid[brow + r][bcol + wide - 2] = pattern[0]
        else: output[r][1] = output[r][wide - 2] = pattern[0]
    if pattern[1]:
      for r, c in [(2, 1), (2, wide - 2), (tall - 3, 1), (tall - 3, wide - 2)]:
        if i: grid[brow + r][bcol + c] = pattern[1]
        else: output[r][c] = pattern[1]
    if pattern[2]:
      for r, c in [(1, 1), (1, wide - 2), (tall - 2, 1), (tall - 2, wide - 2)]:
        if i: grid[brow + r][bcol + c] = pattern[2]
        else: output[r][c] = pattern[2]
    if pattern[3]:
      for r, c in [(1, 2), (1, wide - 3), (tall - 2, 2), (tall - 2, wide - 3)]:
        if i: grid[brow + r][bcol + c] = pattern[3]
        else: output[r][c] = pattern[3]
    if pattern[4]:
      for c in range(1, wide - 1):
        if i: grid[brow + 1][bcol + c] = grid[brow + tall - 2][bcol + c] = pattern[4]
        else: output[1][c] = output[tall - 2][c] = pattern[4]
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(width=24, height=20, wides=[7, 5, 6, 8], talls=[5, 18, 6, 9],
               brows=[14, 1, 3, 10], bcols=[7, 1, 12, 15], colors=[3, 2, 1, 8],
               pattern=[0, 0, 5, 5, 5]),
      generate(width=20, height=22, wides=[12, 5, 5], talls=[20, 8, 8],
               brows=[1, 1, 13], bcols=[7, 1, 1], colors=[8, 2, 3],
               pattern=[0, 0, 7, 0, 0]),
      generate(width=20, height=20, wides=[6, 18, 5, 5], talls=[10, 7, 10, 10],
               brows=[9, 1, 9, 9], bcols=[13, 1, 1, 7], colors=[1, 3, 2, 8],
               pattern=[0, 6, 6, 6, 0]),
  ]
  test = [
      generate(width=28, height=28, wides=[5, 10, 15, 10, 9, 15],
               talls=[9, 7, 7, 18, 9, 8], brows=[9, 1, 1, 9, 9, 19],
               bcols=[22, 1, 12, 1, 12, 12], colors=[9, 1, 3, 2, 8, 7],
               pattern=[0, 5, 5, 0, 0]),
  ]
  return {"train": train, "test": test}
