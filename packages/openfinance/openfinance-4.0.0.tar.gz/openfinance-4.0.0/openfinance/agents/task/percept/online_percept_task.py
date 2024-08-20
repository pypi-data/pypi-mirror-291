import asyncio
import json
import re

import datetime
from typing import Dict
from openfinance.config import Config

from openfinance.datacenter.database.source.event.cailianshe import get_cailianshe_news

from openfinance.datacenter.database.base import DataBaseManager
from openfinance.utils.robot.wechat.base import Wechat

from openfinance.agents.task.percept.percept_task import PerceptTask

db = DataBaseManager(Config()).get("db")

DURATION = 5 * 60

class OnlinePerceptTask(PerceptTask):
    name = "online_percept"
    async def aexecute(
        self, 
        text, 
        **kwargs
    ) -> Dict[str, str]:
        
        print("text", text)

        save_db = kwargs.get("save_db", False)
        wechat = kwargs.get("wechat", False)
        save_file = kwargs.get("save_file", False)
        if save_file and "filename" in kwargs:
            infile = open(kwargs.get("filename"), "a+")
        
        docs = list()
        max_len = 15

        while True:
            try:
                jsondata = get_cailianshe_news()
                for d in jsondata["data"]["roll_data"]:
                    if d["id"] in docs:
                        continue
                    if len(docs) == max_len:
                        docs.pop(0)
                    docs.append(d["id"])

                    # filter sources
                    if re.search(r".*（.*）.*", d["title"]):
                        continue

                    if d["subjects"]:
                        flag = False
                        for sd in d["subjects"]:
                            if "天气" in sd["subject_name"]:
                                flag = True
                        if flag:
                            continue
                    filters = ["这家公司", "早间新闻", "要闻"]
                    for i in filters:
                        if i in d['content']:
                            continue

                    # begin to percept
                    content = d["content"]
                    print("content: ", content)
                    result = await self.agent.tools["percept"].acall(
                        content, **kwargs
                    )
                    print("result: ", result)
                    match = result['output']
                    if not match["main_entity"]:
                        continue

                    if save_db:
                        db.insert(
                            "graph.t_news_percept",
                            {
                                "entity": match["main_entity"],
                                "entity_type": match["level"],
                                "indicator": match["indicator"],
                                "effect": match["sentiment"],
                                "src": match["event"],
                                "sid": str(d["id"])
                            }
                        )

                    if wechat:
                        #msg = "新闻: " + d["title"] + "\n"
                        msg = ""
                        msg += "主体: " + match["main_entity"] + "\n"
                        msg += "事件: " + match["event"] + "\n"
                        msg += "指标: " + match["indicator"] + "\n"
                        msg += "情绪: " + match["sentiment"] + "\n"
                        #Wechat.self_push(msg, name="港美缅股交流", isRoom=True)
                        msg += "来源: https://api3.cls.cn/a/" + str(d["id"])
                        Wechat.self_push(msg, name="实时热点财经新闻同步群5", isRoom=True)
                        if d["subjects"]:
                            for sd in d["subjects"]:
                                if "美股动态" == sd["subject_name"] or "港股动态" == sd["subject_name"]:
                                    Wechat.self_push(msg, name="港美缅股交流", isRoom=True)
                    if save_file:
                        infile.write(str(d["id"]) + "\t" + str(datetime.date.today()) + "\t")
                        if d["subjects"]:
                            for sd in d["subjects"]:
                                infile.write(sd["subject_name"] + "|")
                        infile.write("\t" + content.replace("\n", "@line@") + "\t")                                
                        infile.write(str(match) + "\n")
                        infile.flush()                                              
                await asyncio.sleep(DURATION)

            except Exception as e:
                print("Exception:", e)
        return {self.output: "finish detect!"}

if __name__ == '__main__':
    task = OnlinePerceptTask() 
    result = asyncio.run(
        task.aexecute(
            "开始", 
            save_db=False, 
            wechat=False,
            save_file=True,
            filename="openfinance/datacenter/knowledge/entity_graph/files/graph.txt",
        )
    )
    print(result)