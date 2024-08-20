<p align="center">
 📦 <a href="https://pypi.org/project/clinton" style="text-decoration:none;">CLINTON</a>
</p>

```python
import asyncio
from Clinton.functions import Media

async def main():
    duration = 7000 # IN SECONDS
    save = "./Home/" # OUTPUT LOCATION
    file = "./Home/Video.mp4" # FILE LOCATION
    result = await Media.screenshot(file, location, duration)
    print(result)

asyncio.run(main())
```
