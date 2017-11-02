#! /usr/bin/env python3
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
# Last modified: 2017-10-30 00:50:33

import json
import os
import sys
import logging
import traceback
import click

DEFAULT_CONFIG_PATH = ".hackmd_notify_config"


class HackMDConfig(object):

    def __init__(self, path=None):
        self.config = dict()
        self.config_file_path = path

        if self.config_file_path is None:
            self.config_file_path = DEFAULT_CONFIG_PATH

    def check_config(self):
        '''check the .hackmd_notify_config is exists'''

        if not os.path.exists(self.config_file_path) or not os.path.isfile(self.config_file_path):
            return False
        if not self.load_config():
            return False
        return True

    def config_input(self):
        '''make config file input'''
        click.echo("Input the hackmd notifier settings:")
        self.config["account"] = click.prompt(
            "gmail account").strip()
        self.config["password"] = click.prompt("gmail password", hide_input=True)
        self.config["recipient"] = click.prompt(
            "recipient gmail").strip()

    def save_config(self):
        '''write config into file'''
        try:
            if(len(self.config) < 1):
                self.config_input()
            with open(self.config_file_path, 'w') as outfile:
                json.dump(
                    self.config, fp=outfile, separators=(',', ':'), sort_keys=True,
                )
            return True
        except:
            logging.debug(traceback.print_exc())
            return False

    def load_config(self):
        '''load exists .hackmd_notifier_config'''
        try:
            with open(self.config_file_path, "r") as f:
                data = f.read()
                config = json.loads(data)
                self.config = dict((key, value) for key, value in config.items())
            return True
        except:
            return False

    @property
    def get_configs(self):
        '''get config property'''
        return self.config

    @property
    def get_config_file_path(self):
        '''get config file path'''
        return self.config_file_path

    def show_current_settings(self):
        '''show current settings'''
        self.load_config()
        click.echo("Current settings: {} ".format(self.config))
