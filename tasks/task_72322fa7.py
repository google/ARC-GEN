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


def generate(width=None, height=None, rows=None, cols=None, colors=None,
             idxs=None, megarows=None, megacols=None, megaidxs=None,
             megashows=None):
  """Returns input and output grids according to the given parameters.

  Args:
    width: the width of the grid
    height: the height of the grid
    rows: a list of vertical coordinates where pixels should be placed
    cols: a list of horizontal coordinates where pixels should be placed
    colors: a list of digits representing the colors to be used
    idxs: a list of indices into the array of sprite types
    megarows: a list of vertical coordinates where sprites should be placed
    megacols: a list of horizontal coordinates where sprites should be placed
    megaidxs: a list of indices into the array of sprite types
    megashows: a list of values in the set {0, 1, 2} to indicate what to show
  """
  if width is None:
    while True:
      width, height = common.randint(10, 25), common.randint(10, 25)
      # First, choose the sprite types
      sprite_types = common.randint(1, 3)
      color_list = common.shuffle(range(1, 10))
      rows, cols, colors, idxs = [], [], [], []
      for idx in range(sprite_types):
        color0, color1 = color_list[2 * idx], color_list[2 * idx + 1]
        sprite_type = common.randint(0, 3)  # 0=x, 1=plus, 2=horiz, 3=vert
        if sprite_type == 0:
          rows.extend([0, 0, 1, 2, 2])
          cols.extend([0, 2, 1, 0, 2])
          colors.extend([color0, color0, color1, color0, color0])
          idxs.extend([idx] * 5)
        if sprite_type == 1:
          rows.extend([0, 1, 1, 1, 2])
          cols.extend([1, 0, 1, 2, 1])
          colors.extend([color0, color0, color1, color0, color0])
          idxs.extend([idx] * 5)
        if sprite_type == 2:
          rows.extend([1, 1, 1])
          cols.extend([0, 1, 2])
          colors.extend([color0, color1, color0])
          idxs.extend([idx] * 3)
        if sprite_type == 3:
          rows.extend([0, 1, 2])
          cols.extend([1, 1, 1])
          colors.extend([color0, color1, color0])
          idxs.extend([idx] * 3)
      # Second, choose some non-overlapping locations.
      megarows, megacols, megaidxs, megashows = [], [], [], []
      for idx in range(sprite_types):
        copies = common.randint(2, 4)
        megarows.extend([common.randint(0, height - 3) for _ in range(copies)])
        megacols.extend([common.randint(0, width - 3) for _ in range(copies)])
        megaidxs.extend([idx] * copies)
        megashows.extend([0])
        megashows.extend([common.randint(1, 2) for _ in range(copies - 1)])
      lengths = [3] * len(megarows)
      if not common.overlaps(megarows, megacols, lengths, lengths, 2): break

  grid, output = common.grids(width, height)
  for mr, mc, mi, ms in zip(megarows, megacols, megaidxs, megashows):
    for row, col, color, idx in zip(rows, cols, colors, idxs):
      if idx != mi: continue
      output[mr + row][mc + col] = grid[mr + row][mc + col] = color
      if ms == 0: continue
      if ms == 1 and row == 1 and col == 1: continue
      if ms == 2 and (row != 1 or col != 1): continue
      grid[mr + row][mc + col] = common.black()
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(width=22, height=13, rows=[0, 0, 1, 2, 2, 0, 1, 1, 1, 2],
               cols=[0, 2, 1, 0, 2, 1, 0, 1, 2, 1],
               colors=[1, 1, 3, 1, 1, 8, 8, 6, 8, 8],
               idxs=[0, 0, 0, 0, 0, 1, 1, 1, 1, 1],
               megarows=[0, 3, 4, 9, 9, 9], megacols=[12, 5, 18, 1, 8, 15],
               megaidxs=[0, 1, 1, 0, 1, 1], megashows=[1, 0, 1, 0, 1, 2]),
      generate(width=12, height=13, rows=[1, 1, 1], cols=[0, 1, 2],
               colors=[4, 8, 4], idxs=[0, 0, 0], megarows=[2, 3, 8, 9],
               megacols=[1, 9, 0, 6], megaidxs=[0, 0, 0, 0],
               megashows=[0, 1, 2, 1]),
      generate(width=19, height=14, rows=[1, 1, 1, 0, 1, 2],
               cols=[0, 1, 2, 1, 1, 1],
               colors=[8, 2, 8, 1, 3, 1],
               idxs=[0, 0, 0, 1, 1, 1],
               megarows=[0, 2, 4, 10, 11], megacols=[15, 8, 2, 4, 11],
               megaidxs=[0, 0, 1, 0, 1], megashows=[0, 2, 0, 1, 1]),
  ]
  test = [
      generate(width=19, height=19, rows=[1, 1, 1, 0, 1, 2, 0, 1, 1, 1, 2],
               cols=[0, 1, 2, 1, 1, 1, 1, 0, 1, 2, 1],
               colors=[3, 7, 3, 1, 8, 1, 2, 2, 4, 2, 2],
               idxs=[0, 0, 0, 1, 1, 1, 2, 2, 2, 2, 2],
               megarows=[0, 1, 2, 5, 7, 9, 9, 14, 15, 15],
               megacols=[12, 7, 2, 5, 15, 0, 8, 10, 4, 16],
               megaidxs=[0, 1, 2, 0, 2, 1, 0, 2, 2, 1],
               megashows=[0, 1, 1, 2, 0, 1, 1, 2, 1, 0]),
  ]
  return {"train": train, "test": test}
