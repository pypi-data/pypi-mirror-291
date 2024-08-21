import sys

from scraper_hj3415.krx import krx300
from utils_hj3415 import utils, noti
import argparse


def nfs():
    from scraper_hj3415.nfscraper import run_nfs
    spiders = {
        'c101': run_nfs.c101,
        'c106': run_nfs.c106,
        'c103y': run_nfs.c103y,
        'c103q': run_nfs.c103q,
        'c104y': run_nfs.c104y,
        'c104q': run_nfs.c104q,
        'c108': run_nfs.c108,
        'all_spider': run_nfs.all_spider
    }

    parser = argparse.ArgumentParser()
    parser.add_argument('spider', help=f"Spiders - {spiders.keys()}")
    parser.add_argument('targets', nargs='+', type=str, help="원하는 종류의 코드를 나열하세요.")
    parser.add_argument('--noti', action='store_true', help='작업완료후 메시지 전송여부')

    args = parser.parse_args()

    if args.spider in spiders.keys():
        if len(args.targets) == 1 and args.targets[0] == 'all':
            #x = input("It will take a long time. Are you sure? (y/N)")
            #if x == 'y' or x == 'Y':
            # krx300 에서 전체코드리스트를 가져와서 섞어준다.
            import random
            all_codes = krx300.get()
            random.shuffle(all_codes)
            spiders[args.spider](*all_codes)
            if args.noti:
                noti.telegram_to('manager', f"모든 코드의 {args.spider}를 저장했습니다.")
        else:
            # args.targets의 코드 유효성을 검사한다.
            is_valid = True
            for code in args.targets:
                # 하나라도 코드 형식에 이상 있으면 에러
                is_valid = utils.is_6digit(code)
            if is_valid:
                spiders[args.spider](*args.targets)
                if args.noti:
                    noti.telegram_to('manager', f"{len(args.targets)}개 코드의 {args.spider}를 저장했습니다.")
            else:
                print(f"{args.targets} 종목 코드의 형식은 6자리 숫자입니다.")
    else:
        print(f"The spider should be in {list(spiders.keys())}")

"""
def miscraper():
    spiders = ['mihistory', 'mi']

    parser = argparse.ArgumentParser()
    parser.add_argument('spider', help=f"Spiders - {spiders}")

    parser.add_argument('-d', '--db_path', help="Set mongo database path")
    args = parser.parse_args()

    if args.spider in spiders:
        if args.spider == 'mihistory':
            years = 2
            print(f"We will collect MI data for past {years} years.")
            mirun.mi_history(years, args.db_path) if args.db_path else mirun.mi_history(years)
        elif args.spider == 'mi':
            mirun.mi_all(args.db_path) if args.db_path else mirun.mi_all()
    else:
        print(f"The spider option should be in {spiders}")
"""
