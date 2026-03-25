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


def generate(width=None, height=None, bgwidth=None, bgheight=None, pattern=None,
             wides=None, talls=None, brows=None, bcols=None, outers=None,
             inners=None):
  """Returns input and output grids according to the given parameters.

  Args:
    width: The width of the input grid.
    height: The height of the input grid.
    bgwidth: The width of the background pattern.
    bgheight: The height of the background pattern.
    pattern: The pattern of the background pattern.
    wides: The widths of the rectangles.
    talls: The heights of the rectangles.
    brows: The rows of the rectangles.
    bcols: The columns of the rectangles.
    outers: The colors of the outer sides of the rectangles.
    inners: The colors of the inner sides of the rectangles (-1 if none).
  """

  def draw():
    grid, output = common.grid(width, height), common.grid(wides[0], talls[0])
    for r in range(height):
      for c in range(width):
        grid[r][c] = pattern[(r % bgheight) * bgwidth + c % bgwidth]
    j = 0
    for w, t, r, c, o, i in zip(wides, talls, brows, bcols, outers, inners):
      common.hollow_rect(grid, w, t, r, c, o)
      common.hollow_rect(output, w, t, talls[0] - t - j, j, o)
      if i != -1:
        common.rect(grid, w - 2, t - 2, r + 1, c + 1, i)
        common.rect(output, w - 2, t - 2, talls[0] - t - j + 1, j + 1, i)
      if i != o: j += 1
    # If the box has a center, it should be fully visible.
    for w, t, r, c, i in zip(wides, talls, brows, bcols, inners):
      if i == -1: continue
      for row in range(r + 1, r + t - 1):
        for col in range(c + 1, c + w - 1):
          if grid[row][col] != i: return None, None
    # Check that at least three corners of each box are visible.
    for w, t, r, c, o in zip(wides, talls, brows, bcols, outers):
      corners = 0
      if grid[r][c] == o: corners += 1
      if grid[r + t - 1][c] == o: corners += 1
      if grid[r][c + w - 1] == o: corners += 1
      if grid[r + t - 1][c + w - 1] == o: corners += 1
      if corners < 3: return None, None
    return grid, output

  if width is None:
    # First, settle on the background pattern.
    bgwidth, bgheight = common.randint(2, 4), common.randint(2, 3)
    subset, pattern = common.sample([0, 1, 2, 3], bgwidth), []
    for _ in range(bgheight):
      for c in range(bgwidth):
        pattern.append(subset[c])
    row = common.randint(0, bgheight - 1)
    for c in range(bgwidth):
      pattern[row * bgwidth + c] = subset[c - 1]
    # Second, settle on the rectangle types.
    while True:
      num_hollow = common.randint(0, 2)
      num_filled = common.randint(0, 1)
      num_solid = common.randint(1, 2)
      if num_hollow + num_filled + num_solid < 2: continue
      if num_hollow + num_filled + num_solid > 4: continue
      break
    # Third, settle on the rectangle sizes, positions, and colors.
    width, height = common.randint(21, 29), common.randint(12, 20)
    while True:
      colors = common.shuffle(list(range(1, 10)))
      for color in subset:
        if color: colors.remove(color)
      def get_color():
        return colors.pop()
      good = True
      wides, talls, outers, inners = [], [], [], []
      wide = common.randint(width // 2, width - 2)
      tall = common.randint(height // 2, height - 2)
      for _ in range(num_hollow):
        if wide < 5 or tall < 5: good = False
        wides.append(wide)
        talls.append(tall)
        outers.append(get_color())
        inners.append(-1)
        wide -= common.randint(3, 4)
        tall -= common.randint(3, 4)
      for _ in range(num_filled):
        if wide < 5 or tall < 5: good = False
        wides.append(wide)
        talls.append(tall)
        outers.append(get_color())
        inners.append(get_color())
        wide -= common.randint(3, 4)
        tall -= common.randint(3, 4)
      for _ in range(num_solid):
        if wide < 2 or tall < 2: good = False
        wides.append(wide)
        talls.append(tall)
        color = get_color()
        outers.append(color)
        inners.append(color)
        wide -= common.randint(1, 2)
        tall -= common.randint(1, 2)
      if not good: continue
      brows = [common.randint(0, height - t) for t in talls]
      bcols = [common.randint(0, width - w) for w in wides]
      grid, _ = draw()
      if grid: break

  grid, output = draw()
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(width=22, height=14, bgwidth=4, bgheight=2,
               pattern=[0, 1, 2, 3, 1, 2, 3, 0],
               wides=[11, 7, 2], talls=[12, 6, 2], brows=[1, 3, 8],
               bcols=[1, 8, 17], outers=[8, 4, 6], inners=[-1, 5, -1]),
      generate(width=23, height=13, bgwidth=3, bgheight=3,
               pattern=[0, 1, 2, 1, 2, 0, 1, 2, 0],
               wides=[12, 5, 2], talls=[9, 5, 2], brows=[3, 1, 0],
               bcols=[5, 14, 17], outers=[3, 8, 4], inners=[-1, 6, -1]),
      generate(width=23, height=16, bgwidth=2, bgheight=2,
               pattern=[0, 1, 1, 0],
               wides=[8, 3], talls=[8, 3], brows=[1, 4], bcols=[2, 12],
               outers=[3, 4], inners=[8, 4]),
  ]
  test = [
      generate(width=27, height=19, bgwidth=3, bgheight=3,
               pattern=[2, 3, 3, 1, 2, 2, 3, 1, 1],
               wides=[13, 9, 4, 2], talls=[15, 7, 3, 2], brows=[2, 6, 8, 2],
               bcols=[3, 10, 13, 21], outers=[8, 6, 4, 9],
               inners=[-1, -1, 4, -1]),
  ]
  return {"train": train, "test": test}
