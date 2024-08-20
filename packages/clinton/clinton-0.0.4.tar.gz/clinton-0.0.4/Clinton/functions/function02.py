import os
import time
import ffmpeg
import random
import asyncio
from ..scripts import Scripted
from .collections import SMessage
#====================================================================================================

class Media:

    async def interval(duramini, duration, numbers):
        moonus = random.sample(range(duramini, duration), numbers)
        moonus.sort()
        return moonus

#====================================================================================================

    async def metadata(incoming, outgoing, maps="0", command=None):
        if not command or incoming == None:
            return incoming
        try:
            mainse = ffmpeg.input(incoming)
            nemose = mainse.output(outgoing, map=maps, **command, c="copy")
            moonus = nemose.run(quiet=True)
            os.remove(incoming)
            return SMessage(result=outgoing)
        except ffmpeg.Error as errors:
            moonus = str(errors.stderr.decode('utf-8'))
            return SMessage(result=None, errors=moonus)
        except Exception as errors:
            return SMessage(result=None, errors=errors)

#====================================================================================================

    async def short(stime, etime, file, flocation, extension):
        try:
            output = flocation + str(round(time.time())) + extension
            ffmpeg.input(file, ss=stime, t=etime).output(output).run(quiet=True)
            ouoing = output if os.path.lexists(output) else None
            return ouoing
        except Exception:
            return None

#====================================================================================================

    async def screenshot(file, location, duration, extension=Scripted.DATA11):
        try:
            output = location + str(round(time.time())) + extension
            ffmpeg.input(file, ss=duration).output(output, vframes=1).run(quiet=True)
            ouoing = output if os.path.lexists(output) else None
            return ouoing
        except ffmpeg.Error as errors:
            print(errors)
            return None
        except Exception as errors:
            print(errors)
            return None

#====================================================================================================

    async def screenshots(file, location, numbers, duration, durations=5, images=None):
        imageess = images if images else []
        if duration < durations:
            return imageess
        interval = await Video.interval(durations, duration, numbers)
        for looper in range(numbers):
            valuesom = interval[0]
            imagesve = await Video.screenshot(file, location, valuesom)
            if imagesve == None:
                continue
            imageess.append(imagesve)
            interval.remove(valuesom)
            await asyncio.sleep(3)
        else:
            return imageess

#====================================================================================================
