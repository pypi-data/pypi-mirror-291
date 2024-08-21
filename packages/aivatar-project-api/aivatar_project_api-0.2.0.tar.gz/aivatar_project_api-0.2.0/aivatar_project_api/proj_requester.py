# -*- coding: utf-8 -*-
#
# Copyright @ 2023 Tencent.com

import json
import requests
import urllib3

from .logger import init_logger

logger = init_logger("aivatar_project_tools")

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class ProjectItem(object):
    def __init__(self, project_id=-1, project_name="", experiment=0, experiment_expire_ts=0, days_to_expire=0):
        self.__project_id = project_id
        self.__project_name = project_name
        self.__experiment = int(experiment)
        self.__days_to_expire = int(days_to_expire)
        self.__experiment_expire_ts = int(experiment_expire_ts)

    @property
    def project_id(self):
        return self.__project_id

    @property
    def project_name(self):
        return self.__project_name

    @property
    def experiment(self):
        return self.__experiment

    @property
    def days_to_expire(self):
        return self.__days_to_expire

    @property
    def experiment_expire_ts(self):
        return self.__experiment_expire_ts

    def is_experiment(self):
        return bool(self.__experiment)


class AivProjectRequester(object):
    TIME_OUT = 600
    HEADERS = {"Content-Type": "application/json"}

    def __init__(self, token, business_type, url):
        self.__token = token
        self.__business_type = business_type

        self.url = url
        self.body = {"business_type": self.__business_type}
        self.cookies = {"arthub_account_ticket": self.__token}

    @property
    def token(self):
        return self.__token

    @property
    def business_type(self):
        return self.__business_type

    def query_projects(self):
        logger.info("url: {}".format(self.url))
        logger.info("body: {}".format(self.body))
        logger.info("cookies: {}".format(self.cookies))
        logger.info("headers: {}".format(self.HEADERS))
        response = requests.post(self.url, json=self.body, timeout=self.TIME_OUT, headers=self.HEADERS,
                                 cookies=self.cookies, verify=False)
        logger.info("response: {}".format(response.content))

        rsp_data = json.loads(response.content)
        req_id = rsp_data.get("request_id", "no request id!")
        code = rsp_data.get("code", -1)
        if code != 0:
            msg = rsp_data.get("error", "no error message!")
            raise RuntimeError("{}, request_id: {}".format(msg, req_id))
        result = rsp_data.get("result", {})
        # if not result: raise requests.exceptions.RequestException("Failed to find \"result\" in response!")

        items = result.get("items", [])
        project_items = []
        for item in items:
            proj_id = item.get("project_id", -1)
            proj_name = item.get("project_name", "")
            experiment = item.get("experiment", 0)
            experiment_expire_ts = item.get("experiment_expire_ts", 0)
            days_to_expire = item.get("days_to_expire", 0)
            project_items.append(ProjectItem(project_id=proj_id, project_name=proj_name, experiment=experiment, experiment_expire_ts=experiment_expire_ts, days_to_expire=days_to_expire))
        return project_items
