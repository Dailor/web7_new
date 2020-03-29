import sys
from PIL import Image
from io import BytesIO
from point_by_addr import get_pos
from close_toponim import find_close
from get_map import get_map
import CONST

TOPONIM_TYPE = "аптека"


def main():
    addr = ' '.join(sys.argv[1:])
    p1_pos = get_pos(addr)
    toponim_info = find_close(TOPONIM_TYPE, p1_pos, CONST.NUMBER_RESULT)
    points = [(info['pos'], info['time'][1]) for info in toponim_info]
    map = get_map(points)
    Image.open(BytesIO(
        map.content)).show()


if __name__ == '__main__':
    main()
