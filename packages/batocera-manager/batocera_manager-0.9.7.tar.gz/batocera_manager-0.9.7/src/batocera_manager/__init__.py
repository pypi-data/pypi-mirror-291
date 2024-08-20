"""Batocera manager."""
from __future__ import annotations

import asyncio
import logging
from typing import Any

import aiohttp
from ssh_terminal_manager import (
    _LOGGER,
    DEFAULT_ADD_HOST_KEYS,
    DEFAULT_COMMAND_TIMEOUT,
    DEFAULT_PING_TIMEOUT,
    DEFAULT_PORT,
    DEFAULT_SSH_TIMEOUT,
    Collection,
    Command,
    CommandOutput,
    OfflineError,
    Sensor,
    SSHAuthenticationError,
    SSHConnectError,
    SSHHostKeyUnknownError,
    SSHManager,
    State,
)

from .default_collections import ActionKey, SensorKey, batocera
from .errors import HTTPError
from .game import Game
from .system import System

AVAILABLE = "available"
RUNNING_GAME = "running_game"

DEFAULT_USERNAME = "root"
DEFAULT_PASSWORD = "linux"
DEFAULT_HTTP_PORT = 1234
DEFAULT_HTTP_TIMEOUT = 4
DEFAULT_ALLOW_TURN_OFF = True

_LOGGER = logging.getLogger(__name__)


class BatoceraState(State):
    available: bool = False
    running_game: Game | None = None


class BatoceraManager(SSHManager):
    def __init__(
        self,
        host: str,
        *,
        name: str | None = None,
        port: int = DEFAULT_PORT,
        username: str = DEFAULT_USERNAME,
        password: str = DEFAULT_PASSWORD,
        http_port: int = DEFAULT_HTTP_PORT,
        key_filename: str | None = None,
        host_keys_filename: str | None = None,
        add_host_keys: bool = DEFAULT_ADD_HOST_KEYS,
        allow_turn_off: bool = DEFAULT_ALLOW_TURN_OFF,
        ssh_timeout: int = DEFAULT_SSH_TIMEOUT,
        ping_timeout: int = DEFAULT_PING_TIMEOUT,
        command_timeout: int = DEFAULT_COMMAND_TIMEOUT,
        http_timeout: int = DEFAULT_HTTP_TIMEOUT,
        collection: Collection = batocera,
        logger: logging.Logger = _LOGGER,
    ) -> None:
        super().__init__(
            host,
            name=name,
            port=port,
            username=username,
            password=password,
            key_filename=key_filename,
            host_keys_filename=host_keys_filename,
            add_host_keys=add_host_keys,
            allow_turn_off=allow_turn_off,
            ssh_timeout=ssh_timeout,
            ping_timeout=ping_timeout,
            command_timeout=command_timeout,
            collection=collection,
            logger=logger,
        )
        self.http_port = http_port
        self.http_timeout = http_timeout
        self.state = BatoceraState(self)
        self.session = aiohttp.ClientSession(
            self.base_url, timeout=aiohttp.ClientTimeout(self.http_timeout)
        )

    @property
    def is_up(self) -> bool:
        return super().is_up and self.state.available

    @property
    def base_url(self):
        return f"http://{self.host}:{self.http_port}"

    async def _async_send_http_request(
        self, string: str, data: Any = None, force: bool = False
    ) -> dict | None:
        if not self.state.available and not force:
            raise HTTPError("Server not available")

        if data:
            context_manager = self.session.post(string, data=data)
        else:
            context_manager = self.session.get(string)

        try:
            async with context_manager as response:
                if response.status == 200:
                    try:
                        return await response.json()
                    except aiohttp.ContentTypeError:
                        return None
        except Exception as exc:
            self.state.update(AVAILABLE, False)
            self.state.update(RUNNING_GAME, None)
            raise HTTPError("Server request failed") from exc

    async def async_update_state(self, *, raise_errors: bool = False) -> None:
        """Update state.

        Raises:
            OfflineError (only with `raise_errors=True`)
            SSHHostKeyUnknownError
            SSHAuthenticationError
            SSHConnectError (only with `raise_errors=True`)
            HTTPError (only with `raise_errors=True`)
        """
        await super().async_update_state(raise_errors=raise_errors)

        if not self.state.online:
            self.state.update(AVAILABLE, False)
            self.state.update(RUNNING_GAME, None)
            return

        try:
            data = await self._async_send_http_request("/runningGame", force=True)
        except HTTPError:
            if raise_errors:
                raise
            return

        self.state.update(AVAILABLE, True)

        if data:
            running_game = Game(data, self.base_url)
        else:
            running_game = None

        self.state.update(RUNNING_GAME, running_game)

    async def async_close(self) -> None:
        await super().async_close()
        await self.session.close()
        self.state.update(AVAILABLE, False)
        self.state.update(RUNNING_GAME, None)

    async def async_get_game(self, game_id: str) -> Game | None:
        """Get a single game."""
        data = await self._async_send_http_request(f"/systems/all/games/{game_id}")
        return Game(data, self.base_url) if data else None

    async def async_get_games(self) -> list[Game]:
        """Get all games."""
        data = await self._async_send_http_request("/systems/all/games")
        return [Game(item, self.base_url) for item in data]

    async def async_get_games_by_system(self, system_name: str) -> list[Game] | None:
        """Get all games of a system."""
        data = await self._async_send_http_request(f"/systems/{system_name}/games")
        return [Game(item, self.base_url) for item in data] if data else None

    async def async_get_system(self, system_name: str) -> System | None:
        """Get a single system."""
        data = await self._async_send_http_request(f"/systems/{system_name}")
        return System(data, self.base_url) if data else None

    async def async_get_systems(self) -> list[System]:
        """Get all systems."""
        data = await self._async_send_http_request("/systems")
        return [System(item, self.base_url) for item in data]

    async def async_start_game(self, game_id: str) -> Game | None:
        """Start a game."""
        game = await self.async_get_game(game_id)
        if game is None:
            return None
        await self.async_stop_game()
        await self._async_send_http_request("/launch", data=game.path)
        await asyncio.sleep(2)
        self.state.update(RUNNING_GAME, game)
        return game

    async def async_stop_game(self) -> None:
        """Stop the running game."""
        await self._async_send_http_request("/emukill")
        self.state.update(RUNNING_GAME, None)

    async def async_volume_up(self) -> bool:
        """Turn the volume up."""
        await self.async_set_sensor_value(
            SensorKey.AUDIO_VOLUME, lambda volume: volume + 3, raise_errors=True
        )

    async def async_volume_down(self) -> bool:
        """Turn the volume down."""
        await self.async_set_sensor_value(
            SensorKey.AUDIO_VOLUME, lambda volume: volume - 3, raise_errors=True
        )

    async def async_set_volume(self, volume: int) -> bool:
        """Set the volume."""
        await self.async_set_sensor_value(
            SensorKey.AUDIO_VOLUME, volume, raise_errors=True
        )

    async def async_mute(self, mute: bool) -> bool:
        """Mute or unmute."""
        await self.async_set_sensor_value(SensorKey.AUDIO_MUTE, mute)
