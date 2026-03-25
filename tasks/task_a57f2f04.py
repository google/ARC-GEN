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
             bcols=None, lengths=None, depths=None, lefts=None, tops=None,
             patterns=None):
  """Returns input and output grids according to the given parameters.

  Args:
    width: The width of the grids.
    height: The height of the grids.
    wides: The widths of the rectangles.
    talls: The heights of the rectangles.
    brows: The row offsets of the rectangles.
    bcols: The column offsets of the rectangles.
    lengths: The lengths of the patterns.
    depths: The depths of the patterns.
    lefts: Whether the patterns are left-aligned.
    tops: Whether the patterns are top-aligned.
    patterns: The patterns to use.
  """

  if width is None:
    width, height = common.randint(12, 30), common.randint(12, 30)
    num_boxes = 1
    if width * height >= 250: num_boxes = 2
    if width * height >= 500: num_boxes = 3
    if width * height >= 750: num_boxes = 4
    bcolors = common.sample([1, 2, 3, 4], num_boxes)
    lefts = [common.randint(0, 1) for _ in range(num_boxes)]
    tops = [common.randint(0, 1) for _ in range(num_boxes)]
    while True:
      lengths = [common.randint(2, 5) for _ in range(num_boxes)]
      depths = [common.randint(2, 5) for _ in range(num_boxes)]
      wides = [wide * common.randint(2, 5) for wide in lengths]
      talls = [tall * common.randint(2, 5) for tall in depths]
      if max(wides) + 4 > width or max(talls) + 4 > height: continue
      brows = [common.randint(2, height - tall - 2) for tall in talls]
      bcols = [common.randint(2, width - wide - 2) for wide in wides]
      if not common.overlaps(brows, bcols, wides, talls, 2): break
    patterns = ""
    for depth, length, bcolor in zip(depths, lengths, bcolors):
      pixels = common.diagonally_connected_sprite(length, depth, length + depth)
      grid = common.grid(length, depth)
      for row in range(depth):
        for col in range(length):
          if (row, col) in pixels: grid[row][col] = bcolor
      patterns += "".join(str(x) for x in common.flatten(grid))

  grid, output = common.grids(width, height, 8)
  offset = 0
  for wide, tall, brow, bcol, length, depth, left, top in zip(
      wides, talls, brows, bcols, lengths, depths, lefts, tops
  ):
    common.rect(grid, wide, tall, brow, bcol, 0)
    common.rect(output, wide, tall, brow, bcol, 0)
    for row in range(tall):
      for col in range(wide):
        color = int(patterns[offset + (row % depth) * length + col % length])
        output[brow + row][bcol + col] = color
        if (left and col >= length) or (not left and col + length < wide):
          continue
        if (top and row >= depth) or (not top and row + depth < tall):
          continue
        grid[brow + row][bcol + col] = color
    offset += depth * length
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(width=19, height=23, wides=[8, 9], talls=[6, 6], brows=[2, 13],
               bcols=[2, 7], lengths=[2, 3], depths=[2, 3], lefts=[1, 0],
               tops=[1, 0], patterns="1110030303333"),
      generate(width=13, height=19, wides=[6], talls=[12], brows=[3], bcols=[2],
               lengths=[3], depths=[3], lefts=[1], tops=[1],
               patterns="222022202"),
      generate(width=21, height=24, wides=[10, 15], talls=[9, 6], brows=[3, 14],
               bcols=[6, 3], lengths=[5, 3], depths=[3, 3], lefts=[0, 1],
               tops=[1, 0], patterns="020202202202220444040404"),
  ]
  test = [
      generate(width=22, height=26, wides=[6, 6, 8], talls=[9, 8, 6],
               brows=[2, 4, 16], bcols=[3, 13, 3], lengths=[3, 2, 4],
               depths=[3, 2, 3], lefts=[0, 1, 0], tops=[1, 0, 0],
               patterns="0101011104044303303033303"),
  ]
  return {"train": train, "test": test}
