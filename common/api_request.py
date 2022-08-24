#!/usr/bin/python3.7
# -*- coding: utf-8 -*-
#-------------------------------------------------------------------------------
# @Time    : 2022/8/11 20:36
# @Author  : mojin
# @Email   : 397135766@qq.com
# @File    : api_request.py
# @Software: PyCharm
#-------------------------------------------------------------------------------

from requests import Session
from common.logger import Logger
from common.exchange_data import ExchangeData
import allure,json
class Api_Request(Session):

    @classmethod
    def api_data(cls,cases):
        url="http://192.168.1.10:8888/api/private/v1/"
        (
            case_id,
            case_title,
            header_ex,
            path,
            case_severity,
            skips,
            method,
            parametric_key,
            file_obj,
            data,
            extra,
            sql,
            expect,
        ) = cases

        # a,b=1,2

        path=ExchangeData.rep_expr(path,return_type='srt')
        header_ex=ExchangeData.rep_expr(header_ex,return_type='dict')
        data=ExchangeData.rep_expr(data,return_type='dict')
        file_obj=ExchangeData.rep_expr(file_obj,return_type='dict')
        Logger.info(case_title)

        res=Api_Request().api_request("%s%s"%(url,path),method,parametric_key,header_ex,(data),file_obj)

        ExchangeData.Extract(res,extra)

        ExchangeData.extra_allure(extra)#显示提取参数路径
        Logger.info('提取参数路径：%s' % extra)
        Logger.info('参数池：%s' % ExchangeData.extra_pool)


        return res






    def api_request(self,url, method, parametric_key, header=None, data=None, file=None) -> dict:
        if parametric_key=="params":
            parametric={"params":data}
        elif parametric_key=="data":
            parametric={"data":data}
        elif parametric_key=="json":
            parametric={"json":data}
        else:
            raise ValueError("“parametric_key”的可选关键字为params, json, data")


        req_info = {
            "请求地址": url,
            "请求头": header,
            "请求方法": method,
            '参数类型':parametric_key,
            "请求数据": data,
            "上传文件": str(file),
        }
        with allure.step('请求数据：'):
            allure.attach(
                json.dumps(req_info, ensure_ascii=False, indent=4),
                "附件内容",
                allure.attachment_type.JSON,
            )


        Logger.info('接口地址：%s' % url)
        Logger.info('请求头：%s' % header)
        Logger.info('请求方法：%s' % method)
        Logger.info('参数类型：%s' % parametric_key)
        Logger.info('请求参数：%s' % data)
        Logger.info('上传文件：%s' % file)
        try:
            res = self.request(method=method, url=url, files=file, headers=header, **parametric)
            #res = self.request(method=method, url=url, files=file, headers=header, data=data)
            response=res.json()
        except Exception as e:
            raise '请求发送失败：%s'%(e)

        Logger.info('返回响应：%s' % response)

        with allure.step('响应数据：'):
            allure.attach(
                json.dumps(response, ensure_ascii=False, indent=4),
                "附件内容",
                allure.attachment_type.JSON,
            )


        return response


#
# if __name__ == '__main__':
#     Api_Request=Api_Request()
#     method = 'post'  #get,post,put,delete,head,options,patch
#     url = 'http://***.**.***.*:9999/stage-api/'
#     header = {"Content-Type": "application/json;charset=UTF-8","Authorization":"eyJhbGciOiJIUzUxMiJ9.eyJsb2dpbl91c2VyX2tleSI6IjY2YTcxMjVjLTY4N2EtNGI1OS04ODJlLTE1YTk4ZDMxMWJiNyJ9.gfkoOQ6ZQbut71eSy1vbfZax-EZGKy58i1wnEdO2sNf_NqiM_RxXjGMz4otQq25VamKIFLiAnypmRZ6u3gykdQ"}
#     """
#     1. params：类似这种：url?参数名=参数值&参数名1=参数值1
#     2. data：请求头content-type是from表单类型。
#     3. json：请求头content-type：application/json。
#     """
#     parametric_key="json"#  params,data,json三种类型
#     data ={"searchValue":'',"createBy":"ff","createTime":"2022-02-25 14:16:50","updateBy":"","updateTime":'',"remark":'',"params":{},"noticeId":4,"noticeTitle":"22222","noticeType":"1","noticeContent":"wqe ","status":"0"}
#     #data ={}
#     file=''  #上传文件路径
#     a=Api_Request.api_request(url,method,parametric_key,header,data,file)
#     print(a)
#
