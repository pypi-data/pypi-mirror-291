#!/usr/bin/env python

'''Driver UI'''

import tkinter as tk

from ac_websocket_client.objects import (
    GriddedButton, GriddedFrame, GriddedLabel, GriddedTreeview, TrafficLight)


class DriverUI(GriddedFrame):
    '''Driver UI'''

    def __init__(self, parent):

        super().__init__(grid_row=3, grid_col=0, height_by=3)

        self.parent = parent

        self.configure_columns(1, 1, 1, 1, 1, 1, 1)

        GriddedLabel(self, grid_row=0,
                     grid_col=0, width=8, text="Grid")

        self._button = tk.StringVar(value='Show Drivers')
        GriddedButton(self, grid_row=0, grid_col=2,
                      textvar=self._button, width=10,
                      command=lambda: self.parent.loop.create_task(self._toggle_grid()))
        GriddedButton(self, grid_row=0, grid_col=3,
                      text='Order 1..n', width=10,
                      command=lambda: self.parent.loop.create_task(self.parent.update_grid(by_finishing=True)))
        GriddedButton(self, grid_row=0, grid_col=4,
                      text='Order n..1', width=10,
                      command=lambda: self.parent.loop.create_task(self.parent.update_grid(by_reverse=True)))
        GriddedButton(self, grid_row=0, grid_col=5,
                      text='Show', width=10,
                      command=lambda: self.parent.loop.create_task(self.parent.update_grid()))
        GriddedButton(self, grid_row=0, grid_col=6,
                      text='Save', width=10,
                      command=lambda: self.parent.loop.create_task(self.parent.update_grid(write=True)))

        self._light = TrafficLight(self, row=0, column=7)
        self._light.gray()

        self.driver_tree = GriddedTreeview(self, 1, 0, grid_span=8)
        self.driver_tree.add_columns('Name', 'GUID', 'Car', 'Ballast',
                                     'Restrictor', 'Position', 'Connected')
        self.driver_tree.set_widths(190, 80, 190, 80, 80, 80, 80)

        self.update_ui()

    def _show_drivers(self):
        # pylint: disable=consider-using-dict-items

        self.driver_tree.delete(*self.driver_tree.get_children())
        for key in self.parent.drivers:
            self.driver_tree.insert('', tk.END,
                                    values=(self.parent.drivers[key]['name'],
                                            self.parent.drivers[key]['guid'],
                                            self.parent.drivers[key]['car'],
                                            self.parent.drivers[key]['ballast'],
                                            self.parent.drivers[key]['restrictor'],
                                            'n/a', 'Yes'))

    def _show_entries(self):
        # pylint: disable=consider-using-dict-items

        self.driver_tree.delete(*self.driver_tree.get_children())
        for key in self.parent.entries:
            self.driver_tree.insert('', tk.END,
                                    values=(self.parent.entries[key]['drivername'],
                                            self.parent.entries[key]['guid'],
                                            self.parent.entries[key]['model'],
                                            self.parent.entries[key]['ballast'],
                                            self.parent.entries[key]['restrictor'],
                                            str(key + 1),
                                            self.parent.entries[key]['connected']))

    async def _toggle_grid(self):

        if 'Show Drivers' in self._button.get():
            self._show_drivers()
            self._button.set('Show Active')
        else:
            self._show_entries()
            self._button.set('Show Drivers')

        self.update_ui()

    def update_ui(self):
        '''Update the UI based on states'''

        if 'Show Drivers' in self._button.get():
            self._show_entries()
        else:
            self._show_drivers()
