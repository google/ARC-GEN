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


def generate(width=None, height=None, color=None, brows=None, bcols=None,
             lengthss=None, turnss=None, idxss=None):
  """Returns input and output grids according to the given parameters.

  Args:
    width: The width of the grid.
    height: The height of the grid.
    color: The color of the lines.
    brows: The row indices of the start of each box.
    bcols: The column indices of the start of each box.
    lengthss: The lengths of each segment.
    turnss: The turns at the end of each segment.
    idxss: The box indices of each segment.
  """

  def draw():
    num_reds = 0
    grid, output = common.grids(width, height)
    for bidx, (brow, bcol) in enumerate(zip(brows, bcols)):
      lengths = [int(length) for length, idx in zip(lengthss, idxss) if idx == str(bidx)]
      turns = [turn for turn, idx in zip(turnss, idxss) if idx == str(bidx)]
      # First, draw the pixels.
      row, col = brow, bcol
      rdirs, cdirs, angle = [0, 1, 0, -1], [1, 0, -1, 0], 0
      for length, turn in zip(lengths, turns):
        for i in range(length - 1):
          common.draw(grid, row, col, color)
          if i: common.draw(output, row, col, color)
          row, col = row + rdirs[angle], col + cdirs[angle]
        if turn == "L":
          angle = (angle + 3) % 4
          common.draw(output, row, col, 2)
          num_reds += 1
        elif turn == "R":
          angle = (angle + 1) % 4
          common.draw(output, row, col, 4)
      # Second, ensure that each pixel has exactly two neighbors.
      row, col = brow, bcol
      rdirs, cdirs, angle = [0, 1, 0, -1], [1, 0, -1, 0], 0
      for length, turn in zip(lengths, turns):
        for _ in range(length - 1):
          if row < 0 or row >= height or col < 0 or col >= width:
            return None, None  # Out of bounds.
          neighbors = 0
          for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            if common.get_pixel(grid, row + dr, col + dc) == color:
              neighbors += 1
          if neighbors != 2: return None, None
          row, col = row + rdirs[angle], col + cdirs[angle]
        if turn == "L":
          angle = (angle + 3) % 4
        elif turn == "R":
          angle = (angle + 1) % 4
    if num_reds < 5: return None, None
    return grid, output

  if width is None:
    width, height = common.randint(12, 16), common.randint(12, 16)
    color, num_boxes = common.random_color(exclude=[2, 4]), common.randint(2, 3)
    while True:
      wides = [common.randint(3, 10) for _ in range(num_boxes)]
      talls = [common.randint(3, 10) for _ in range(num_boxes)]
      brows = [common.randint(0, height - tall) for tall in talls]
      bcols = [common.randint(0, width - wide) for wide in wides]
      if common.overlaps(brows, bcols, wides, talls, 1): continue
      lengthss, turnss, idxss = [], [], []
      for bidx, (wide, tall) in enumerate(zip(wides, talls)):
        lengths = [wide, tall, wide, tall]
        turns = ["R", "R", "R", "R"]
        idxs = [bidx] * 4
        for _ in range((wide + tall) // 4):
          idx = common.randint(0, len(lengths) - 1)
          if lengths[idx] < 5: continue
          segment = common.randint(3, lengths[idx] - 2)
          start = common.randint(1, lengths[idx] - segment - 1)
          depth = common.randint(2, 4)
          length = [start + 1, depth, segment, depth, lengths[idx] - (start + segment) + 1]
          turn = ["L", "R", "R", "L"] if common.randint(0, 1) else ["R", "L", "L", "R"]
          lengths = lengths[:idx] + length + lengths[idx + 1:]
          turns = turns[:idx] + turn + turns[idx:]
          idxs = idxs[:idx] + [bidx] * 4 + idxs[idx:]
        lengthss.extend(lengths)
        turnss.extend(turns)
        idxss.extend(idxs)
      lengthss = "".join(str(length) for length in lengthss)
      turnss = "".join(turnss)
      idxss = "".join(str(idx) for idx in idxss)
      grid, _ = draw()
      if grid: break

  grid, output = draw()
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(width=15, height=12, color=8, brows=[1, 4, 9], bcols=[1, 10, 2],
               lengthss="75423423 5523533323 3333",
               turnss="RRLRRLRR RRLRRRLLRR RRRR",
               idxss="00000000 1111111111 2222"),
      generate(width=13, height=13, color=3, brows=[2, 8], bcols=[2, 4],
               lengthss="32443244 5322364254", turnss="LRRRLRRR LRLRRRLRRR",
               idxss="00000000 111111111111"),
      generate(width=16, height=14, color=1, brows=[1, 10], bcols=[1, 3],
               lengthss="6235324434 62324224323283",
               turnss="RLRRLRRLRR LRLRRLRRRLLRRR",
               idxss="0000000000 11111111111111"),
  ]
  test = [
      generate(width=16, height=15, color=3, brows=[2, 4, 12], bcols=[1, 11, 3],
               lengthss="22324235432342443334 49543423 3333",
               turnss="LRRLLRRRLLRRLRRRLLRR RRRRLLRR RRRR",
               idxss="00000000000000000000 11111111 2222"),
  ]
  return {"train": train, "test": test}
