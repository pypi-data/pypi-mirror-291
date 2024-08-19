## Skyeye Python 工程增强器

1. fastapi R.E.D

## 简介

该项目主要用于采集客户端服务、服务全接口、单接口QPS、耗时、状态指标

## 使用说明
1、安装python增强器，命令如下

    pip install skyeye-python-instrumentator==0.1.5
    
    # 1. fastapi 增强引入
    from skyeye.web.middleware.fastapi import APMReporter
    app.add_middleware(APMReporter)