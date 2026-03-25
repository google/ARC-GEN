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


def generate(wides=None, talls=None, brows=None, bcols=None, colors=None,
             pattern=None):
  """Returns input and output grids according to the given parameters.

  Args:
    wides: The widths of the sprites.
    talls: The heights of the sprites.
    brows: The row offsets of the sprites.
    bcols: The column offsets of the sprites.
    colors: The colors of the sprites.
    pattern: The pattern of the sprites.
  """

  def draw():
    if max(w * h for w, h in zip(wides, talls)) > 9: return None, None
    if common.overlaps(brows, bcols, wides, talls, 1): return None, None
    if common.overlaps_1d(bcols, wides): return None, None
    grid, output = common.grids(10, 10, 7)
    offset, deltas = 0, []
    for wide, tall, brow, bcol, color in zip(wides, talls, brows, bcols, colors):
      sprite = common.grid(wide, tall)
      for r in range(tall):
        for c in range(wide):
          sprite[r][c] = int(pattern[offset])
          offset += 1
      delta = sum(common.flatten(sprite))
      deltas.append(delta)
      for r in range(tall):
        for c in range(wide):
          if not sprite[r][c]: continue
          grid[brow + r][bcol + c] = color
          common.draw(output, brow + r + delta, bcol + c, color)
    if len(set(common.flatten(output))) != 4: return None, None
    if len(set(deltas)) != 3: return None, None
    return grid, output

  if wides is None:
    colors = [2, 5, 9]
    while True:
      wides = [common.randint(1, 4) for _ in range(3)]
      talls = [common.randint(1, 4) for _ in range(3)]
      brows = [common.randint(0, 10 - tall) for tall in talls]
      bcols = [common.randint(0, 10 - wide) for wide in wides]
      pattern = ""
      for wide, tall in zip(wides, talls):
        sprite = common.connected_sprite(wide, tall)
        for r in range(tall):
          for c in range(wide):
            pattern += "1" if (r, c) in sprite else "0"
      grid, _ = draw()
      if grid: break

  grid, output = draw()
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(wides=[3, 1, 1], talls=[1, 1, 4], brows=[2, 4, 1],
               bcols=[1, 4, 8], colors=[2, 5, 9], pattern="11111111"),
      generate(wides=[1, 2, 2], talls=[1, 1, 2], brows=[2, 4, 2],
               bcols=[2, 4, 7], colors=[5, 2, 9], pattern="1111101"),
      generate(wides=[4, 1, 1], talls=[2, 3, 2], brows=[1, 3, 7],
               bcols=[1, 6, 9], colors=[9, 2, 5], pattern="1111000111111"),
  ]
  test = [
      generate(wides=[1, 3, 2], talls=[3, 3, 1], brows=[6, 1, 4],
               bcols=[0, 3, 7], colors=[5, 2, 9], pattern="11101011101011"),
  ]
  return {"train": train, "test": test}
