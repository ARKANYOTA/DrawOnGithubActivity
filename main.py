import argparse
import os
from PIL import Image
from datetime import date, timedelta
import numpy as np

days = ["L", "Ma", "Me", "J", "V", "S", "D"]

def argsError(e):
    print(f'[Error] - {e}')
    exit(0)

def get_first_day():
    if not argv.year:
        argsError("Year needed")
        return
    if not argv.year.isdigit():
        argsError("Year need to be a int")
        return
    d = date(int(argv.year), 1, 1)
    return days[d.weekday()]

def get_image_data():
    if not argv.image:
        argsError("Image Path needed")
        return
    im = Image.open(argv.image)
    image_sequence = im.getdata()
    image_array = np.array(image_sequence)
    arr = [" " if px[1] > 120 else "1" for px in image_array]
    print(arr)
    for ind, i in enumerate(arr):
        if ind % 52 == 0:
            print()
        print(i, end="")

    print()
    new_arr = ["."]*len(arr)
    print(new_arr)
    ecx = 0
    for i in arr:
        new_arr[ecx] = i
        if ecx+7 >= len(arr):
            ecx  = (ecx+7)%len(arr)+1
        else:
            ecx = (ecx+7)
    for ind, i in enumerate(new_arr):
        if ind % 7 == 0:
            print()
        print(i, end="")
    return new_arr



def start_draw(new_arr):
    # Get first dimanche
    ecx = 0
    d = date(int(argv.year), 1, 1)
    OneDay = timedelta(days=1)
    while d.weekday() != 6:
        d += OneDay
    print()
    print(d, d.weekday(), ecx)
    while d.year==int(argv.year) and ecx < len(new_arr):
        if new_arr[ecx] == " ":
            push_this_date(d, new_arr[ecx])
        d += OneDay
        ecx += 1

def push_this_date(d, pixel):
    print(d, pixel)
    sdate = str(d) + " 12:05:05"
    os.chdir(argv.path)
    with open(str(d), "w") as f:
        f.write(sdate)
    os.system("git add .")
    os.environ['GIT_COMMITTER_DATE'] = sdate
    os.environ['GIT_AUTHOR_DATE'] = sdate
    os.system("git commit -m \""+sdate+" by https://github.com/ARKANYOTA/DrawOnGithubActivity\"")


def main(argv=None):
    get_first_day()
    new_arr = get_image_data()
    start_draw(new_arr)

    print("Do a \"git push\"")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--year", help="Année à laquel, et renvoie la taille requise à l'image")
    parser.add_argument("--image", help="Image à draw")
    parser.add_argument("--path", help="Github project path")
    argv = parser.parse_args()
    main(argv)



