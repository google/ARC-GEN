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


def generate(size=None, grows=None, gcols=None, femurs=None, tibias=None,
             angles=None):
  """Returns input and output grids according to the given parameters.

  Args:
    size: The size of the grid.
    grows: The rows of the greys.
    gcols: The columns of the greys.
    femurs: The lengths of the femurs.
    tibias: The lengths of the tibias.
    angles: The angles of the segments.
  """

  def draw(bend=False):
    drs, dcs = [-1, 0, 1, 0], [0, 1, 0, -1]
    grid = common.grid(size, size, 7)
    ids = common.grid(size, size, -1)
    def put(row, col, val, id):
      # Make sure it's in bounds, and not already drawn.
      if row < 0 or col < 0 or row >= size or col >= size: return False
      if grid[row][col] != 7: return False
      grid[row][col], ids[row][col] = val, id
      return True
    # Draw the lines on the grid, and the IDs of the lines on the other grid.
    for id, (grow, gcol, femur, tibia, angle) in enumerate(zip(grows, gcols, femurs, tibias, angles)):
      row, col = grow, gcol
      # Draw the grey.
      if not put(row, col, 5, id): return None
      # Draw the femur.
      dr, dc = drs[angle], dcs[angle]
      for _ in range(femur):
        row, col = row + dr, col + dc
        if not put(row, col, 2, id): return None
      # Draw the knee.
      row, col = row + dr, col + dc
      if not put(row, col, 0, id): return None
      if bend:
        if angle in [0, 2]: angle = 1 if col < size // 2 else 3
        elif angle in [1, 3]: angle = 2 if row < size // 2 else 0
      # Draw the tibia.
      dr, dc = drs[angle], dcs[angle]
      for _ in range(tibia):
        row, col = row + dr, col + dc
        if not put(row, col, 2, id): return None
    # Now, check that no two lines were drawn too near to each other.
    for row in range(size):
      for col in range(size):
        if ids[row][col] == -1: continue
        for dr in [-1, 0, 1]:
          for dc in [-1, 0, 1]:
            id = common.get_pixel(ids, row + dr, col + dc)
            if id != -1 and id != ids[row][col]: return None
    return grid

  if size is None:
    segments = common.randint(1, 7)
    size = min(2 * segments + 6, 16)
    while True:
      lengths = [common.randint(3, size - 2) for _ in range(segments)]
      angles = [common.randint(0, 3) for _ in range(segments)]
      grows, gcols, femurs, tibias = [], [], [], []
      for length, angle in zip(lengths, angles):
        grows.append(common.randint(0, size - (length if angle in [0, 2] else 1)))
        gcols.append(common.randint(0, size - (length if angle in [1, 3] else 1)))
        tibia = common.randint(1, length - 2)  # - 2 because of grey and black
        fremur = length - 2 - tibia
        femurs.append(fremur)
        tibias.append(tibia)
      grid, output = draw(bend=False), draw(bend=True)
      if grid and output: break

  grid, output = draw(bend=False), draw(bend=True)
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(size=10, grows=[1, 1], gcols=[1, 7], femurs=[2, 4],
               tibias=[4, 1], angles=[2, 2]),
      generate(size=8, grows=[3], gcols=[1], femurs=[2], tibias=[2],
               angles=[1]),
      generate(size=12, grows=[2, 9, 11], gcols=[4, 1, 10], femurs=[1, 2, 2],
               tibias=[1, 2, 5], angles=[3, 1, 3]),
  ]
  test = [
      generate(size=16, grows=[2, 5, 11, 15, 15, 15, 15],
               gcols=[13, 4, 10, 1, 4, 6, 15], femurs=[2, 2, 0, 7, 4, 1, 0],
               tibias=[2, 2, 1, 3, 1, 2, 1], angles=[2, 1, 1, 0, 0, 0, 3]),
  ]
  return {"train": train, "test": test}
