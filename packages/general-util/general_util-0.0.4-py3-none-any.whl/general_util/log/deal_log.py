import time
import grpc
import requests
from fastapi import Request
from fastapi.responses import JSONResponse
from .log_mapping import log_mapping
from ..config_manager import ConfigManager
from .system_log_schema import Log
from .proto import system_log_pb2, system_log_pb2_grpc


class DealSystemLog:
    def __init__(self, request: Request, response: JSONResponse, mapping:dict=None):
        self.request = request
        self.response = response
        self.mapping = log_mapping
        if mapping is not None:
            self.mapping.update(mapping)

    async def deal(self):
        print("start deal log")
        log = self.__create_system_log()
        print("write log: ", self.__write_log_g(log))

    async def deal_r(self):
        print("start deal log")
        log = self.__create_system_log()
        print("write log: ", self.__write_log_r(log))


    def __create_system_log(self):
        headers: dict = dict(self.response.headers)
        module, submodule, item = self.__get_module_submodule_item()
        headers["custom_header"] = "custom_value"
        self.response.init_headers(headers)
        t = time.time()
        return Log(
            timestamp= t,
            module=module,
            submodule=submodule,
            item=item,
            method=self.request.method,
            status_code=f"{self.response.status_code}",
            message_code=headers.get("message_code", ""),
            message=headers.get("message", ""),
            response_size=headers.get("content-length", ""),
            account=headers.get("account", ""),
            ip=self.request.client.host,
            api_url=self.request.url.path,
            query_params=self.request.url.query,
            web_path=headers.get("web_path", "")
        )

    def __get_module_submodule_item(self):
        if self.mapping.get(self.request.url.path, None) is not None:
            return self.mapping.get(self.request.url.path)
        else:
            url_path = self.request.url.path.split("/")
            return url_path[1], url_path[2], url_path[3]

    @staticmethod
    def __write_log_g(log):
        with grpc.insecure_channel(f"{ConfigManager.server.system_log_g_server}") as channel:
            stub = system_log_pb2_grpc.SystemLogServiceStub(channel)
            request = stub.WriteLog(system_log_pb2.LogRequest(
                timestamp=log.timestamp,
                module=log.module,
                submodule=log.submodule,
                item=log.item,
                method=log.method,
                status_code=log.status_code,
                message_code=log.message_code,
                message=log.message,
                response_size=log.response_size,
                account=log.account,
                ip=log.ip,
                api_url=log.api_url,
                query_params=log.query_params,
                web_path=log.web_path
            ))
            return stub.WriteLog(request)

    @staticmethod
    def __write_log_r(log):
        body = {
            "timestamp": log.timestamp,
            "module": log.module,
            "submodule": log.submodule,
            "item": log.item,
            "method": log.method,
            "status_code": log.status_code,
            "message_code": log.message_code,
            "message": log.message,
            "response_size": log.response_size,
            "account": log.account,
            "ip": log.ip,
            "api_url": log.api_url,
            "query_params": log.query_params,
            "web_path": log.web_path
        }
        url = f'{ConfigManager.server.system_log_r_server}/api/log/'
        headers = {
            'accept': 'application/json',
            'Content-Type': 'application/json'
        }
        response = requests.post(url, json=body, headers=headers)
        return response

