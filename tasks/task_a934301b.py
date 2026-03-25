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


def generate(width=None, height=None, wides=None, talls=None, brows=None,
             bcols=None, prows=None, pcols=None, pidxs=None):
  """Returns input and output grids according to the given parameters.

  Args:
    colors: A list of colors to use.
  """

  if width is None:
    base = common.randint(13, 15)
    width = base + common.randint(-1, 1)
    height = base + common.randint(-1, 1)
    num_boxes = common.randint(6, 7)
    while True:
      wides = [common.randint(2, 6) for _ in range(num_boxes)]
      talls = [common.randint(2, 6) for _ in range(num_boxes)]
      brows = [common.randint(0, height - tall) for tall in talls]
      bcols = [common.randint(0, width - wide) for wide in wides]
      if not common.overlaps(brows, bcols, wides, talls, 1): break
    while True:
      prows, pcols, pidxs, num_small = [], [], [], 0
      for i in range(num_boxes):
        for r in range(talls[i]):
          for c in range(wides[i]):
            if common.randint(0, 9): continue
            prows.append(r)
            pcols.append(c)
            pidxs.append(i)
        if pidxs.count(i) < 2: num_small += 1
      if num_small == 3: break

  grid, output = common.grids(width, height)
  for i, (wide, tall, brow, bcol) in enumerate(zip(wides, talls, brows, bcols)):
    common.rect(grid, wide, tall, brow, bcol, 1)
    if pidxs.count(i) < 2:
      common.rect(output, wide, tall, brow, bcol, 1)
  for prow, pcol, pidx in zip(prows, pcols, pidxs):
    brow, bcol = brows[pidx], bcols[pidx]
    grid[brow + prow][bcol + pcol] = 8
    if pidxs.count(pidx) < 2:
      output[brow + prow][bcol + pcol] = 8
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(width=14, height=14, wides=[3, 2, 4, 4, 4, 4],
               talls=[3, 3, 3, 3, 4, 4], brows=[0, 0, 2, 5, 7, 10],
               bcols=[5, 11, 0, 9, 3, 10],
               prows=[0, 1, 0, 1, 2, 1, 2, 0, 1, 2, 2],
               pcols=[1, 1, 2, 1, 3, 2, 1, 1, 3, 1, 2],
               pidxs=[0, 2, 3, 3, 3, 4, 4, 5, 5, 5, 5]),
      generate(width=14, height=14, wides=[3, 3, 2, 3, 3, 3],
               talls=[2, 4, 2, 3, 3, 4], brows=[1, 2, 2, 5, 7, 9],
               bcols=[1, 5, 10, 11, 1, 7], prows=[0, 1, 1, 2, 3, 0, 1, 0, 1, 2],
               pcols=[1, 2, 1, 2, 0, 1, 1, 2, 0, 0],
               pidxs=[0, 0, 1, 1, 1, 2, 3, 4, 4, 5]),
      generate(width=15, height=13, wides=[4, 2, 4, 4, 5, 3, 4],
               talls=[4, 2, 3, 3, 3, 4, 3], brows=[0, 0, 1, 3, 6, 9, 10],
               bcols=[5, 11, 0, 11, 2, 9, 2],
               prows=[1, 1, 3, 0, 1, 1, 1, 0, 1, 2, 0, 1, 3, 3],
               pcols=[0, 3, 2, 0, 1, 1, 1, 2, 3, 1, 2, 1, 0, 2],
               pidxs=[0, 0, 0, 1, 1, 2, 3, 4, 4, 4, 5, 5, 5, 5]),
  ]
  test = [
      generate(width=12, height=13, wides=[4, 3, 3, 4, 6, 3],
               talls=[3, 3, 4, 4, 4, 2], brows=[0, 1, 3, 6, 8, 11],
               bcols=[8, 0, 4, 8, 1, 8], prows=[0, 2, 2, 1, 0, 2, 1, 1, 2],
               pcols=[1, 1, 3, 0, 0, 2, 2, 4, 1],
               pidxs=[0, 0, 0, 1, 2, 2, 3, 4, 4]),
  ]
  return {"train": train, "test": test}
