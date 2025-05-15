# Copyright 2025 Google LLC
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


def generate(starcolors=None, vert=None, horiz=None, srow=None, scol=None,
             brows=None, bcols=None, wides=None, talls=None, boxcolor=None,
             bgcolor=None, srows=None, scols=None, sidxs=None, flip=None,
             xpose=None, size=30, num_boxes=2):
  """Returns input and output grids according to the given parameters.

  Args:
    starcolors: a list of 4 colors for the star and its borders
    vert: whether the star extends vertically
    horiz: whether the star extends horizontally
    srow: the vertical coordinate of the star
    scol: the horizontal coordinate of the star
    brows: a list of vertical coordinates where the boxes are placed
    bcols: a list of horizontal coordinates where the boxes are placed
    wides: a list of widths of the boxes
    talls: a list of heights of the boxes
    boxcolor: a digit representing the color of the boxes
    bgcolor: a digit representing the color of the background
    srows: a list of vertical coordinates where the stars are placed
    scols: a list of horizontal coordinates where the stars are placed
    sidxs: a list of indices of the boxes that the stars are placed on
    flip: whether to flip the image
    xpose: whether to transpose the image
    size: the size of the image
    num_boxes: the number of boxes
  """

  def draw_star(grid, r, c, extra):
    for dr in [-1, 0, 1]:
      for dc in [-1, 0, 1]:
        if starcolors[2] != -1: grid[r + dr][c + dc] = starcolors[2]
    grid[r][c] = starcolors[0]
    for dr in [-1, 1]:
      if vert: grid[r + dr][c] = starcolors[1]
      if vert and extra: grid[r + 2 * dr][c] = starcolors[1]
    for dc in [-1, 1]:
      if horiz: grid[r][c + dc] = starcolors[1]
      if horiz and extra: grid[r][c + 2 * dc] = starcolors[1]

  def draw(grid, output):
    # Draw the boxes.
    for brow, bcol, wide, tall in zip(brows, bcols, wides, talls):
      for r in range(brow, brow + tall):
        for c in range(bcol, bcol + wide):
          output[r][c] = grid[r][c] = boxcolor
    for r in range(-3, 4):
      for c in range(-3, 4):
        if common.get_pixel(grid, srow + r, scol + c) == boxcolor:
          return False  # Too close to a box
    # Draw the star in the top right.
    draw_star(grid, srow, scol, True)
    # Draws the lines on top of the flags.
    for row, col, sidx in zip(srows, scols, sidxs):
      for c in range(bcols[sidx], bcols[sidx] + wides[sidx]):
        if horiz: output[row + brows[sidx]][c] = starcolors[1]
      for r in range(brows[sidx], brows[sidx] + talls[sidx]):
        if vert: output[r][col + bcols[sidx]] = starcolors[1]
    # Draws the stars on top of the flags.
    for row, col, sidx in zip(srows, scols, sidxs):
      grid[brows[sidx] + row][bcols[sidx] + col] = starcolors[0]
      draw_star(output, brows[sidx] + row, bcols[sidx] + col, False)
    return True

  if starcolors is None:
    while True:
      # First, figure out the colors.
      color_list = common.random_colors(5)
      starcolors = [color_list[0], color_list[1], color_list[2]]
      boxcolor, bgcolor = color_list[3], color_list[4]
      while True:
        vert, horiz = common.randint(0, 1), common.randint(0, 1)
        if vert or horiz: break
      if vert and horiz:
        starcolors[2] = -1 if common.randint(0, 1) else starcolors[0]
      # Next, placement of the star and boxes.
      srow, scol = common.randint(3, 5), common.randint(23, 25)
      wides = [common.randint(17, 18) for _ in range(num_boxes)]
      talls = [9, common.randint(13, 15)]
      if common.randint(0, 1): talls = talls[::-1]
      brows = [common.randint(1, 2)]
      brows.append(brows[0] + talls[0] + common.randint(1, 2))
      bcols = [common.randint(1, 3), common.randint(4, 8)]
      # Finally, place some stars within the boxes.
      srows, scols, sidxs = [], [], []
      for idx in range(num_boxes):
        num_stars = common.randint(1, 2)
        while True:
          xrows = common.sample(range(1, talls[idx] - 1), num_stars)
          if num_stars == 1 or max(xrows) - min(xrows) > 5: break
        while True:
          xcols = common.sample(range(1, wides[idx] - 1), num_stars)
          if num_stars == 1 or max(xcols) - min(xcols) > 5: break
        srows.extend(xrows)
        scols.extend(xcols)
        sidxs.extend([idx] * num_stars)
      flip, xpose = common.randint(0, 1), common.randint(0, 1)
      grid, output = common.grids(size, size, bgcolor)
      if draw(grid, output): break

  grid, output = common.grids(size, size, bgcolor)
  draw(grid, output)
  # Flip and/or transpose the images.
  if flip: grid, output = grid[::-1], output[::-1]
  if xpose: grid, output = common.transpose(grid), common.transpose(output)
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(starcolors=[3, 2, 3], vert=1, horiz=1, srow=4, scol=25,
               brows=[1, 18], bcols=[2, 8], wides=[17, 18], talls=[15, 9],
               boxcolor=1, bgcolor=8, srows=[4, 7], scols=[3, 9], sidxs=[0, 1],
               flip=0, xpose=0),
      generate(starcolors=[4, 3, -1], vert=1, horiz=1, srow=5, scol=24,
               brows=[5, 15], bcols=[1, 6], wides=[17, 18], talls=[9, 13],
               boxcolor=2, bgcolor=1, srows=[2, 5, 9], scols=[13, 4, 10],
               sidxs=[0, 0, 1], flip=0, xpose=0),
      generate(starcolors=[4, 5, 6], vert=1, horiz=0, srow=3, scol=24,
               brows=[6, 7, 15], bcols=[1, 12, 11], wides=[9, 10, 16],
               talls=[15, 7, 13], boxcolor=3, bgcolor=8, srows=[11, 2, 4, 8],
               scols=[3, 6, 4, 12], sidxs=[0, 1, 2, 2], flip=1, xpose=0),
  ]
  test = [
      generate(starcolors=[2, 8, 3], vert=1, horiz=0, srow=3, scol=23,
               brows=[3, 12], bcols=[2, 14], wides=[10, 14], talls=[12, 17],
               boxcolor=1, bgcolor=4, srows=[3, 6, 11], scols=[7, 10, 3],
               sidxs=[0, 1, 1], flip=0, xpose=1),
  ]
  return {"train": train, "test": test}
