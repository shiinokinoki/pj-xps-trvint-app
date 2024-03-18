from data_class import AllInfo
from pydantic import BaseModel

def list_not_none_attributes(instance: BaseModel, instance_name: str) -> str:
    result = f'"{instance_name}":\n'
    not_none_found = False
    for field in instance.model_fields.keys():
        value = getattr(instance, field)
        if value is not None:
            result += f'- {field}: {value}\n'
            not_none_found = True
        else:
            result += f'- {field}: 抽出されませんでした\n'
    if not not_none_found:  # If all fields are None, add a placeholder
        result += '- No data available\n'
    return result

def create_chat_answer(parsed_data: AllInfo, gened_mail:str):
    output = ""
    output += "下記の情報を抽出しました。\n"
    agt_data_str = list_not_none_attributes(parsed_data.intermediate_company_info, "AGT情報:")
    output += agt_data_str
    cst_data_str = list_not_none_attributes(parsed_data.customer_info, "お客様情報:")
    output += cst_data_str

    output += '\n 不足情報を追加で受領するために、以下のような返信を提案します。\n'
    output += '>>>\n'
    output += gened_mail
    output += '\n\n[EOF]'
    return output
