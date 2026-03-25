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


def generate(width=None, height=None, brows=None, bcols=None, tops=None,
             bottoms=None, lefts=None, rights=None, color=None):
  """Returns input and output grids according to the given parameters.

  Args:
    width: The width of the grid.
    height: The height of the grid.
    brows: The rows of the boxes.
    bcols: The columns of the boxes.
    tops: Whether the boxes go up.  
    bottoms: Whether the boxes go down.
    lefts: Whether the boxes go left.
    rights: Whether the boxes go right.
    color: The color of the boxes.
  """

  def draw():
    grid, output = common.grids(width, height)
    # First, draw the input grid.
    for brow, bcol, top, bottom, left, right in zip(brows, bcols, tops, bottoms, lefts, rights):
      common.hollow_rect(grid, 4, 4, brow, bcol, color)
      if top: common.rect(grid, 4, 1, 0, bcol, 1)
      if bottom: common.rect(grid, 4, 1, height - 1, bcol, 1)
      if left: common.rect(grid, 1, 4, brow, 0, 1)
      if right: common.rect(grid, 1, 4, brow, width - 1, 1)
    # Second, draw the output grid.
    for brow, bcol, top, bottom, left, right in zip(brows, bcols, tops, bottoms, lefts, rights):
      common.hollow_rect(output, 4, 4, brow, bcol, color)
      if top:
        row = brow
        while row + 4 >= 0:
          row -= 4
          if not common.hollow_rect(output, 4, 4, row, bcol, color, True):
            return None, None
      if bottom:
        row = brow
        while row - 4 <= height:
          row += 4
          if not common.hollow_rect(output, 4, 4, row, bcol, color, True):
            return None, None
      if left:
        col = bcol
        while col + 4 >= 0:
          col -= 4
          if not common.hollow_rect(output, 4, 4, brow, col, color, True):
            return None, None
      if right:
        col = bcol
        while col - 4 <= width:
          col += 4
          if not common.hollow_rect(output, 4, 4, brow, col, color, True):
            return None, None
    return grid, output

  if width is None:
    mid = common.randint(18, 22)
    width = mid + common.randint(0, 4) - 2
    height = mid + common.randint(0, 4) - 2
    num_boxes = common.randint(1, 2)
    color = common.random_color(exclude=[1])
    while True:
      brows = [common.randint(2, height - 6) for _ in range(num_boxes)]
      bcols = [common.randint(2, width - 6) for _ in range(num_boxes)]
      # More than just not overlapping, their "sight lines" should also differ.
      if num_boxes == 2:
        if abs(brows[0] - brows[1]) <= 6 or abs(bcols[0] - bcols[1]) <= 6:
          continue
      tops, bottoms, lefts, rights = [], [], [], []
      for _ in range(num_boxes):
        values = common.choices([0, 1, 2, 3], common.randint(1, 3))
        tops.append(1 if 0 in values else 0)
        bottoms.append(1 if 1 in values else 0)
        lefts.append(1 if 2 in values else 0)
        rights.append(1 if 3 in values else 0)
      grid, _ = draw()
      if grid: break  # Checks that their paths don't clobber each other.

  grid, output = draw()
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(width=19, height=22, brows=[8, 14], bcols=[8, 2], tops=[1, 0],
               bottoms=[0, 1], lefts=[1, 0], rights=[1, 0], color=8),
      generate(width=17, height=18, brows=[2], bcols=[2], tops=[0], bottoms=[1],
               lefts=[0], rights=[1], color=2),
      generate(width=22, height=22, brows=[5, 11], bcols=[6, 12], tops=[1, 0],
               bottoms=[0, 1], lefts=[1, 0], rights=[0, 1], color=3),
  ]
  test = [
      generate(width=24, height=24, brows=[6, 12], bcols=[6, 13], tops=[1, 1],
               bottoms=[1, 1], lefts=[1, 0], rights=[0, 0], color=4),
  ]
  return {"train": train, "test": test}
