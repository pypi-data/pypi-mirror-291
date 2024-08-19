#!/usr/bin/env python

'''Server UI'''

import tkinter as tk

from ac_websocket_client.objects import (
    GriddedButton, GriddedEntry, GriddedFrame, GriddedLabel, TrafficLight)


class ServerUI(GriddedFrame):
    '''Server UI'''

    def __init__(self, parent):

        super().__init__(grid_row=1, grid_col=0, height_by=3.5)

        self.parent = parent

        self.configure_columns(1, 1, 4, 1, 1)

        self._buttons = {}
        self._fields = {}
        self._lights = {}

        grid_row = 0

        GriddedLabel(self, grid_row=grid_row, grid_col=0,
                     width=8, text="Game")

        GriddedLabel(self, grid_row=grid_row, grid_col=1,
                     width=8, text="started:")
        self._fields['started'] = tk.StringVar()
        GriddedEntry(self, grid_row=grid_row, grid_col=2,
                     textvariable=self._fields['started'], state=tk.DISABLED)
        self._buttons['game'] = tk.StringVar(value='Start Game')
        GriddedButton(self, grid_row=grid_row, grid_col=3,
                      textvariable=self._buttons['game'],
                      command=lambda: self.parent.loop.create_task(self.parent.toggle_game()))
        self._lights['game'] = TrafficLight(self, row=grid_row, column=4)

        grid_row += 1

        self._fields['registered'] = tk.StringVar()
        GriddedLabel(self, grid_row=grid_row, grid_col=1,
                     width=8, text="registered:")
        GriddedEntry(self, grid_row=grid_row, grid_col=2,
                     textvariable=self._fields['registered'], state=tk.DISABLED)
        self._lights['registered'] = TrafficLight(self, row=grid_row, column=4)
        self._buttons['lobby'] = tk.StringVar(value='(Re)register')
        GriddedButton(self, grid_row=grid_row, grid_col=3,
                      textvariable=self._buttons['lobby'],
                      command=lambda: self.parent.loop.create_task(self.parent.toggle_registration()))
        self._lights['lobby'] = TrafficLight(self, row=grid_row, column=4)

        grid_row += 1

        GriddedLabel(self, grid_row=grid_row,
                     grid_col=0, width=8, text="Config")

        self._fields['cfg'] = tk.StringVar()
        GriddedLabel(self, grid_row=grid_row, grid_col=1, width=8, text="cfg:")
        GriddedEntry(self, grid_row=grid_row, grid_col=2,
                     textvariable=self._fields['cfg'], state=tk.DISABLED)
        self._buttons['save'] = tk.StringVar(value='Edit .cfg')
        GriddedButton(self, grid_row=grid_row, grid_col=3,
                      textvariable=self._buttons['save'],
                      command=lambda: self.parent.loop.create_task(self.parent.unimplemented('Save not implemented')))
        self._lights['save'] = TrafficLight(self, row=grid_row, column=4)

        grid_row += 1

        self._fields['name'] = tk.StringVar()
        GriddedLabel(self, grid_row=grid_row,
                     grid_col=1, width=8, text="name:")
        GriddedEntry(self, grid_row=grid_row, grid_col=2,
                     textvariable=self._fields['name'], state=tk.DISABLED)

        grid_row += 1

        self._fields['track'] = tk.StringVar()
        GriddedLabel(self, grid_row=grid_row,
                     grid_col=1, width=8, text="track:")
        GriddedEntry(self, grid_row=grid_row, grid_col=2,
                     textvariable=self._fields['track'], state=tk.DISABLED)

        grid_row += 1

        self._fields['cars'] = tk.StringVar()
        GriddedLabel(self, grid_row=grid_row,
                     grid_col=1, width=8, text="cars:")
        GriddedEntry(self, grid_row=grid_row, grid_col=2,
                     textvariable=self._fields['cars'], state=tk.DISABLED)

        self._buttons['sessions'] = {}
        self._fields['sessions'] = {}
        self._lights['sessions'] = {}

        grid_row += 1

        self._fields['sessions']['Practice'] = tk.StringVar()
        GriddedLabel(self, grid_row=grid_row, grid_col=1,
                     width=8, text="practice:")
        GriddedEntry(self, grid_row=grid_row, grid_col=2,
                     textvariable=self._fields['sessions']['Practice'], state=tk.DISABLED)
        self._buttons['sessions']['Practice'] = tk.StringVar(value='Enable')
        GriddedButton(self, grid_row=grid_row, grid_col=3,
                      textvariable=self._buttons['sessions']['Practice'],
                      command=lambda: self.parent.loop.create_task(self.parent.unimplemented('Enable not implemented')))
        self._lights['sessions']['Practice'] = TrafficLight(
            self, row=grid_row, column=4)

        grid_row += 1

        self._fields['sessions']['Qualify'] = tk.StringVar()
        GriddedLabel(self, grid_row=grid_row, grid_col=1,
                     width=8, text="qualify:")
        GriddedEntry(self, grid_row=grid_row, grid_col=2,
                     textvariable=self._fields['sessions']['Qualify'], state=tk.DISABLED)
        self._buttons['sessions']['Qualify'] = tk.StringVar(value='Enable')
        GriddedButton(self, grid_row=grid_row, grid_col=3,
                      textvariable=self._buttons['sessions']['Qualify'],
                      command=lambda: self.parent.loop.create_task(self.parent.unimplemented('Enable not implemented')))
        self._lights['sessions']['Qualify'] = TrafficLight(
            self, row=grid_row, column=4)

        grid_row += 1

        self._fields['sessions']['Race'] = tk.StringVar()
        GriddedLabel(self, grid_row=grid_row, grid_col=1,
                     width=8, text="race:")
        GriddedEntry(self, grid_row=grid_row, grid_col=2,
                     textvariable=self._fields['sessions']['Race'], state=tk.DISABLED)
        self._buttons['sessions']['Race'] = tk.StringVar(value='Enable')
        GriddedButton(self, grid_row=grid_row, grid_col=3,
                      textvariable=self._buttons['sessions']['Race'],
                      command=lambda: self.parent.loop.create_task(self.parent.unimplemented('Enable not implemented')))
        self._lights['sessions']['Race'] = TrafficLight(
            self, row=grid_row, column=4)

        self.update_ui()

    def update_ui(self):
        '''Update the UI with the contents of the parent.server'''

        self._fields['cfg'].set(self.parent.server.get('child_ini_file', ''))
        self._fields['name'].set(self.parent.server.get('name', ''))
        self._fields['track'].set(self.parent.server.get('track', ''))
        self._fields['cars'].set(self.parent.server.get('cars', ''))

        if not self.parent.states.is_connected:
            self._lights['game'].gray()
            self._lights['lobby'].gray()
            for session in ('Practice', 'Qualify', 'Race'):
                if self.parent.sessions.get(session, None):
                    self.parent.sessions[session]['active'] = False
                    self._lights['sessions'][session].gray()

        if self.parent.states.is_started:
            self._fields['started'].set(
                self.parent.server.get('timestamp', None))
            self._buttons['game'].set('Stop Game')
            self._lights['game'].green()
        else:
            self._fields['started'].set('n/a')
            self._buttons['game'].set('Start Game')
            self._lights['game'].red()

        if self.parent.states.is_registered and self.parent.states.is_started:
            self._fields['registered'].set(
                self.parent.lobby.get('since', ''))
            self._buttons['lobby'].set('Re-register')
            self._lights['lobby'].green()
        else:
            self._fields['registered'].set('n/a')
            self._buttons['lobby'].set('Register')
            self._lights['lobby'].red()

        if self.parent.states.cfg_needs_saving:
            self._lights['save'].red()
        else:
            self._lights['save'].gray()

        if sessions := self.parent.sessions:
            for session_type in sessions:
                if session_type not in ('Practice', 'Qualify', 'Race'):
                    return
                self._buttons['sessions'][session_type].set('Disable')
                session_active = sessions[session_type]['active']
                if session_active:
                    self._lights['sessions'][session_type].green()
                else:
                    self._lights['sessions'][session_type].gray()
                session_description = str(
                    sessions[session_type]['time'])
                if sessions[session_type]['laps'] == 0:
                    session_description += ' minutes'
                else:
                    session_description += ' laps'
                self._fields['sessions'][session_type].set(session_description)
