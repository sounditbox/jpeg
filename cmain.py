import logic
import sys

def main():
    filename = sys.argv[1]
    sectors = logic.parse(filename)
    for key, value in sectors.items():
        print(key, value)


if __name__ == '__main__':
    main()