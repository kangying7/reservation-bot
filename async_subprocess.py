import asyncio
from calendar import FRIDAY, MONDAY, THURSDAY, TUESDAY, WEDNESDAY

async def run(cmd):
    proc = await asyncio.create_subprocess_shell(
        cmd,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE)

    stdout, stderr = await proc.communicate()

    print(f'[{cmd!r} exited with {proc.returncode}]')
    if stdout:
        print(f'[stdout]\n{stdout.decode()}')
    if stderr:
        print(f'[stderr]\n{stderr.decode()}')

async def main():
    time = "07:30"
    coros = [run(f'python ./automate_reservation.py --time {time} --day {weekday}') for weekday in [MONDAY, TUESDAY, WEDNESDAY, THURSDAY, FRIDAY]]
    await asyncio.gather(*coros)
    # await asyncio.gather(
    #     run('python ./automate_reservation.py --time "08:40" --day 1'),
    #     run('python ./automate_reservation.py --time "08:40" --day 2'))

if __name__ == "__main__":
    asyncio.run(main())