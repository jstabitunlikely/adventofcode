from Day import Day


class Day09(Day):

    def __init__(self,
                 auto_fetch: bool = True,
                 auto_parse: bool = True) -> None:
        super().__init__(year='2024', day='09', auto_fetch=auto_fetch, auto_parse=auto_parse)

    def parse_puzzle(self) -> None:
        self.puzzle = [int(n) for n in list(self.puzzle_raw.strip())]

    def solve_part_1(self,
                     move_files: bool = False) -> int:
        # Separate files and spaces
        spaces = self.puzzle[1::2]
        files = self.puzzle[::2]
        # ID of the last file on the disk
        last_fid = len(files) - 1
        # Current block index
        index = 0
        # File IDs used to track processed files
        bottom_fid = 0
        top_fid = 0
        # ID of the current space
        sid = 0
        # ID of the current file
        #  fid is the same as bottom_id so we dont need it
        # Flag for alternating between files and spaces
        is_file = True
        # Compacting the files
        compact_disk = []
        # Go until all files are processed
        while bottom_fid < len(files):
            # File block
            if is_file:
                # At least one file block is here
                if files[bottom_fid]:
                    compact_disk.append(bottom_fid)
                    # Decrement the file block counter to signal it's been put into place
                    files[bottom_fid] -= 1
                    # There are no more blocks left in this file
                    if not files[bottom_fid]:
                        # Process a space in the next iteration
                        is_file = False
                        # Prepare for the next file (two iterations later)
                        bottom_fid += 1
                # A file block used to be here but it was moved,
                #   skip the whole group by incrementing <index>
                else:
                    # Process a space in the next iteration
                    is_file = False
                    # These spaces will not be filled (as per spec)
                    orig_file_size = self.puzzle[bottom_fid*2]
                    for _ in range(orig_file_size):
                        compact_disk.append(-1)
                    index += orig_file_size
                    # Prepare the next file
                    bottom_fid += 1
                    # Index was incremented already, skip the rest of the iteration
                    continue

            # Space block
            else:
                # No spaces between two files at all
                if not spaces[sid]:
                    # Process a file in the next iteration
                    is_file = True
                    # Prepare for the next space (two iterations later)
                    sid += 1
                    # Move on without doing anything else
                    # Note: even block index won't be incremented
                    continue

                # Find a file (on the right from the space) to move here
                # Note: not using iterators because we'll update the list on the fly
                for fid in range(len((files[bottom_fid:]))):
                    # Reverse order
                    top_fid = last_fid - fid
                    # Found a file
                    if files[top_fid]:
                        # Check if it fits only when whole files can be moved
                        if not move_files or files[top_fid] <= spaces[sid]:
                            compact_disk.append(top_fid)
                            # Decrement the file block counter to signal it's been put into place
                            files[top_fid] -= 1
                            # Decrement the space block counter to signal it's been filled
                            spaces[sid] -= 1
                            break
                # No files to move (either no files at all or bigger files only)
                else:
                    # These spaces cannot be filled
                    for i in range(spaces[sid]):
                        compact_disk.append(-1)
                    # Process a file in the next iteration
                    is_file = True
                    # Prepare for the next space (two iterations later)
                    sid += 1

            # Index is alway incremented
            index += 1

        # Debug info
        # Note: spaces are denoted by -1, changing them to '.'
        msg = "".join([str(d) if d > -1 else '.' for d in compact_disk])  # noqa: F841
        # print(f"Disk: {msg}")

        # Checksum calculation
        # Note: spaces are denoted by -1,
        #   changing them to 0, so they wouldn't affect the checksum
        checksum = sum([max(d, 0)*i for i, d in enumerate(compact_disk)])
        return checksum

    def solve_part_2(self):
        return self.solve_part_1(move_files=True)


def main() -> dict[str, str]:  # pragma: no cover
    today = Day09()
    today.solve()
    return today.answer


if __name__ == "__main__":  # pragma: no cover
    answer = main()
    print(f'Part 1: {answer['part_1']}')
    print(f'Part 2: {answer['part_2']}')
