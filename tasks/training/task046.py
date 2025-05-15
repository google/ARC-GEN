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


def generate(rows=None, cols=None, wides=None, offsets=None, colors=None,
             extra=None, height=3):
  """Returns input and output grids according to the given parameters.

  Args:
    rows: a list of vertical coordinates where pixels should be placed
    cols: a list of horizontal coordinates where pixels should be placed
    wides: a list of widths of the segments
    offsets: a list of offsets for the segments
    colors: a list of digits representing the color to be used
    extra: an extra column (or not) in the input grid
    height: the height of the input grid
  """
  if rows is None:
    wides = [common.randint(2, 4) for _ in range(common.randint(3, 4))]
    colors = [common.random_color(exclude=[common.gray()]) for _ in wides]
    rows, cols, r, c = [], [], 1, 0
    for w in wides:
      # Sometimes choose a column to "turn" (esp. if we're a short segment!)
      turn = -1 if w > 2 and common.randint(0, 1) else common.randint(0, w - 1)
      for i in range(w):
        rows.append(r)
        cols.append(c)
        if i == turn:
          angle = common.choice([1, -1])
          if r in [0, height - 1]: angle = (1 - 2 * min(r, 1))
          while True:  # Turn as much as desired, but don't go off the grid.
            r += angle
            rows.append(r)
            cols.append(c)
            if r in [0, height - 1] or common.randint(0, 1) or w > 2: break
        c += 1
    offsets, c = [], 0
    for idx, w in enumerate(wides):
      srows = [p[0] for p in zip(rows, cols) if p[1] >= c and p[1] < c + w]
      offset = common.randint(-min(srows), height - max(srows) - 1)
      offsets.append(offset if idx > 0 else 0)
      c += w
    extra = common.randint(0, 1)

  width = sum(wides)
  grid = common.grid(width + len(colors) - 1 + extra, height)
  output = common.grid(width, height)
  # We'll create a idxs vector that maps each pixel to its segment.
  idxs, c = [-1] * len(rows), 0
  for w in wides:
    for i in range(len(idxs)):
      if cols[i] >= c: idxs[i] += 1
    c += w
  for i, idx in enumerate(idxs):
    r, c, color = rows[i], cols[i], colors[idx]
    if i > 0 and idx != idxs[i - 1]: color = common.gray()
    if i + 1 < len(idxs) and idx != idxs[i + 1]: color = common.gray()
    grid[r + offsets[idx]][c + idx] = color
    output[r][c] = colors[idx]
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(rows=[1, 1, 0, 0, 0, 1, 1, 1, 1],
               cols=[0, 1, 1, 2, 3, 3, 4, 5, 6, 7],
               wides=[2, 2, 3], offsets=[0, 1, 0], colors=[2, 1, 2], extra=0),
      generate(rows=[1, 1, 2, 2, 2, 2, 2, 2, 1, 1, 1],
               cols=[0, 1, 1, 2, 3, 4, 5, 6, 6, 7, 8],
               wides=[2, 3, 4], offsets=[0, -2, 0], colors=[2, 1, 3], extra=0),
      generate(rows=[1, 1, 1, 2, 2, 2, 2, 1, 1, 1, 1],
               cols=[0, 1, 2, 2, 3, 4, 5, 5, 6, 7, 8],
               wides=[3, 3, 3], offsets=[0, -1, 1], colors=[2, 8, 6], extra=0),
      generate(rows=[1, 1, 0, 0, 0, 0, 1, 1, 1, 0, 0],
               cols=[0, 1, 1, 2, 3, 4, 4, 5, 6, 6, 7],
               wides=[3, 2, 3], offsets=[0, 1, 0], colors=[1, 2, 2], extra=1),
  ]
  test = [
      generate(rows=[1, 1, 0, 0, 0, 1, 2, 2, 2, 1, 1, 1, 2],
               cols=[0, 1, 1, 2, 3, 3, 3, 4, 5, 5, 6, 7, 7],
               wides=[2, 2, 2, 2], offsets=[0, 0, -1, -1], colors=[2, 1, 3, 8],
               extra=0),
  ]
  return {"train": train, "test": test}
