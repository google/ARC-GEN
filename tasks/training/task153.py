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


def generate(rows=None, cols=None, idxs=None, colors=None, size=10, minisize=3):
  """Returns input and output grids according to the given parameters.

  Args:
    rows: a list of vertical coordinates where halves should be placed
    cols: a list of horizontal coordinates where halves should be placed
    idxs: a list of indices into the colors pair
    colors: a pair of digits representing the colors of the halves
    size: the width and height of the input grid
    minisize: the width and height of the output grid
  """
  if rows is None:
    # TODO: Allow rows / cols that eclipse the grid if the half is small enough.
    # TODO: Ensure that the negative of the creature is also contiguous?
    while True:
      rows = [common.randint(0, size - 3) for _ in range(2)]
      cols = [common.randint(0, size - 3) for _ in range(2)]
      if abs(rows[0] - rows[1]) > 2 and abs(cols[0] - cols[1]) > 2: break
    while True:
      pixels = common.continuous_creature(common.randint(3, 6))
      idxs = []
      for r in range(minisize):
        for c in range(minisize):
          idxs.append(1 if (r, c) in pixels else 0)
      # Make sure the two halves are both self-connnected.
      one = [(i // 3, i % 3) for i, color in enumerate(idxs) if color == 0]
      two = [(i // 3, i % 3) for i, color in enumerate(idxs) if color == 1]
      if not common.diagonally_connected(one): continue
      if not common.diagonally_connected(two): continue
      # Make sure the solution can't be "split" evenly (causes ambiguity).
      unsplittable = False
      for r in range(minisize):
        if len(set([idxs[r * minisize + c] for c in range(minisize)])) > 1:
          unsplittable = True
      if not unsplittable: continue
      unsplittable = False
      for c in range(minisize):
        if len(set([idxs[r * minisize + c] for r in range(minisize)])) > 1:
          unsplittable = True
      if not unsplittable: continue
      break
    colors = common.random_colors(2)

  grid, output = common.grid(size, size), common.grid(minisize, minisize)
  for r in range(minisize):
    for c in range(minisize):
      idx = idxs[r * minisize + c]
      output[r][c] = grid[rows[idx] + r][cols[idx] + c] = colors[idx]
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(rows=[2, 7], cols=[1, 7], idxs=[0, 0, 1, 0, 1, 1, 0, 1, 1],
               colors=[3, 7]),
      generate(rows=[-1, 2], cols=[8, 3], idxs=[1, 1, 1, 0, 1, 1, 0, 0, 1],
               colors=[4, 6]),
      generate(rows=[3, 8], cols=[3, 1], idxs=[1, 1, 1, 1, 0, 1, 0, 0, 0],
               colors=[3, 1]),
  ]
  test = [
      generate(rows=[2, 6], cols=[2, 7], idxs=[1, 1, 0, 1, 0, 0, 1, 1, 1],
               colors=[2, 8]),
  ]
  return {"train": train, "test": test}
