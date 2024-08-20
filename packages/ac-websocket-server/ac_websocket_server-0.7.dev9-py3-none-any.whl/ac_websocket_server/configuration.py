'''Assetto Corsa server.cfg helper Class'''

import configparser
import logging
import os
import shutil


from ac_websocket_server.objects import SessionEvent
from ac_websocket_server.error import WebsocketsServerError


class ServerConfiguration:
    '''The server configuration'''

    def __init__(self, file_name: str = None) -> None:
        '''
        Create a new ServerConfiguration.
        '''

        self.__logger = logging.getLogger('ac-ws.configuration')

        self.__cfg = configparser.ConfigParser()
        self.__cfg.optionxform = str

        self.__dirty = False

        self.__file_name = file_name
        self.__dir_name = os.path.dirname(self.__file_name)

        if not os.path.exists(self.__file_name):
            error_message = f'Missing server_cfg.ini file in {self.__dir_name}'
            self.__logger.error(error_message)
            raise WebsocketsServerError(error_message)

        try:
            self.__cfg.read(self.__file_name)
        except configparser.Error as e:
            error_message = f'Unable to parse server_cfg.ini file in {self.__dir_name}'
            raise WebsocketsServerError(error_message) from e

    @property
    def cars(self):
        '''Allowed cars'''
        return self.__cfg['SERVER']['CARS']

    @cars.setter
    def cars(self, value):
        self.__cfg['SERVER']['CARS'] = value
        self.__dirty = True

    @property
    def http_port(self):
        '''HTTP port'''
        return self.__cfg['SERVER']['HTTP_PORT']

    @property
    def name(self):
        '''Name of server'''
        return self.__cfg['SERVER']['NAME']

    @name.setter
    def name(self, value):
        self.__cfg['SERVER']['NAME'] = value
        self.__dirty = True

    def session_disable(self, session_name: str):
        '''Disable a session'''

        session_name = session_name.capitalize()

        if self.__cfg.has_section(session_name):
            self.__cfg.remove_section(session_name)
            self.__dirty = True

    def session_enable(self, session_name: str):
        '''Enable a session'''

        session_name = session_name.capitalize()

        if not self.__cfg.has_section(session_name):
            self.__cfg.add_section(session_name)
            self.__cfg.set(session_name, 'NAME', session_name)
            self.__cfg.set(session_name, 'IS_OPEN', '1')
            if session_name == 'PRACTICE' or session_name == 'QUALIFY':
                self.__cfg.set(session_name, 'TIME', '10')
            if session_name == 'RACE':
                self.__cfg.set(session_name, 'LAPS', '10')
                self.__cfg.set(session_name, 'WAIT_TIME', '60')
            self.__dirty = True

    def session_modify(self, session_name: str,
                       laps: int | None = None,
                       time: int | None = None):
        '''Modify a session'''

        session_name = session_name.capitalize()

        if laps and session_name == 'RACE':
            self.__cfg.set(session_name, 'LAPS', laps)
            self.__cfg.remove_option(session_name, 'TIME')
            self.__dirty = True
        if time:
            self.__cfg.set(session_name, 'TIME', time)
            self.__cfg.remove_option(session_name, 'LAPS')
            self.__dirty = True

    @property
    def sessions(self):
        '''Dict of sessions'''

        sessions = {}

        for session in ['PRACTICE', 'QUALIFY', 'RACE']:
            if self.__cfg.has_section(session):
                name = self.__cfg[session].get('NAME')
                time = self.__cfg[session].get('TIME', 0)
                laps = self.__cfg[session].get('LAPS', 0)
                sessions[name] = SessionEvent(name, laps=laps, time=time)

        return sessions

    @property
    def tcp_port(self):
        '''TCP port'''
        return self.__cfg['SERVER']['TCP_PORT']

    @property
    def track(self):
        '''Name of track'''
        return self.__cfg['SERVER']['TRACK']

    @track.setter
    def track(self, value):
        self.__cfg['SERVER']['TRACK'] = value
        self.__dirty = True

    @property
    def udp_port(self):
        '''UDP port'''
        return self.__cfg['SERVER']['UDP_PORT']

    def write(self):
        '''Write the server config file'''
        # pylint: disable=logging-fstring-interpolation

        if not self.__dirty:
            self.__logger.error(f'{self.__file_name} is not dirty')

        try:

            if not os.path.exists(self.__file_name + '.old'):
                shutil.copy(self.__file_name, self.__file_name + '.old')
                self.__logger.debug(
                    f'Created {self.__file_name}.old before changes')

            with open(self.__file_name, 'w', encoding='utf-8') as f:
                self.__cfg.write(f, space_around_delimiters=False)
                self.__dirty = False

        except (IOError, OSError) as e:
            error_message = f'Unable to write server_cfg.ini file in {self.__dir_name}'
            self.__logger.error(error_message)
            raise WebsocketsServerError(error_message) from e
