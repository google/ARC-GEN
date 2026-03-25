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


def generate(size=None, length=None, icolor=None, ocolor=None, brows=None,
             bcols=None, bcolors=None, colors=None):
  """Returns input and output grids according to the given parameters.

  Args:
    size: The size of the input grid.
    length: The length of the output grid.
    icolor: The background color of the input grid.
    ocolor: The background color of the output grid.
    brows: The rows of the boxes.
    bcols: The columns of the boxes.
    bcolors: The colors of the input boxes.
    colors: The colors of the output grid.
  """

  if size is None:
    length = common.randint(4, 6)
    size, num_boxes = length * 2 + 6, length - 2
    icolor = common.random_color()
    ocolor = common.random_color(exclude=[icolor])
    bcolors = common.random_colors(num_boxes, exclude=[icolor, ocolor])
    colors = [ocolor] * (length * length)
    while True:
      brows = [common.randint(1, size - length - 1) for _ in range(num_boxes)]
      bcols = [common.randint(1, size - length - 1) for _ in range(num_boxes)]
      if not common.overlaps(brows, bcols, [length] * num_boxes, [length] * num_boxes, 1):
        break
    while True:
      slen = common.randint(1, length - 2)
      soff = common.randint(1, length - slen - 1)
      spos = common.randint(1, length - 2)
      sdir = common.randint(0, 1)
      scolor = common.choice(bcolors + [ocolor])
      for val in range(soff, soff + slen):
        if sdir: colors[val * length + spos] = scolor
        else: colors[spos * length + val] = scolor
      if len(set(colors)) != num_boxes + 1: continue
      good = True
      for bcolor in bcolors:
        pixels = [(r, c) for r in range(length) for c in range(length) if colors[r * length + c] == bcolor]
        if not common.connected(pixels): good = False
      if good: break

  grid, output = common.grid(size, size, icolor), common.grid(length, length)
  for brow, bcol, bcolor in zip(brows, bcols, bcolors):
    for row in range(length):
      for col in range(length):
        color = colors[row * length + col]
        grid[brow + row][bcol + col] = color if color == bcolor else ocolor
  for r in range(length):
    for c in range(length):
      output[r][c] = colors[r * length + c]
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(size=14, length=4, icolor=2, ocolor=3, brows=[2, 7],
               bcols=[1, 7], bcolors=[1, 6],
               colors=[3, 3, 3, 3, 3, 6, 6, 3, 3, 6, 1, 3, 3, 3, 3, 3]),
      generate(size=16, length=5, icolor=8, ocolor=2, brows=[1, 3, 8],
               bcols=[2, 10, 3], bcolors=[1, 4, 3],
               colors=[2, 2, 2, 2, 2, 2, 1, 1, 4, 2, 2, 1, 2, 4, 2, 2, 3, 3, 3, 2, 2, 2, 2, 2, 2]),
  ]
  test = [
      generate(size=18, length=6, icolor=4, ocolor=3, brows=[1, 2, 9, 10],
               bcols=[8, 1, 2, 10], bcolors=[5, 2, 8, 1],
               colors=[3, 3, 3, 3, 3, 3, 3, 3, 2, 3, 1, 3, 3, 2, 2, 3, 3, 3, 3, 5, 5, 8, 8, 3, 3, 5, 5, 8, 3, 3, 3, 3, 3, 3, 3, 3]),
  ]
  return {"train": train, "test": test}
