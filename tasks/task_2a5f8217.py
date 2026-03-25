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


def generate(size=None, brows=None, bcols=None, bshapes=None, srows=None,
             scols=None, sshapes=None, colors=None):
  """Returns input and output grids according to the given parameters.

  Args:
    size: The size of the grid.
    brows: The rows of the boxes.
    bcols: The columns of the boxes.
    bshapes: The shapes of the boxes.
    srows: The rows of the shape pixels.
    scols: The columns of the shape pixels.
    sshapes: The shapes of the shape pixels.
    colors: The colors of the shapes.
  """

  def draw():
    grid, output = common.grids(size, size)
    ids = common.grid(size, size, -1)
    seen = set()
    for i, (brow, bcol, bshape) in enumerate(zip(brows, bcols, bshapes)):
      rows = [r for r, s in zip(srows, sshapes) if s == bshape]
      cols = [c for c, s in zip(scols, sshapes) if s == bshape]
      for row, col in zip(rows, cols):
        if grid[brow + row][bcol + col] != 0: return None, None
        grid[brow + row][bcol + col] = 1 if bshape in seen else colors[bshape]
        output[brow + row][bcol + col] = colors[bshape]
        ids[brow + row][bcol + col] = i
      seen.add(bshape)
    # Now, check that no two shapes share a common edge.
    for r in range(size):
      for c in range(size):
        if ids[r][c] == -1: continue
        for dr, dc in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
          if common.get_pixel(ids, r + dr, c + dc) not in [-1, ids[r][c]]:
            return None, None
    # Shapes can touch corners ... but only if their colors differ!
    for r in range(size):
      for c in range(size):
        if ids[r][c] == -1: continue
        for dr, dc in [(1, 1), (-1, 1), (1, -1), (-1, -1)]:
          if common.get_pixel(ids, r + dr, c + dc) not in [-1, ids[r][c]]:
            if grid[r + dr][c + dc] == grid[r][c]: return None, None
    return grid, output

  if size is None:
    size = common.randint(6, 15)
    num_shapes = (size - 3) // 2
    colors = [common.random_color(exclude=[1]) for _ in range(num_shapes)]
    bshapes = list(range(num_shapes)) + list(range(num_shapes))
    while True:
      # Find widths and heights of the basic shapes.
      wides, talls, coords = [], [], []
      for _ in range(num_shapes):
        while True:
          wide, tall = common.randint(1, 3), common.randint(1, 3)
          if wide > 1 or tall > 1: break
        wides, talls = wides + [wide], talls + [tall]
        coords.append(common.connected_sprite(wide, tall))
      # Check that the chosen shapes are unique.
      shape_set = set()
      good = True
      for coord in coords:
        if tuple(coord) in shape_set: good = False
        shape_set.add(tuple(coord))
      if not good: continue
      # Find locations of the shapes and their copies.
      brows = [common.randint(0, size - talls[shape]) for shape in bshapes]
      bcols = [common.randint(0, size - wides[shape]) for shape in bshapes]
      srows, scols, sshapes = [], [], []
      for i, coord in enumerate(coords):
        for r, c in coord:
          srows.append(r)
          scols.append(c)
          sshapes.append(i)
      grid, _ = draw()
      if grid: break

  grid, output = draw()
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(size=9, brows=[4, 6, 7, 1, 1, 5], bcols=[7, 5, 0, 1, 6, 2],
               bshapes=[0, 1, 2, 2, 1, 0],
               srows=[0, 0, 1, 0, 1, 1, 0, 0, 0, 1, 1],
               scols=[0, 1, 1, 0, 0, 1, 0, 1, 2, 0, 2],
               sshapes=[0, 0, 0, 1, 1, 1, 2, 2, 2, 2, 2], colors=[9, 7, 6]),
      generate(size=6, brows=[3, 0], bcols=[3, 0], bshapes=[0, 0],
               srows=[0, 1, 1, 1, 2], scols=[1, 0, 1, 2, 1],
               sshapes=[0, 0, 0, 0, 0], colors=[8]),
      generate(size=11, brows=[0, 4, 4, 7, 0, 0, 3, 8],
               bcols=[9, 0, 5, 7, 0, 5, 7, 2], bshapes=[0, 1, 2, 3, 3, 2, 0, 1],
               srows=[0, 1, 1, 2, 0, 1, 1, 1, 0, 1, 0, 1, 1, 1, 2],
               scols=[1, 0, 1, 1, 1, 0, 1, 2, 0, 0, 1, 0, 1, 2, 2],
               sshapes=[0, 0, 0, 0, 1, 1, 1, 1, 2, 2, 3, 3, 3, 3, 3],
               colors=[9, 3, 6, 7]),
  ]
  test = [
      generate(size=13, brows=[0, 5, 6, 9, 11, 1, 1, 4, 8, 10],
               bcols=[5, 1, 10, 10, 0, 1, 8, 5, 5, 2],
               bshapes=[0, 1, 2, 3, 4, 2, 0, 3, 1, 4],
               srows=[0, 0, 1, 1, 1, 2, 0, 1, 1, 2, 0, 1, 1, 1, 0, 1, 1, 1, 2, 0, 1],
               scols=[1, 2, 0, 1, 2, 1, 1, 0, 1, 1, 1, 0, 1, 2, 1, 0, 1, 2, 1, 0, 0],
               sshapes=[0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 2, 2, 2, 2, 3, 3, 3, 3, 3, 4, 4],
               colors=[8, 4, 2, 6, 8]),
  ]
  return {"train": train, "test": test}
