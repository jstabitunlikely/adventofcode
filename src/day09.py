import sys
import inputfetcher


EXAMPLE = '2333133121414131402'


def parse_input(example: bool) -> str:
    disk = EXAMPLE if example else inputfetcher.fetch_input('2024', '9')
    disk = [int(n) for n in list(disk.strip())]
    return disk


def solve_1(disk: list[int]) -> int:
    # Final checksum
    checksum = 0
    # Separate the file and space groups
    spaces = disk[1::2]
    files = disk[::2]
    # ID of the last file on the disk
    last_fid = len(files) - 1
    # Current block index
    index = 0
    # File ID used to fill file blocks
    bottom_fid = 0
    # File ID used to fill space blocks
    top_fid = last_fid
    # ID of the current space
    sid = 0
    # ID of the current file
    #  fid is the same as bottom_id so we dont need it
    # Flag for alternating between files and spaces
    is_file = True
    # Go until all the files are in there place
    while any(files):
        if is_file:
            # Increment the checksum
            checksum += bottom_fid * index
            # Decrement the file block counter to signal it's been put into place
            files[bottom_fid] -= 1
            # There are no more blocks left in this file
            if not files[bottom_fid]:
                # First, do a space in the next iteration
                is_file = False
                # Prepare for the next file (two iterations later)
                bottom_fid += 1

        else:
            # Edge case: no spaces between two files at all
            if not spaces[sid]:
                # First, do a file in the next iteration
                is_file = True
                # Prepare for the next space (two iterations later)
                sid += 1
                # Move on without doing anything else
                continue
            # Increment the checksum
            checksum += top_fid * index

            # Decrement the file block counter to signal it's been put into place
            files[top_fid] -= 1
            # There are no more blocks left in this file
            if not files[top_fid]:
                # Prepare for the next file (two iterations later)
                top_fid -= 1

            # Decrement the space block counter to signal it's been filled
            spaces[sid] -= 1
            # There are no more empty blocks left
            if not spaces[sid]:
                # First, do a file in the next iteration
                is_file = True
                # Prepare for the next space (two iterations later)
                sid += 1
        # Index is alway incremented
        index += 1
    return checksum


def solve_2(disk: str) -> int:
    return 0


if __name__ == "__main__":
    use_example = "--example" in sys.argv
    disk = parse_input(use_example)
    result_1 = solve_1(disk)
    print(f'Result 1: {result_1}')
    result_2 = solve_2(disk)
    print(f'Result 2: {result_2}')
