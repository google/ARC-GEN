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


def generate(size=None, wides=None, talls=None, brows=None, bcols=None,
             hmids=None, vmids=None, idxs=None, colors=None, bcolor=None):
  """Returns input and output grids according to the given parameters.

  Args:
    colors: A list of colors to use.
  """

  if size is None:
    base = common.randint(1, 3)
    size, num_boxes = 10 + 6 * base, base + 2
    while True:
      wides = [common.randint(5, size // 2) for _ in range(num_boxes)]
      talls = [common.randint(5, size // 2) for _ in range(num_boxes)]
      brows = [common.randint(1, size - t - 1) for t in talls]
      bcols = [common.randint(1, size - w - 1) for w in wides]
      if not common.overlaps(brows, bcols, wides, talls, 1): break
    hmids = [common.randint(2, tall - 3) for tall in talls]
    vmids = [common.randint(2, wide - 3) for wide in wides]
    while True:
      idxs = [common.randint(0, num_boxes - 1) for _ in range(4)]
      if len(set(idxs)) > 1: break
    colors = common.random_colors(5)
    bcolor = colors.pop()

  grid, output = common.grids(size, size)
  for i, (wide, tall, brow, bcol, hmid, vmid) in enumerate(zip(wides, talls,
                                                               brows, bcols,
                                                               hmids, vmids)):
    for g in [grid, output]:
      common.hollow_rect(g, vmid + 1, hmid + 1, brow, bcol, bcolor)
      common.hollow_rect(g, wide - vmid, hmid + 1, brow, bcol + vmid, bcolor)
      common.hollow_rect(g, vmid + 1, tall - hmid, brow + hmid, bcol, bcolor)
      common.hollow_rect(g, wide - vmid, tall - hmid, brow + hmid, bcol + vmid, bcolor)
      if g == output or i == idxs[0]:
        w, t = vmid - 1, hmid - 1
        r, c = brow + 1, bcol + 1
        common.rect(g, w, t, r, c, colors[0])
      if g == output or i == idxs[1]:
        w, t = wide - vmid - 2, hmid - 1
        r, c = brow + 1, bcol + vmid + 1
        common.rect(g, w, t, r, c, colors[1])
      if g == output or i == idxs[2]:
        w, t = vmid - 1, tall - hmid - 2
        r, c = brow + hmid + 1, bcol + 1
        common.rect(g, w, t, r, c, colors[2])
      if g == output or i == idxs[3]:
        w, t = wide - vmid - 2, tall - hmid - 2
        r, c = brow + hmid + 1, bcol + vmid + 1
        common.rect(g, w, t, r, c, colors[3])
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(size=22, wides=[7, 11, 7, 9], talls=[7, 11, 10, 6],
               brows=[1, 2, 11, 14], bcols=[1, 9, 1, 10], hmids=[3, 4, 5, 2],
               vmids=[3, 6, 3, 4], idxs=[0, 2, 0, 0], colors=[4, 3, 9, 6],
               bcolor=1),
      generate(size=22, wides=[6, 5, 6, 9], talls=[6, 5, 11, 7],
               brows=[1, 1, 8, 10], bcols=[2, 10, 1, 8], hmids=[2, 2, 6, 3],
               vmids=[3, 2, 3, 4], idxs=[1, 3, 0, 1], colors=[1, 4, 6, 3],
               bcolor=5),
  ]
  test = [
      generate(size=28, wides=[6, 12, 8, 9, 5, 14], talls=[6, 10, 18, 7, 5, 5],
               brows=[1, 3, 9, 14, 15, 22], bcols=[1, 10, 1, 11, 22, 13],
               hmids=[2, 4, 8, 3, 2, 2], vmids=[3, 5, 4, 5, 2, 6],
               idxs=[1, 3, 0, 2], colors=[3, 2, 4, 1], bcolor=8),
  ]
  return {"train": train, "test": test}
