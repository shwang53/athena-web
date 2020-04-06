import sys
import os

if __name__ == "__main__":
    user_id = sys.argv[1]
    value = sys.argv[2]
    filename = os.getenv("HOME")+"/works/athena-web/users/%s/rr/answer.txt" % (user_id)

    with open(filename, 'w') as f:
        f.write(value)

    print("Done!")