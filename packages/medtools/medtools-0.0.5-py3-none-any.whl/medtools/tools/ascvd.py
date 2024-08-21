import requests
from bs4 import BeautifulSoup
from langchain_core.tools import tool
from pydantic.v1 import BaseModel, Field

from ..types import ToolResult

__all__ = ["ascvd"]


class Arguments(BaseModel):
    sex: int = Field(description="性别，1为男性，2为女性")
    age: int = Field(description="年龄")
    region: int = Field(
        description="现居住地区（以长江分界），0为南方，1为北方"
    )
    area: int = Field(description="地区，0为农村，1为城市")
    waist: int = Field(description="腰围，测量肚脐以上1公分处，单位为cm")
    tc_unit: int = Field(description="总胆固醇值 单位，1为mg/dl，2为mmol/L")
    tc: int = Field(description="总胆固醇值")
    hdlc_unit: int = Field(
        description="高密度脂蛋白胆固醇值 单位，1为mg/dl，2为mmol/L"
    )
    hdlc: int = Field(description="高密度脂蛋白胆固醇值")
    sbp: int = Field(description="当前血压水平，收缩压，单位为mmHg")
    dbp: int = Field(description="当前血压水平，舒张压，单位为mmHg")
    drug: int = Field(description="是否服用降压药，0为否，1为是")
    dm: int = Field(description="是否患有糖尿病，0为否，1为是")
    csmoke: int = Field(description="是否吸烟，0为否，1为是")
    fh_ascvd: int = Field(
        description="是否有心脑血管病家族史(指父母、兄弟姐妹中有人患有心肌梗死或脑卒中)，0为否，1为是"
    )


@tool
def ascvd(data: Arguments) -> ToolResult:
    """心脑血管病风险评估工具提供了一款针对中国人心脑血管病（包括急性心肌梗死、冠心病死亡和脑卒中）"""
    """发病风险进行评估和健康指导的实用工具，本工具适用于20岁及以上、无心脑血管病史的人群。"""
    """本工具能够根据用户输入的年龄、性别、血压等信息，准确评估个体未来发生冠心病、脑卒中等心脑血管病的风险，"""
    """并告知用户其心脑血管病危险的高低，有助于识别心脑血管病高危个体，并提早采取生活方式干预或临床治疗。"""
    """https://www.cvdrisk.com.cn/ASCVD/Eval"""
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    response = requests.post(
        "https://www.cvdrisk.com.cn/ASCVD/Eval/Result",
        headers=headers,
        data=data.__dict__,
    )
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")
        items = soup.find_all("div", class_="risk-score-value")
        result = {}
        for item in items:
            title = item.find_previous_sibling("p").text
            result[title] = item.text
        tool_result = {
            "依据": "中国心血管病风险评估和管理指南",
            "url": "http://www.cvdrisk.com.cn",
            "result": result,
        }
        return ToolResult(type="json", data=tool_result)
    else:
        return ToolResult(type="error", data="工具调用失败！")
