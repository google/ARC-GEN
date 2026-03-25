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


def generate(width=None, height=None, length=None, bgcolor=None, brows=None,
             bcols=None, hiddens=None, colors=None):
  """Returns input and output grids according to the given parameters.

  Args:
    colors: A list of colors to use.
  """

  if width is None:
    length = common.randint(3, 5)
    wide, tall = common.randint(3, 4), common.randint(3, 4)
    width = wide * (length + 1) - 1 + common.randint(0, length)
    height = tall * (length + 1) - 1 + common.randint(0, length)
    num_boxes = 1
    if max(wide, tall) == 4: num_boxes = common.randint(1, 2)
    if min(wide, tall) == 4: num_boxes = common.randint(2, 3)
    while True:
      brows = [common.randint(0, tall - 2) for _ in range(num_boxes)]
      bcols = [common.randint(0, wide - 2) for _ in range(num_boxes)]
      if not common.overlaps(brows, bcols, [2] * num_boxes, [2] * num_boxes):
        break
    bgcolor = common.random_color()
    subset = common.random_colors(num_boxes, exclude=[bgcolor])
    hiddens = [common.randint(0, 3) for _ in range(num_boxes)]
    colors = []
    for i in range(num_boxes):
      pixels = common.diagonally_connected_sprite(common.randint(3, length),
                                                  common.randint(3, length),
                                                  length)
      for r in range(length):
        for c in range(length):
          colors.append(subset[i] if (r, c) in pixels else 0)

  grid, output = common.grids(width, height)
  for r in range(height):
    for c in range(length, width, length + 1):
      output[r][c] = grid[r][c] = bgcolor
  for r in range(length, height, length + 1):
    for c in range(width):
      output[r][c] = grid[r][c] = bgcolor
  for i, (brow, bcol, hidden) in enumerate(zip(brows, bcols, hiddens)):
    for row in range(length):
      for col in range(length):
        color = int(colors[i * length * length + row * length + col])
        r = brow * (length + 1) + length + row + 1
        c = bcol * (length + 1) + length + col + 1
        output[r][c] = color
        if hidden != 3: grid[r][c] = color
        r = brow * (length + 1) + length + row + 1
        c = bcol * (length + 1) + length - col - 1
        output[r][c] = color
        if hidden != 2: grid[r][c] = color
        r = brow * (length + 1) + length - row - 1
        c = bcol * (length + 1) + length + col + 1
        output[r][c] = color
        if hidden != 1: grid[r][c] = color
        r = brow * (length + 1) + length - row - 1
        c = bcol * (length + 1) + length - col - 1
        output[r][c] = color
        if hidden != 0: grid[r][c] = color
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(width=18, height=19, length=4, bgcolor=2, brows=[0, 2],
               bcols=[0, 1], hiddens=[1, 2],
               colors="03000330330300000100110000100000"),
      generate(width=19, height=17, length=4, bgcolor=6, brows=[1], bcols=[1],
               hiddens=[3], colors="0400044004004000"),
  ]
  test = [
      generate(width=23, height=26, length=5, bgcolor=8, brows=[0, 1, 2],
               bcols=[0, 2, 0], hiddens=[3, 1, 2],
               colors="020002220000200000000000001000101000110000000000000400044400000000000000000"),
  ]
  return {"train": train, "test": test}
