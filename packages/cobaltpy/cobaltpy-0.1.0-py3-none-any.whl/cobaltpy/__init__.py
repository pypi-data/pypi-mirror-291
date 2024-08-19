"""
Copyright 2024 Smugaski

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

from aiohttp import ClientSession
from dataclasses import dataclass
from enum import Enum
from typing import Literal, Optional, TypedDict, NotRequired
import asyncio

INSTANCES_URL = "https://instances.hyper.lol/instances.json"


class TrustLevel(Enum):
    """Trust level of an instance."""

    OFFLINE = "offline"
    NOT_SAFE = "not_safe"
    UNKNOWN = "unknown"
    SAFE = "safe"


@dataclass
class InstanceServices:
    """Services supported by an instance."""

    youtube: bool
    facebook: bool
    rutube: bool
    tumblr: bool
    bilibili: bool
    pinterest: bool
    instagram: bool
    soundcloud: bool
    youtube_music: bool
    odnoklassniki: bool
    dailymotion: bool
    snapchat: bool
    twitter: bool
    loom: bool
    vimeo: bool
    streamable: bool
    vk: bool
    tiktok: bool
    reddit: bool
    twitch_clips: bool
    youtube_shorts: bool
    vine: bool


@dataclass
class Instance:
    """An instance of Cobalt."""

    trust: TrustLevel
    api_online: bool
    cors: bool
    commit: str
    version: str
    branch: str
    score: int
    protocol: Literal["http", "https"]
    name: str
    start_time: int
    api: str
    front_end: str
    services: InstanceServices

    @classmethod
    def from_dict(cls, data: dict) -> "Instance":
        return cls(
            trust=TrustLevel(data["trust"]),
            api_online=data["api_online"],
            cors=data["cors"],
            commit=data["commit"],
            version=data["version"],
            branch=data["branch"],
            score=data["score"],
            protocol=data["protocol"],
            name=data["name"],
            start_time=data["startTime"],
            api=data["api"],
            front_end=data["frontEnd"],
            services=InstanceServices(**data["services"]),
        )


@dataclass
class CobaltFile:
    file: bytes
    file_name: str

class DownloadOptions(TypedDict):
    """Options for downloading.
    
    Attributes
    -----------
    vCodec: :class:`str`
        - default: h264
        - description: applies only to youtube downloads. h264 is recommended for phones.
    vQuality: :class:`str`
        - default: 720
        - description: 720 quality is recommended for phones.
    aFormat: :class:`str`
        - default: mp3
    filenamePattern: :class:`str`
        - default: classic
        - description: changes the way files are named. previews can be seen in the web app.
    isAudioOnly: :class:`bool`
        - default: false
    isTTFullAudio: :class:`bool`
        - default: false
        - description: enables download of original sound used in a tiktok video.
    isAudioMuted: :class:`bool`
        - default: false
        - description: disables audio track in video downloads.
    dubLang: :class:`bool`
        - default: false
        - description: backend uses Accept-Language header for youtube video audio tracks when true.
    disableMetadata: :class:`bool`
        - default: false
        - description: disables file metadata when set to true.
    twitterGif: :class:`bool`
        - default: false
        - description: changes whether twitter gifs are converted to .gif
    tiktokH265: :class:`bool`
        - default: false        
    """

    vCodec: NotRequired[Literal["h264", "av1", "vp9"]]
    vQuality: NotRequired[
        Literal["144", "240", "360", "480", "720", "1080", "1440", "2160", "max"]
    ]
    aFormat: NotRequired[Literal["best", "mp3", "ogg", "wav", "opus"]]
    filenamePattern: NotRequired[Literal["classic", "pretty", "basic", "nerdy"]]
    isAudioOnly: NotRequired[bool]
    isTTFullAudio: NotRequired[bool]
    isAudioMuted: NotRequired[bool]
    dubLang: NotRequired[bool]
    disableMetadata: NotRequired[bool]
    twitterGif: NotRequired[bool]
    tiktokH265: NotRequired[bool]


class PickerItem(TypedDict):
    """Item in a picker."""

    url: str
    thumb: str
    type: Optional[Literal["video", "photo", "gif"]]


class DownloadResponse(TypedDict):
    """Response of a download."""

    status: Literal["error", "redirect", "stream", "success", "rate-limit", "picker"]
    text: str
    url: str
    pickerType: Literal["various", "images"]
    picker: list[PickerItem]
    audio: str


class GenericError(Exception):
    """Generic error."""


class InstanceNotSetError(Exception):
    """Instance not set error."""


class RateLimitError(Exception):
    """Rate limit error."""


class DownloadError(Exception):
    """Download error."""


class Cobalt:
    """Cobalt client.

    Attributes
    -----------
    instances :class:`list[Instance]`
        List of instances.
    instance :class:`Instance`
        Instance to use.

    Methods
    --------
    get_instances() -> :class:`list[Instance]`
        Get instances.
    get_best_instance() -> :class:`Instance`
        Get the best instance.
    set_instance() -> None
        Set the instance.
    download(
        url: :class:`str`, 
        options: :class:`DownloadOptions`, 
        timeout: :class:`int`
    ) -> :class:`list[CobaltFile]`
        Download a file.
    """

    instances: list[Instance]
    instance: Instance | None = None

    async def __aenter__(self) -> "Cobalt":
        self._session = ClientSession(
            headers={
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:129.0) Gecko/20100101 Firefox/129.0",
                "Accept": "application/json",
            }
        )

        self.instances = await self.get_instances()

        return self

    async def __aexit__(self, exc_type, exc, tb) -> None:
        await self._session.close()

    async def get_instances(self) -> list[Instance]:
        """Get instances.

        Returns
        -------
        :class:`list[Instance]`
            List of instances.
        """

        async with self._session.get(INSTANCES_URL) as response:
            data = await response.json()

        self.instances = [Instance.from_dict(instance) for instance in data]

        return self.instances

    async def get_best_instance(
        self, trust_level: TrustLevel = TrustLevel.SAFE, exclude: list[str] = []
    ) -> Instance:
        """Get the best instance.

        Parameters
        ----------
        trust_level : :class:`TrustLevel`
            Trust level of the instance.
        exclude : :class:`list[str]`
            Instances to exclude.

        Returns
        -------
        :class:`Instance`
            Best instance.
        """

        return max(
            [
                instance
                for instance in self.instances
                if instance.trust == trust_level and instance.name not in exclude
            ],
            key=lambda instance: instance.score,
        )

    def set_instance(self, instance: Instance) -> None:
        """Set the instance.
        
        Parameters
        ----------
        instance : :class:`Instance`
            Instance to set.
        """
        self.instance = instance

    async def download(
        self, url: str, options: DownloadOptions = {}, timeout: int = 10
    ) -> list[CobaltFile]:
        """Download a file.

        Parameters
        ----------
        url : :class:`str`
            URL of the file.
        options : :class:`DownloadOptions`
            Options for downloading.
        timeout : :class:`int`
            Timeout for downloading.

        Returns
        -------
        :class:`list[CobaltFile]`
            List of downloaded files.
        
        Raises
        ------
        :class:`InstanceNotSetError`
            Instance is not set.
        :class:`GenericError`
            Generic error.
        :class:`RateLimitError`
            Rate limit error.
        :class:`DownloadError`
            Download error.
        :class:`asyncio.TimeoutError`
            Timeout error.
        """
        if self.instance is None:
            raise InstanceNotSetError("Instance is not set.")

        async with self._session.post(
            f"{self.instance.protocol}://{self.instance.api}/api/json",
            headers={"Accept": "application/json"},
            json={"url": url, **options},
        ) as response:
            data: DownloadResponse = await response.json()
            status = data["status"]
            # TODO: implement rate limit handling
            async with asyncio.timeout(timeout):
                match status:
                    case "error":
                        raise GenericError(data["text"])

                    case "rate-limit":
                        raise RateLimitError("Rate limit reached.")

                    case "picker":
                        tasks: list[asyncio.Task] = []

                        async with asyncio.TaskGroup() as group:
                            for item in data["picker"]:
                                tasks.append(group.create_task(self._download(item["url"])))

                        return [CobaltFile(*task.result()) for task in tasks]

                    case "stream" | "redirect":
                        return [CobaltFile(*(await self._download(data["url"])))]

                    case _:
                        raise DownloadError("Download failed.")

    async def _download(self, url: str) -> tuple[bytes, str]:
        async with self._session.get(url) as response:
            if response.headers.get("Content-Length", None) == "0":
                raise DownloadError("Download failed.")

            file_name = response.headers.get("Content-Disposition", None)

            if file_name is not None:
                file_name = file_name.split('"')[1]

            return (
                await response.read(),
                file_name or url.split("/")[-1].split("?")[0],
            )
