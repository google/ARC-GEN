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
    width: The width of the grid.
    height: The height of the grid.
    colors: The colors of the pixels.
  """

  if width is None:
    while True:
      width = common.randint(5, 9)
      height = width + common.randint(0, 2) - 1
      while True:
        row, rows, talls = common.randint(0, 4), [], []
        while True:
          tall = common.randint(2, 4)
          if row + tall >= height: break
          rows.append(row)
          talls.append(tall)
          row += tall + common.randint(1, 2)
        if talls: break
      wides = [common.randint(1, 2) for _ in talls]
      while True:
        pixels = common.random_pixels(width, height)
        if pixels: break
      colors = [0] * (width * height)
      for pixel in pixels:
        r, c = pixel
        colors[r * width + c] = 8
      good = False  # at least one green strip should move left.
      for wide, tall, row in zip(wides, talls, rows):
        for r in range(row, row + tall):
          if colors[r * width + width - wide - 1] == 0: good = True
          for c in range(width - wide, width):
            colors[r * width + c] = 3
      if good: break

  grid, output = common.grids(width, height)
  for i, color in enumerate(colors):
    output[i // width][i % width] = grid[i // width][i % width] = color
  for row in range(height):
    col = width - 1
    if output[row][col] != 3: continue
    while output[row][col] == 3:
      col -= 1
    while col >= 0 and output[row][col] == 0:
      for c in range(col, width):
        output[row][c] = output[row][c + 1] if c + 1 < width else 0
      col -= 1
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(width=8, height=7, colors=[0, 0, 0, 8, 0, 0, 8, 3,
                                          0, 8, 0, 0, 8, 0, 0, 3,
                                          8, 8, 0, 8, 0, 0, 8, 3,
                                          8, 8, 0, 0, 0, 0, 0, 3,
                                          0, 0, 0, 8, 8, 0, 0, 8,
                                          8, 0, 0, 0, 0, 0, 0, 0,
                                          0, 0, 0, 8, 8, 8, 0, 0]),
      generate(width=6, height=7, colors=[0, 0, 0, 8, 0, 0,
                                          0, 0, 8, 0, 0, 8,
                                          8, 0, 0, 0, 0, 8,
                                          0, 0, 8, 0, 8, 0,
                                          0, 0, 0, 0, 3, 3,
                                          8, 0, 8, 0, 3, 3,
                                          0, 8, 0, 8, 8, 0]),
      generate(width=8, height=9, colors=[0, 0, 0, 0, 8, 8, 8, 8,
                                          0, 0, 0, 8, 0, 8, 3, 3,
                                          8, 0, 0, 8, 0, 0, 3, 3,
                                          8, 8, 0, 0, 0, 0, 3, 3,
                                          8, 8, 0, 0, 8, 8, 0, 8,
                                          0, 0, 0, 8, 0, 8, 0, 3,
                                          0, 8, 0, 0, 0, 0, 0, 3,
                                          0, 0, 0, 8, 8, 0, 8, 3,
                                          8, 0, 0, 8, 8, 8, 0, 8]),
  ]
  test = [
      generate(width=9, height=9, colors=[0, 8, 8, 8, 8, 8, 8, 0, 8,
                                          8, 8, 8, 0, 0, 8, 8, 0, 8,
                                          0, 8, 8, 0, 8, 8, 0, 0, 8,
                                          0, 8, 0, 0, 0, 0, 0, 3, 3,
                                          0, 8, 0, 8, 0, 0, 0, 3, 3,
                                          8, 0, 0, 0, 0, 0, 0, 3, 3,
                                          0, 0, 8, 0, 8, 8, 0, 3, 3,
                                          0, 8, 8, 8, 0, 0, 0, 0, 0,
                                          0, 8, 0, 8, 0, 8, 8, 8, 0]),
  ]
  return {"train": train, "test": test}
