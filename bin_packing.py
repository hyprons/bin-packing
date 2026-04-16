def compute_rotation(dim: list[float], rot: tuple[int, int, int]) -> list[float]:
    dim_new = dim.copy()

    if rot[0]:  # x rot
        temp = dim_new[2]
        dim_new[2] = dim_new[1]
        dim_new[1] = temp
    if rot[1]:  # y rot
        temp = dim_new[0]
        dim_new[0] = dim_new[2]
        dim_new[2] = temp
    if rot[2]:  # z rot
        temp = dim_new[0]
        dim_new[0] = dim_new[1]
        dim_new[1] = temp

    return dim_new


def compute_item_count(box_dim: list[float], item_dim: list[float], branch: int) -> int:
    global rotations
    # global rotations_s

    # dimensions of items that fit with item quantity as unit
    item_count = [
        (box_dim[0] / item_dim[0]) // 1,
        (box_dim[1] / item_dim[1]) // 1,
        (box_dim[2] / item_dim[2]) // 1,
    ]

    print(item_count, box_dim, item_dim)

    # TODO: add non greedy alternative for maximizing possible items
    # for x_has_z; for y_has_z; for x_has_y; 2^3 = 8 possiblities
    # to split the overlapping space, iterate over these
    # https://prnt.sc/08r7MAN7oLI3

    # comput leftover space
    diffs = [box_dim[i] - item_dim[i] * item_count[i] for i in range(0, 3)]
    # greedily let z cut out the volume, then x then y
    splits = [
        [diffs[2], box_dim[0], box_dim[1]],
        [diffs[0], (item_count[2] * item_dim[2]), box_dim[1]],
        [diffs[1], (item_count[0] * item_dim[0]), (item_count[2] * item_dim[2])],
    ]

    count = int(item_count[0] * item_count[1] * item_count[2])

    best_count_total = 0

    for i in splits:
        best_count = 0
        sub_box_vol = i[0] * i[1] * i[2]  # compute split volume
        if sub_box_vol > 0:
            for j in rotations:
                rot_dim = compute_rotation(item_dim, j)
                c = (
                    (i[0] // rot_dim[0]) * (i[1] // rot_dim[1]) * (i[2] // rot_dim[2])
                )  # pre-compute item count
                if c > 0:
                    print(
                        f"Split {i} found at depth {branch} with rotation {j}! {
                            c
                        } items can fit."
                    )
                    print(f"presplit: {box_vol}, postsplit: {sub_box_vol}")
                    # recurse a branch deeper
                    count_split = compute_item_count(
                        i, compute_rotation(item_dim, j), branch + 1
                    )
                    if count_split > best_count:
                        best_count = count_split
        best_count_total += best_count
    count += best_count_total

    return count


if __name__ == "__main__":
    rotations = [(0, 0, 0), (1, 0, 0), (0, 1, 0), (0, 0, 1), (1, 1, 0), (1, 0, 1)]
    rotations_s = [(0, 0, 0)]  # for testing single rotation runs

    box_dim = [float(i) for i in input("box dimension (x,y,z): ").split(",")]
    while box_dim[0] <= 0 or box_dim[1] <= 0 or box_dim[2] <= 0:
        print("Invlalid input, try again!")
        box_dim = [float(i) for i in input("box dimension (x,y,z): ").split(",")]

    box_vol = box_dim[0] * box_dim[1] * box_dim[2]

    item_dim = [float(i) for i in input("item dimension (x,y,z): ").split(",")]
    while item_dim[0] <= 0 or item_dim[1] <= 0 or item_dim[2] <= 0:
        print("Invlalid input, try again!")
        item_dim = [float(i) for i in input("item dimension (x,y,z): ").split(",")]
    item_vol = item_dim[0] * item_dim[1] * item_dim[2]

    max_count = box_vol // item_vol
    if max_count > 0:
        print(f"The maximum is {max_count} items")

        best_rotation = (0, 0, 0)
        best_eff = 0
        best_count = 0

        for i in rotations:
            print(f"Trying rotation {i}")
            item_count = compute_item_count(box_dim, compute_rotation(item_dim, i), 0)
            print(f"{item_count} items can fit in the box")
            print(f"{box_vol - item_count * item_vol} units of space will be left")

            efficiency = item_count / max_count * 100
            print(f"Packing efficiency of {item_count / max_count * 100}%")

            if efficiency > best_eff:
                best_eff = efficiency
                best_rotation = i
                best_count = item_count
        # TODO: prioritize answers with the least amount of branches
        print(
            f"The most efficient rotation is x:{best_rotation[0] * 90}, y:{
                best_rotation[1] * 90
            }, z:{best_rotation[2] * 90} with an effiency of {best_eff}%"
        )
        print(f"It could fit a max of {best_count} items")
    else:
        print("No items can fit")
